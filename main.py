
import os
import re

import streamlit as st
import vertexai
from dotenv import load_dotenv
from google.api_core.retry import Retry
from google.cloud import bigquery
from langchain.document_loaders import BigQueryLoader
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
REGION = os.getenv("REGION")
PROJECT_ID = os.getenv("PROJECT_ID")

# Configure Streamlit page
st.set_page_config(
    page_title="Wynnsights", page_icon="👊", layout="wide", initial_sidebar_state="auto"
)

# Initialize session state
if "dataframe" not in st.session_state:
    st.session_state["dataframe"] = {}


# Initialize BigQuery client
client = bigquery.Client()


# Sidebar for user input and configuration
st.title("Wynnsights BQ")
st.sidebar.title("Configuration")

# Dataset selection
dataset = st.sidebar.selectbox(
    "Dataset", (f"{PROJECT_ID}.thelook", "bigquery-public-data.github_repos")
)

# Schema query
schema_query = f"""
SELECT table_name, ddl
FROM `{dataset}.INFORMATION_SCHEMA.TABLES`
WHERE table_type = 'BASE TABLE'
ORDER BY table_name;
"""

# LLM model selection
model_name = st.sidebar.selectbox("LLM Model Name", ("code-bison", "text-bison@002"))

# LLM parameters
max_output_tokens = st.sidebar.number_input(
    "Max Output Tokens", min_value=1, value=2048
)
temperature = st.sidebar.slider("Temperature (randomness)", 0.0, 1.0, 0.0)
top_p = st.sidebar.slider("Top P (determinism)", min_value=0, max_value=1, value=1)
top_k = st.sidebar.number_input(
    "Top K (vocabulary probability)", min_value=0, max_value=1, value=1
)
verbose = st.sidebar.checkbox("Verbose", value=True)

# Initialize LLM model
llm = VertexAI(
    model_name=model_name,
    max_output_tokens=max_output_tokens,
    temperature=temperature,
    top_p=top_p,
    top_k=top_k,
    verbose=verbose,
)

# Initialize prompt template
prompt = PromptTemplate.from_template(
    """
SYSTEM: You are a bigquery specialist helping users by suggesting a GoogleSQL query that will help them answer their question againsts the provided context. Do not add backticks to your answer. make sure you reply with valid GoogleSQL syntax.
=============
Question:
{question}
=============
context:
{schema}
"""
)

# Chain the prompt and LLM model
chain = prompt | llm

# Initialize BigQuery loader
loader = BigQueryLoader(query=schema_query, page_content_columns="ddl")


# Parse BigQuery schema from documents
def parse_bigquery_schema(documents):
    result = []

    for doc in documents:
        # Assuming each document has a 'page_content' attribute
        page_content = doc.page_content

        # Extract the DDL content and table name
        ddl_start = page_content.find("ddl: CREATE TABLE")
        ddl_end = page_content.find("\\n)\\nOPTIONS")
        ddl_content = page_content[ddl_start:ddl_end]
        table_name = re.search(r"`([^`]+)`", ddl_content).group(1)

        table_info = f"Table Name: `{table_name}`\n"
        columns_str = ddl_content.split("(")[1]
        columns = re.findall(r"(\w+ \w+),?", columns_str)

        column_info = "\n".join(
            ["   - " + col.replace("\\n", "").strip() for col in columns]
        )
        result.append(table_info + column_info)

    return "\n\n".join(result)


# Format BigQuery dataframe for display
def format_table(df):
    formatted_strings = []
    for row_name, row in df.iterrows():
        for col_name in df.columns:
            formatted_strings.append(f"{row_name}:{col_name}")
    return ", ".join(formatted_strings)


# Initialize Vertex AI client
vertexai.init(project=PROJECT_ID, location=REGION)

# Main app layout
with st.container():
    # Get user query
    user_query = st.text_input("Enter your query:")

    col1, col2 = st.columns(2)

    # Data and schema expanders
    with col2:
        data_placeholder = col2.expander("Data", expanded=True).empty()
        schema_placeholder = col2.expander("BQ Schema", expanded=False).empty()

        # Load data and schema
        data = loader.load()
        parsed_schema = parse_bigquery_schema(data)
        st.session_state["dataframe"] = parsed_schema
        schema_placeholder.write(parsed_schema)

    # Generate query button
    if col1.button("Generate Query"):
        bqschema = parse_bigquery_schema(data)
        googlesql = (
            (chain.invoke({"question": user_query, "schema": bqschema}))
            .strip("```")
            .strip("googlesql")
        )
        col1.code(googlesql, language="sql", line_numbers=True)

        # Execute query with retry
        custom_retry = Retry(
            initial=1.0,
            maximum=10.0,
            multiplier=2,
            deadline=300.0,
        )
        try:
            bqdata = (
                client.query(googlesql)
                .result(timeout=300, retry=custom_retry)
                .to_dataframe()
            )
            data_placeholder.write(bqdata)

            # Generate description and interpretation of the query
            describe = "you are a data scientist, describe this and interpret the query intent in relation to the bigquery schema answering the question: what is this information good for?, very briefly evaluate the IA generated sql in terms of optimization, stricly limit your response to information in this context:\n"
            col1.write(
                llm(
                    describe
                    + "bigquery schema: "
                    + bqschema
                    + " user query: "
                    + user_query
                    + "generated sql:"
                    + googlesql
                    + "data response: "
                    + format_table(bqdata)
                )
            )
        except Exception as e:
            st.error(f"Error executing query: {e}")
