import pygit2
import logging
import shutil
import github

import vertexai
from vertexai.language_models import TextGenerationModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

REPO_DIR = 'local_repo'
VERTEX_FOUNDATIONAL_MODEL = 'text-bison@002'

class Autocoder:

    def __init__(
            self,
            gcp_project: str,
            gcp_location: str,
            git_private_key: str,
            git_public_key: str,
            git_pat: str,
            git_key_passphrase: str = ""
    ):
        self.git_private_key = git_private_key
        self.git_public_key = git_public_key
        self.git_key_passphrase = git_key_passphrase
        self._local_repo = None
        self._github = github.Github(git_pat)

        vertexai.init(project=gcp_project, location=gcp_location)
        self._llm = TextGenerationModel.from_pretrained(VERTEX_FOUNDATIONAL_MODEL)

    def clone_repository(
            self,
            repo_link: str
    ):
        """Clones the provided repository

        :param repo_link: The link of the repo to clone (must be the SSH clone URL).
        :type repo_link: str
        """
        creds = pygit2.KeypairFromMemory(
            username='git',
            pubkey=self.git_public_key,
            privkey=self.git_private_key,
            passphrase=self.git_key_passphrase
        )
        self._pygit_callback = pygit2.RemoteCallbacks(credentials=creds)
        self._local_repo = pygit2.clone_repository(repo_link, REPO_DIR, callbacks=self._pygit_callback)

    @staticmethod
    def _fetch_repo_file_contents(
            repo_rel_path: str
    ) -> str:
        """Returns a string containing the content of the requested file path

        :param repo_rel_path: The file whose contents to return, relative to the root of the git repo.
        :type repo_rel_path: str
        :return: The contents of the requested file.
        :rtype: str
        """
        contents = None
        try:
            with open(f"{REPO_DIR}/{repo_rel_path}", 'r') as fp:
                contents = fp.read()
            return contents
        except:
            logger.error("Unable to fetch file contents.")
            raise

    @staticmethod
    def _write_repo_file_contents(
            repo_rel_path: str,
            contents: str
    ):
        """Overwrites the provided content to the provided file path.

        :param repo_rel_path: The relative path within the git repo to where the content should be written.
        :type repo_rel_path: str
        :param contents: The contents / file body to write.
        :type contents: str
        """
        try:
            with open(f"{REPO_DIR}/{repo_rel_path}", 'w') as fp:
                fp.write(contents)
        except:
            logger.error("Unable to write changes.")
            raise

    def create_branch(
            self,
            branch_name: str = None,
            contributing: str = None,
            desired_change: str = None
    ) -> str:
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
            prompt = f"Create an appropriate git feature branch name based on the requested code change -- do NOT format with markdown:\n{desired_change}"

            if contributing:
                prompt += f"\n\nFollow any branch naming convention within this guide, if any are stipulated:\n{contributing}"
            
            resp = self._llm.predict(prompt)
            branch_name = resp.text.strip()

        self._branch = self._local_repo.branches.local.create(branch_name, commit)
        self._branch.upstream = self._branch
        self._local_repo.checkout(self._branch)
        return branch_name

    def apply_code_changes(
            self,
            path_to_code: str,
            desired_change: str
    ) -> (str, str):
        """Applies the desired changes to the given code file path.

        :param path_to_code: The file path containing the code to update.
        :type path_to_code: str
        :param desired_change: The desired change (in natural language) to be applied to the code.
        :type desired_change: str
        :return: The old and new code.
        :rtype: (str, str)
        """
        existing_code = self._fetch_repo_file_contents(path_to_code)
        response = self._llm.predict(
                f"Given the below code:\n{existing_code}\n\nPlease adjust the code to fulfill the following change. Provide just the new version of the code -- do NOT surround the code in markdown backticks:\n{desired_change}"
            )
        replacement_code = response.text.strip()
        Autocoder._write_repo_file_contents(path_to_code, replacement_code)
        return existing_code, replacement_code
    
    def update_unit_tests(
            self,
            path_to_tests: str,
            updated_code: str
    ) -> str:
        """Updates the existing unit tests based on the updated code provided.

        :param path_to_tests: The relative path of the unit tests to update.
        :type path_to_tests: str
        :param updated_code: The new code that the unit tests need to be adapted for.
        :type updated_code: str
        :return: The adapted unit tests.
        :rtype: str
        """
        existing_tests = self._fetch_repo_file_contents(path_to_tests)
        replacement_unit_tests_prompt = f"Given the existing code:\n{updated_code}\n\nPlease change the unit tests below to work with the above code. Provide just the new version of the unit tests -- do NOT surround the unit tests in markdown backticks: \n\n{existing_tests}"

        response = self._llm.predict(replacement_unit_tests_prompt)
        logger.info(f"New unit tests: {response}")
        replacement_unit_tests = response.text.strip()
        self._write_repo_file_contents(path_to_tests, replacement_unit_tests)
        return replacement_unit_tests
    
    def create_commit(
            self,
            existing_code: str,
            replacement_code: str,
            commit_message: str = None,
            contributing: str = None,
            author_email: str = 'bot@evanseabrook.ca',
            author_name: str = 'EvanBot'
    ) -> str:
        """Adds all modified files and creates a commit in the branch. `apply_code_changes` and `update_unit_tests` should be called before calling this.

        :param existing_code: The code as it previously was before any changes.
        :type existing_code: str
        :param replacement_code: The new code written based on the desired change.
        :type replacement_code: str
        :param commit_message: The commit message to use -- one will be generated based on the changes found between `existing_code` and `replacement_code` if None provided, defaults to None
        :type commit_message: str, optional
        :param author_email: The email to use as the git commit author, defaults to 'bot@evanseabrook.ca'
        :type author_email: str, optional
        :param author_name: The name to use as the git commit author, defaults to 'EvanBot'
        :type author_name: str, optional
        :return: The commit message provided or generated.
        :rtype: str
        """
        if not commit_message:
            commit_msg_prompt = f"Please provide a commit message outlining the change between the old and new code. Provide just the commit message -- no need to title the message as 'commit message' or anything. Old code:\n{existing_code}\n\nNew code:\n{replacement_code}"

            if contributing:
                commit_msg_prompt += f"\n\nTake any commit structure instructions/examples into account from the following:\n{contributing}"
            response = self._llm.predict(
                commit_msg_prompt
            )
            commit_message = response.text.strip()
        
        index = self._local_repo.index
        parents = [self._local_repo.head.target]
        index.add_all()
        index.write()
        ref = self._local_repo.head.name
        author = pygit2.Signature(author_name, author_email)
        committer = author
        tree = index.write_tree()
        self._local_repo.create_commit(ref, author, committer, commit_message, tree, parents)
        return commit_message

    def push_remote(
            self,
            remote_name: str = 'origin'
    ):
        """Pushes the commit to the remote.

        :param remote_name: The remote to which changes should be pushed, defaults to 'origin'
        :type remote_name: str, optional
        """
        self._local_repo.remotes[remote_name].push([self._branch.upstream_name], self._pygit_callback)

    def create_pr(
            self,
            repo_id: int,
            issue_number: int,
            commit_message: str,
    ):
        """Creates a pull request in GitHub and ties it to the given issue.

        :param repo_id: The ID of the repository to create the pull request in.
        :type repo_id: int
        :param issue_number: The issue number (i.e. `1` in <https://github.com/evanseabrook/genai-issue-actor/pull/1>)
        :type issue_number: int
        :param commit_message: The commit message to use as the PR's body.
        :type commit_message: str
        """

        logger.info(f"repo_id: {repo_id}")
        logger.info(f"issue_id: {issue_number}")
        repo = self._github.get_repo(repo_id)
        logger.info(f"Repo owner: {repo.owner}")
        issues = repo.get_issues()
        logger.info(issues)
        for issue_instance in issues:
            logger.info(issue_instance.title)
            logger.info(issue_instance.id)
        issue = repo.get_issue(issue_number)
        repo.create_pull(
            base='main',
            head=self._branch.branch_name,
            body=commit_message,
            maintainer_can_modify=True,
            issue=issue
        )

    @staticmethod
    def cleanup_local_dir():
        """Deletes the locally cloned repository files.
        """
        shutil.rmtree(REPO_DIR, True)
        