from prefect import flow

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO="https://github.com/zhenxiay/Prefect_Test.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="Flow/Test_data_ingestion_stock_intelligence.py:ingest_stock_data",
    ).deploy(
        name="deployment-stock-intelligence",
        parameters={
            "db_name": "portfolio_analysis",
            "stock_list": ['MSFT','ASML']
        },
        work_pool_name="data-ingestion-wp",
        cron="0 6 * * 7",
    )
