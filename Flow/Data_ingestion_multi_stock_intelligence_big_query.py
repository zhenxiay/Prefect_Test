from StockIntelligence.load_multi_stock_data import LoadMultiStockData
from prefect import flow, task

@flow(log_prints=True)
def ingest_stock_data(table_name: str, stock_list: list[str], project: str):
    """Flow: Show results of the data ingested"""
    # Call Task 1
    portfolio = fetch_data(stock_list,
                          project)
    
    print(f"portfolio created for {stock_list} in GCP project {project}")

    # Call Task 2
    result_data_ingestion = ingest_data(portfolio, 
                                        stock_list, 
                                        table_name)

    # Print the result
    print(f"{result_data_ingestion}")

@task
def fetch_data(stock_list: list[str], project: str):
    """Task 1: Fetch the data from a stock intelligence library"""
    portfolio = LoadMultiStockData(stock_list, 
                                  '2y', 
                                  project, 
                                  'StockIntelligence')
    
    return portfolio

@task
def ingest_data(portfolio, stock_list: list[str], table_name: str):
    """Task 2: Write data into big query"""
    
    portfolio.load_multi_stock_data_to_big_query(stock_list, table_name)
    
    return f'Ingested stock data: {stock_list} into {table_name}'


# Run the flow
if __name__ == "__main__":
    ingest_stock_data(
                    'portfolio_analysis',
                     [
                     "MSFT",
                     "NVDA",
                     "ASML"
                     ],
                     'keen-vial-420113'
                     )