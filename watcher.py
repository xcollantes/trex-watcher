"""Desktop monitoring service."""

import requests
import json
import logging
import time
from typing import Dict
from google.cloud import bigquery
from trexMinerDataSchema import TrexMinerDataSchema


TREX_HOST = "127.0.0.1"
TREX_PORT = "4067"
TARGET_ADDRESS = f"http://{TREX_HOST}:{TREX_PORT}/summary"
INTERVAL_SECONDS = 5
logging.basicConfig(level=logging.DEBUG)


def pretty(input: json, indent: int = 4) -> str:
    """Print out JSON."""
    return logging.debug(json.dumps(json.loads(input), indent=indent))


def writeToBigQuery(row: Dict) -> str:
    """Upload one entry to BigQuery.

    Args:
        row: One entity of data made up of key-value pair of field and value.
             [field_name, field_value]

    Returns: BigQuery return.
    """
    logging.info("Writing to BigQuery...")
    logging.info("Connecting to BigQuery...")

    client = bigquery.Client()

    query = """
        INSERT desktop_logs.eth_logs ()
        VALUES('The Great Gatsby', 'F. Scott Fizgerald'),
              ('War and Peace', 'Leo Tolstoy');
    """

    query_job = client.query(query)
    results = query_job.result()  # Waits for job to complete.
    logging.info(results)

    return results


def jsonToDict(logJson: json) -> Dict:
    """Extract data from log into dictionary.

    Args:
        logJson: JSON object from Trex.

    Returns: Dictionary.
    """
    logEntry = {

    }
    return logEntry


def buildQuery(log: json) -> str:
    pass


def startWatcher() -> None:
    logging.info("Checking if T-rex is online...")

    try:
        while True:
            response = requests.get(TARGET_ADDRESS)

            logContent = TrexMinerDataSchema(
                json.loads(response.text)).getSchema()
            logging.debug(logContent)
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt as ki:
        logging.info("STOP MONITORING ON %s *** \n %s", TARGET_ADDRESS, ki)

    # with open("s.txt", "w+") as f:
    # for p in x:
    #     if p.isinstance():
    #         print(f""""{p}": logJson["{p}"],""")


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
