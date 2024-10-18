import warnings
from sqlalchemy import exc as sa_exc

# Suppress specific SAWarning related to function registration
warnings.filterwarnings("ignore", category=sa_exc.SAWarning, message=".*GenericFunction 'flatten'.*")

import os
import streamlit as st
from dotenv import load_dotenv
from gpt4all import GPT4All
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
# from superset_api_client import SupersetClient
import requests
import json

# Load environment variables
load_dotenv()

# Initialize GPT4All model
try:
    model = GPT4All("ggml-gpt4all-j-v1.3-groovy")

except Exception as e:
    st.error(f"Failed to initialize GPT4All model: {e}")
    print(f"Error details: {e}")


# Function to generate SQL query
def generate_sql_query(question):
    prompt = f"""
    Given the following question, generate a SQL query to answer it using the sales table.
    The sales table has the following columns: date, product, quantity, revenue.

    Question: {question}

    SQL Query:
    """
    try:
        response = model.generate(prompt, max_tokens=100)
        return response.strip()
    
    except Exception as e:
        st.error(f"Error generating SQL query: {str(e)}")
        return None
    

# Function to execute SQL query on Snowflake
def execute_snowflake_query(query):
    try:
        engine = create_engine(URL(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
        ))
        with engine.connect() as conn:
            result = conn.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None


# Function to update Superset dashboard
def update_superset_dashboard(dashboard_id, chart_id, dataframe):
    try:
        client = SupersetClient(
            host="http://localhost:8080",
            username="admin",
            password="admin"
        )
        
        # Update chart data
        client.update_chart_data(chart_id, dataframe)

        # Refresh dashboard
        client.refresh_dashboard(dashboard_id)
        st.success("Superset dashboard updated successfully.")
    except Exception as e:
        st.error(f"Error updating Superset dahsboard: {str(e)}")


# Streamlit app
def main():
    st.title("Sales Data Query Generator")

    # User input
    question = st.text_input("Enter your question about the sales data:")

    if st.button("Generate and Execute Query"):
        if question:
            # Generate SQL query
            sql_query = generate_sql_query(question)
            st.subheader("Generated SQL Query:")
            st.code(sql_query, language="sql")

            # Execute query
            result_df = execute_snowflake_query(sql_query)
            if result_df is not None:
                st.subheader("Query Result: ")
                st.dataframe(result_df)

                # Update Superset dashboard
                update_superset_dashboard(1, 1, result_df)

        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()





