import os
from dotenv import load_dotenv
import vertexai
from langchain.llms import VertexAI
from google.cloud import bigquery
from langchain.llms import VertexAI
from langchain.document_loaders import BigQueryLoader
from langchain.prompts import PromptTemplate
import streamlit as st
import pandas as pd
import re
from google.api_core.retry import Retry


load_dotenv()
REGION = os.getenv('REGION')
PROJECT_ID = os.getenv('PROJECT_ID')


st.set_page_config(page_title="