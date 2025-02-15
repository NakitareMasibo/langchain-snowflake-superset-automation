import json
import os
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
from superset_api_client import SupersetClient

# Load Snowflake configuration
with open('snowflake_config.json') as f:
    snowflake_config = json.load(f)

# Set up OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-QxWzUSzVvZdU7q7eFvnPm8mRwFQCvCPXupqJMlGad2T3BlbkFJKQw4bkGP4dSOzwINAEIi9edzNRPS-vDTLjqj4SXx4A'

# Set up LangChain
llm = OpenAI(temperature=0)
template = """
Given the following question, generate a SQL query to answer it using the sales table.
The sales table has the following columns: date, product, quantity, revenue.

Question: {question}

SQL Query:
"""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Function to execute SQL query on Snowflake
def execute_snowflake_query(query):
    engine = create_engine(URL(
        account=snowflake_config['account'],
        user=snowflake_config['user'],
        password=snowflake_config['password'],
        database=snowflake_config['database'],
        schema=snowflake_config['schema'],
        warehouse=snowflake_config['warehouse']
    ))
    
    with engine.connect() as conn:
        result = conn.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    return df

# Function to update Superset dashboard
def update_superset_dashboard(dashboard_id, chart_id, dataframe):
    client = SupersetClient(
        host="http://localhost:8080",
        username="admin",
        password="admin"
    )
    
    # Update chart data
    client.update_chart_data(chart_id, dataframe)
    
    # Refresh dashboard
    client.refresh_dashboard(dashboard_id)

# Main execution
if __name__ == "__main__":
    question = "What is the total revenue for each product?"
    sql_query = llm_chain.run(question)
    print(f"Generated SQL Query: {sql_query}")

    result_df = execute_snowflake_query(sql_query)
    print("Query Result:")
    print(result_df)

    # Update Superset dashboard (replace with your actual dashboard and chart IDs)
    update_superset_dashboard(1, 1, result_df)
    print("Superset dashboard updated successfully.")