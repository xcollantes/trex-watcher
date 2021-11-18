"""Desktop monitoring service."""

import requests
import json
import logging
import time
from typing import List
from google.cloud import bigquery


TREX_HOST = "127.0.0.1"
TREX_PORT = "4067"
TARGET_ADDRESS = f"http://{TREX_HOST}:{TREX_PORT}/summary"
INTERVAL_SECONDS = 5
logging.basicConfig(level=logging.DEBUG)


def pretty(input: json, indent: int = 4) -> str:
    """Print out JSON."""
    return logging.debug(json.dumps(json.loads(input), indent=indent))


def startWatcher() -> None:
    logging.info("Checking if T-rex is online...")

    logging.info("Connecting to BigQuery...")

    client = bigquery.Client()

    query1 = """
            CREATE OR REPLACE TABLE desktop_logs.books AS
            SELECT 'Hamlet' title, 'William Shakespeare' author;

            INSERT desktop_logs.books (title, author)
            VALUES('The Great Gatsby', 'F. Scott Fizgerald'),
                  ('War and Peace', 'Leo Tolstoy');
        """

    query2 = """
        ALTER TABLE desktop_logs.books

    """

    query_job = client.query(query2)

    results = query_job.result()  # Waits for job to complete.
    logging.info(results)

    for row in results:
        print("{} : {} views".format(row.url, row.view_count))

    # try:
    #     while True:
    #         logging.debug(pretty(response.text))
    #         response = requests.get(TARGET_ADDRESS)
    #         # logging.info(response.json)
    #         time.sleep(INTERVAL_SECONDS)
    # except KeyboardInterrupt as ki:
    #     logging.info("STOP MONITORING ON %s *** \n %s", TARGET_ADDRESS, ki)


if __name__ == "__main__":
    startWatcher()
