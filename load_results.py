import logging
import sqlite3
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

CSV_PATH = Path("data/raw/test_result.csv")  
SEP = "|"
DB_PATH = Path("data/mot.db")
TABLE = "mot_results"
CHUNK_SIZE = 100_000


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    total = 0
    try:
        for i, chunk in enumerate(pd.read_csv(CSV_PATH, sep=SEP, chunksize=CHUNK_SIZE)):
            mode = "replace" if i == 0 else "append"
            chunk.to_sql(TABLE, conn, if_exists=mode, index=False)
            total += len(chunk)
            log.info("chunk %d loaded, %d rows so far", i, total)
    finally:
        conn.close()
    log.info("done: %d rows in table %s", total, TABLE)


if __name__ == "__main__":
    main()