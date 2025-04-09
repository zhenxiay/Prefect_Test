import pandas as pd
from StockIntelligence.load_multi_stock_data import LoadMultiStockData
import sqlite3
from prefect import flow, task

@flow(log_prints=True)
def ingest_stock_data(db_name: str, stock_list: list[str]):
    """Flow: Show results of the data ingested"""
    # Call Task 1
    data = fetch_data(stock_list)
    print(f"{len(data)} read for {stock_list}")

    # Call Task 2
    result_data_ingestion = ingest_data(data, db_name)

    # Print the result
    print(f"{result_data_ingestion}")

@task
def fetch_data(stock_list: list[str]):
    """Task 1: Fetch the data from a stock intelligence library"""
    porfolio = LoadMultiStockData(stock_list, 
                                  '2y', 
                                  'project', 
                                  'dataset')
    
    return porfolio.create_combined_dataset(stock_list)

@task
def ingest_data(data, db_name):
    """Task 2: Write data into a sqlite3 db"""
    conn = sqlite3.connect(db_name)
    data.to_sql('portfolio_analysis',
                 con=conn,
                 if_exists="replace"
                 )
    
    return f'Ingested rows: {len(data)} into {db_name}, table portfolio_analysis'


# Run the flow
if __name__ == "__main__":
    ingest_stock_data('stock_intelligence',
                     [
                     "MSFT",
                     "ASML"
                     ])
