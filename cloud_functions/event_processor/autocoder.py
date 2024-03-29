import logging
import os
import shutil
import github
from langchain_google_genai import ChatGoogleGenerativeAI
import pygit2
from langchain.prompts import PromptTemplate
from langchain.output_parsers import (
    OutputFixingParser,
    PydanticOutputParser,
    RetryOutputParser,
)
from langchain_core.pydantic_v1 import BaseModel, Field, validator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

REPO_DIR = "local_repo"


class GitBranch(BaseModel):
    name: str = Field(description="valid name for a git branch")

    @validator('name')
    def restrictions(cls, name):
        forbidden_chars = [' ', '/', '\\', '?', '*', ':', '..']
        if any(char in name for char in forbidden_chars) or name.startswith('.') or name.endswith('.'):
            return cls.fix_branch_name(name)
        return name

    @classmethod
    def fix_branch_name(cls, name):
        forbidden_chars = [' ', '/', '\\', '?', '*', ':', '..']
        for char in forbidden_chars:
            name = name.replace(char, '_')
        name = name.strip('.')
        if name[0] in forbidden_chars:
            name = name[1:]
        if name[-1] in forbidden_chars:
            name = name[:-1]
        # Replace sequences of underscores caused by replacement with a single underscore
        name = '_'.join(filter(None, name.split('_')))
        return name
    
class GitFile(BaseModel):
    file: str = Field(description="valid file contents")

    @validator('file')
    def validate_file_language(cls, v):
        recognized_languages = [
            "python", "java", "c++", "javascript", "php", "ruby", "go", "swift", "kotlin", "scala",
            "rust", "typescript", "coffeescript", "elixir", "erlang", "fortran", "haskell", "ocaml",
            "perl", "prolog", "r", "scheme", "smalltalk", "tcl", "vim", "yaml"
        ]
        first_line = v.strip().splitlines()[0] if v.strip().splitlines() else ''
        if first_line.startswith('```') and v.endswith('```'):
            lang = first_line[3:].strip()
            if lang in recognized_languages:
                return cls.fix_language_block(v, lang)
        return v

    @classmethod
    def fix_language_block(cls, v, lang):
        if v.startswith(f'```{lang}') and v.endswith('```'):
            v = v[len(f'```{lang}'):].rstrip('```').strip()
        return v

class GitCommit(BaseModel):
    message: str = Field(description="a git commit message")

    @validator('message')
    def validate_message(cls, v):
        v = cls.fix_message(v) 
        return v

    @classmethod
    def fix_message(cls, v):
        if v.startswith('```'):
            v = v[3:]
        if v.endswith('```'):
            v = v[:-3]
        return v

class Autocoder:
    def __init__(
        self,
        git_private_key: str,
        git_public_key: str,
        git_pat: str,
        git_key_passphrase: str = "",
        llm: str = "",
        gemini_api_key: str = "",
    ):
        self.git_private_key = git_private_key
        self.git_public_key = git_public_key
        self.git_key_passphrase = git_key_passphrase
        self._local_repo = None
        self._github = github.Github(git_pat)
        self._llm = ChatGoogleGenerativeAI(model=llm, google_api_key=gemini_api_key)

    def clone_repository(self, repo_link: str):
        """Clones the provided repository

        :param repo_link: The link of the repo to clone (must be the SSH clone URL).
        :type repo_link: str
        """
        creds = pygit2.KeypairFromMemory(
            username="git",
            pubkey=self.git_public_key,
            privkey=self.git_private_key,
            passphrase=self.git_key_passphrase,
        )
        self._pygit_callback = pygit2.RemoteCallbacks(credentials=creds)
        self._local_repo = pygit2.clone_repository(
            repo_link, REPO_DIR, callbacks=self._pygit_callback
        )

    @staticmethod
    def _fetch_repo_file_contents(repo_rel_path: str) -> str:
        """Returns a string containing the content of the requested file path

        :param repo_rel_path: The file whose contents to return, relative to the root of the git repo.
        :type repo_rel_path: str
        :return: The contents of the requested file.
        :rtype: str
        """
        try:
            with open(f"{REPO_DIR}/{repo_rel_path}", "r") as fp:
                return fp.read()
        except Exception as e:
            logger.error(f"Unable to fetch file contents: {e}")
            raise

    @staticmethod
    def _write_repo_file_contents(repo_rel_path: str, contents: str):
        """Overwrites the provided content to the provided file path.

        :param repo_rel_path: The relative path within the git repo to where the content should be written.
        :type repo_rel_path: str
        :param contents: The contents / file body to write.
        :type contents: str
        """
        try:
            with open(f"{REPO_DIR}/{repo_rel_path}", "w") as fp:
                fp.write(contents)
        except Exception as e:
            logger.error(f"Unable to write changes: {e}")
            raise

    def create_branch(self, branch_name: str = None, desired_change: str = None) -> str:
        """Creates and checks out a branch in the cloned repo.

        :param branch_name: The optional name of the branch to create, defaults to None. If None, a branch name is generated based on `desired_change` and `contributing`
        :type branch_name: str, optional
        :param contributing: The contributing guidelines to take into account when creating a branch name, defaults to None
        :type contributing: str, optional
        :param desired_change: The description of the change to make on which to base the branch name, defaults to None
        :type desired_change: str, optional
        :return: The branch name provided / generated.
        :rtype: str
        """
        commit = self._local_repo.head.peel()

        if not branch_name:
            contributing = ''
            try:
                contributing = self._fetch_repo_file_contents("CONTRIBUTING.md")
            except:
                logger.info("No existing CONTRIBUTING.md to use.")
                contributing = 'git best practices'
                pass
            
            parser = PydanticOutputParser(pydantic_object=GitBranch)                        
            prompt = PromptTemplate(
                template="Create a branch name for this change:\n{desired_change}\nuse this guidelines:\n{contributing}\nformat:\n{format_instructions}. DO NOT add any wrapper or comment to your response, just the branch name.",
                input_variables=["desired_change","contributing"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                }
            )            
            chain = prompt | self._llm | parser
            branch_name = chain.invoke(
                    {
                        "desired_change": desired_change, 
                        "contributing": contributing
                    }
                ).name
        
        self._branch = self._local_repo.branches.local.create(branch_name, commit)
        self._branch.upstream = self._branch
        self._local_repo.checkout(self._branch)
        return branch_name

    def apply_code_changes(self, path_to_code: str, desired_change: str) -> (str, str):
        """Applies the desired changes to the given code file path.

        :param path_to_code: The file path containing the code to update.
        :type path_to_code: str
        :param desired_change: The desired change (in natural language) to be applied to the code.
        :type desired_change: str
        :return: The old and new code.
        :rtype: (str, str)
        """
        existing_file = self._fetch_repo_file_contents(path_to_code)

        parser = PydanticOutputParser(pydantic_object=GitFile)     
        prompt = PromptTemplate(
            template="Given the file:\n{existing_file}\n\nPlease adjust it to fulfill the following change:\n{desired_change}.\n reply with the file contents with the desired change only, do not add any markdown wrapper, explanations or comments to your response, just the file contents. overal comply with the following format instructions but dont add the format instructions to your response:\n{format_instructions}",
            input_variables=["existing_file","desired_change"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()
            }
        )            
        chain = prompt | self._llm | parser
        replacement_file = chain.invoke(
            {
                "existing_file": existing_file,
                "desired_change": desired_change
            }
        ).file
        
        Autocoder._write_repo_file_contents(
            path_to_code, 
            replacement_file
        )
        return existing_file, replacement_file

    def create_commit(
        self,
        existing_code: str,
        replacement_code: str,
        commit_message: str = None,
        author_email: str = "lapeyus@gmail.com",
        author_name: str = "lapeyus",
    ) -> str:
        """Adds all modified files and creates a commit in the branch. `apply_code_changes` should be called before calling this.

        :param existing_code: The code as it previously was before any changes.
        :type existing_code: str
        :param replacement_code: The new code written based on the desired change.
        :type replacement_code: str
        :param commit_message: The commit message to use -- one will be generated based on the changes found between `existing_code` and `replacement_code` if None provided, defaults to None
        :type commit_message: str, optional
        :param author_email: The email to use as the git commit author, defaults to 'lapeyus@gmail.com'
        :type author_email: str, optional
        :param author_name: The name to use as the git commit author, defaults to 'lapeyus'
        :type author_name: str, optional
        :return: The commit message provided or generated.
        :rtype: str
        """
        if not commit_message:
            try:
                contributing = self._fetch_repo_file_contents("CONTRIBUTING.md")
            except:
                logger.info("No existing CONTRIBUTING.md to use.")
                contributing = 'use git best practices'
                pass

            parser = PydanticOutputParser(pydantic_object=GitCommit)        
            prompt = PromptTemplate(
                template="Please provide a commit message outlining the change between the old and new code. Old code:\n{existing_code}\n\nNew code:\n{replacement_code}\n\nUse this guidelines:\n{contributing}\nformat:\n{format_instructions}. DO NOT add any markdown wrapper, explanations or comments to your response, just the commit message.",
                input_variables=["existing_code","replacement_code"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                }
            )            
            chain = prompt | self._llm | parser
            commit_message = chain.invoke(
                {
                    "existing_code": existing_code,
                    "replacement_code": replacement_code,
                    "contributing": contributing
                }
            ).message

        commit_message += f"\n\nSigned-off-by: {author_name} <{author_email}>"

        index = self._local_repo.index
        parents = [self._local_repo.head.target]
        index.add_all()
        index.write()
        ref = self._local_repo.head.name
        author = pygit2.Signature(author_name, author_email)
        committer = author
        print(author, committer)
        tree = index.write_tree()
        self._local_repo.create_commit(
            ref, author, committer, commit_message, tree, parents
        )
        return commit_message

    def push_remote(self, remote_name: str = "origin"):
        """Pushes the commit to the remote.

        :param remote_name: The remote to which changes should be pushed, defaults to 'origin'
        :type remote_name: str, optional
        """
        self._local_repo.remotes[remote_name].push(
            [self._branch.upstream_name], self._pygit_callback
        )

    def create_pr(
        self,
        repo_id: int,
        issue_number: int,
        commit_message: str = None,
    ):
        """Creates a pull request in GitHub and ties it to the given issue.

        :param repo_id: The ID of the repository to create the pull request in.
        :type repo_id: int
        :param issue_number: The issue number (i.e. `1` in <https://github.com/evanseabrook/genai-issue-actor/pull/1>)
        :type issue_number: int
        :param commit_message: The commit message to use as the PR's body.
        :type commit_message: str
        """
        if not commit_message:
            try:
                contributing = self._fetch_repo_file_contents("CONTRIBUTING.md")                
            except:
                logger.info("No existing CONTRIBUTING.md to use.")
                contributing = 'use git best practices'
                pass

            parser = PydanticOutputParser(pydantic_object=GitCommit)
            prompt = PromptTemplate(
                template="Please provide a commit message outlining the change between the old and new files. Provide just the commit message, your response will be inserted into a create PR request so it needs to be valid.\n\nUse this guidelines:\n{contributing}\nformat:\n{format_instructions}. DO NOT add any wrapper or comment in your response, just the commit message.",
                input_variables=["contributing"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                }
            )            
            chain = prompt | self._llm | parser
            commit_message = chain.invoke(
                {
                    "contributing": contributing
                }
            ).message

        repo = self._github.get_repo(repo_id)
        # issues = repo.get_issues()
        # for issue_instance in issues:
        #     logger.info(issue_instance.title)
        #     logger.info(issue_instance.id)
        issue = repo.get_issue(issue_number)
        repo.create_pull(
            base="main",
            head=self._branch.branch_name,
            body=commit_message,
            maintainer_can_modify=True,
            issue=issue,
        )

    @staticmethod
    def cleanup_local_dir():
        if os.path.exists(REPO_DIR):
            shutil.rmtree(REPO_DIR, ignore_errors=True)
