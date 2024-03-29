import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import os
# from streamlit_feedback import streamlit_feedback
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

 

model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="")


class GitBranch(BaseModel):
    name: str = Field(description="valid name for a git branch")

class GitFile(BaseModel):
    file: str = Field(description="file contents")

create_branch_prompt_template = PromptTemplate.from_template(
                "Create a branch name based on it's purpose:\n{desired_change}\nand this guidelines:\n{contributing}. only reply with the branch name, don't add any explanation or aditional text, your response will be inserted in a git create branch command"
            )
parser = PydanticOutputParser(pydantic_object=GitBranch)
template = "Create a branch name based on it's purpose:\n{desired_change}\nand this guidelines:\n{contributing}\nformat:{format_instructions}"
prompt = PromptTemplate(
    template=template,
    input_variables=["desired_change","contributing"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)            
chain = prompt | model| parser
branch_name = chain.invoke({"desired_change": "add units tests", "contributing": "git best practices"}).name
print(branch_name)