# Sales Data Query Generator

This project uses GPT4All to generate SQL queries for a Snowflake database based on natural language questions. It includes a Streamlit web interface and can update a Superset dashboard with query results.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/sales-data-query-generator.git
   cd sales-data-query-generator
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Snowflake credentials:
   ```
   SNOWFLAKE_ACCOUNT=your_account_locator
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=sample_db
   SNOWFLAKE_SCHEMA=public
   ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

5. Open your web browser and go to `http://localhost:8501` to use the app.

## Usage

1. Enter a question about the sales data in the text input field.
2. Click "Generate and Execute Query" to generate an SQL query, execute it, and see the results.
3. The app will also update a Superset dashboard with the query results.

## Note

Make sure you have set up your Snowflake database and Superset dashboard before running the app. Update the dashboard and chart IDs in the `update_superset_dashboard` function as needed.