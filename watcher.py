"""Desktop monitoring service."""

import requests
import json
import logging
import time
import datetime
from typing import Dict
from google.cloud import bigquery
import sys
from trexMinerDataSchema import TrexMinerDataSchema


TREX_HOST = "127.0.0.1"
TREX_PORT = "4067"
BIGQUERY_TABLENAME = "trex-watcher.desktop_logs.desktop_miner"
TARGET_ADDRESS = f"http://{TREX_HOST}:{TREX_PORT}/summary"
INTERVAL_SECONDS = 300  # Every 5 minutes
logging.basicConfig(level=logging.DEBUG)


def writeToBigQuery(query: str) -> str:
    """Upload one entry to BigQuery.

    Args:
        query: Full query to send to BigQuery.

    Returns: BigQuery return.
    """
    logging.info("Writing to BigQuery...")

    client = bigquery.Client()

    query_job = client.query(query)
    results = None
    try:
        results = query_job.result()  # Waits for job to complete.
    finally:
        client.close()
        logging.info(results)

    return results


def buildInsertNewEntryQuery(logContent: dict) -> str:
    fields = ""
    values = ""

    lengthLog = len(logContent)
    print("LENGTH: ", len(logContent))
    for field, value in logContent.items():
        #  Avoid syntax errors in BigQuery SQL with last comma
        if lengthLog <= 1:
            fields += f"{field}"
            values += f"'{value}'"
        else:
            fields += f"{field},"
            values += f"'{value}',"
            lengthLog -= 1

    now = datetime.datetime.now()
    return f"""
        INSERT `{BIGQUERY_TABLENAME}`
            ({fields}, script_exe_datetime, script_interval_seconds)
        VALUES ({values}, '{now.strftime("%b %d %Y %H:%M:%S")}', '{INTERVAL_SECONDS}');
    """


def createSchema(logEntry: json) -> dict:
    """Turn JSON log entry into Data Schema Object.

    Args:
        logEntry: One row of logs entry from Trex Miner.

    Returns: Specified fields as dictionary.
    """
    return TrexMinerDataSchema(logEntry).getSchema()


def startWatcher() -> None:
    logging.info("Checking if T-rex is online...")

    try:
        while True:
            response = requests.get(TARGET_ADDRESS)

            logContent = TrexMinerDataSchema(
                json.loads(response.text)).getSchema()
            logging.debug("Size of entry: %s bytes", sys.getsizeof(logContent))
            logging.debug(logContent)
            query = buildInsertNewEntryQuery(logContent)
            logging.debug(query)
            logging.info(writeToBigQuery(query))

            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt as ki:
        logging.info("STOP MONITORING ON %s *** \n %s", TARGET_ADDRESS, ki)

    # with open("s.txt", "w+") as f:
    # for p in x:
    #     if p.isinstance():
    #         print(f""""{p}": logJson["{p}"], """)


def iterateJson(jsonObject: json) -> None:
    """Recursive iteration of JSON."""
    recursiveTraverse(jsonObject)


def recursiveTraverse(dictLog: dict):
    """Iterate over JSON object."""
    logging.debug("recursiveTraverse")
    logging.debug(dictLog)

    for key, value in dictLog.items():
        if isinstance(value, Dict):
            recursiveTraverse(value)
        elif isinstance(value, list):
            logging.debug("list found")
            for sub in value:
                recursiveTraverse(sub)
        else:
            print(f""""{key}": logJson["{key}"],""")
            logging.debug(f"END CASE: {key} :: {value}")


if __name__ == "__main__":
    # _tempFormat()
    startWatcher()
