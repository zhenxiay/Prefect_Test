from prefect import flow

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO="https://github.com/zhenxiay/Prefect_Test.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="Prefect_Flow_Read_Credit_Risk.py:ingest_credit_risk",
    ).deploy(
        name="deployment-credit-risk",
        parameters={
            "path": "https://raw.githubusercontent.com/PacktPublishing/Python-for-Finance-Cookbook/master/Datasets/credit_card_default.csv",
            "db_name": "credit_risk_db"
        },
        work_pool_name="data-ingestion-wp",
        cron="0 6 * * 7",
    )