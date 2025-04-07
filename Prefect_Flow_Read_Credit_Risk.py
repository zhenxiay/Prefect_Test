import pandas as pd
import sqlite3
from prefect import flow, task

@flow(log_prints=True)
def ingest_credit_risk(path: str, db_name: str):
    """Flow: Show results of the data ingested"""
    # Call Task 1
    data = fetch_data(path)
    print(f"{len(data)} read from {path}")

    # Call Task 2
    result_data_ingestion = ingest_data(data, db_name)

    # Print the result
    print(f"{result_data_ingestion}")


@task
def fetch_data(path: str):
    """Task 1: Fetch the data from a GitHub repo"""
    return pd.read_csv(path)


@task
def ingest_data(data, db_name):
    """Task 2: Write data into a sqlite3 db"""
    conn = sqlite3.connect(db_name)
    data.to_sql('credit_risk',
                 con=conn,
                 if_exists="replace"
                 )
    
    return f'Ingested rows: {len(data)}'


# Run the flow
if __name__ == "__main__":
    ingest_credit_risk('https://raw.githubusercontent.com/PacktPublishing/Python-for-Finance-Cookbook/master/Datasets/credit_card_default.csv',
                       'credit_risk_db')