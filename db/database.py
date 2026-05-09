import os
import pyodbc
from queue import Queue
from threading import Lock
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor

# =========================
# Config
# =========================
SERVER = os.getenv("DB_SERVER", r"WIN-8F5G6TCFF1J\SQL2022")
DATABASE = os.getenv("DB_NAME", "Crypto")
DB_USERNAME = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASS", "Aa@123456")

DB_CONNECTION_STRING = (
    f"DRIVER={{SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={DB_USERNAME};"
    f"PWD={DB_PASSWORD}"
)

# =========================
# Pool
# =========================
class ConnectionPool:
    def __init__(self, max_size=50):
        self.pool = Queue(max_size)
        self.lock = Lock()

        for _ in range(max_size):
            self.pool.put(self._new_conn())

    def _new_conn(self):
        return pyodbc.connect(DB_CONNECTION_STRING)

    def get_connection(self):
        with self.lock:
            conn = self.pool.get()
            try:
                conn.cursor().execute("SELECT 1")
            except:
                try:
                    conn.close()
                except:
                    pass
                conn = self._new_conn()
            return conn

    def return_connection(self, conn):
        if conn:
            with self.lock:
                self.pool.put(conn)

connection_pool = ConnectionPool(
    max_size=int(os.getenv("DB_POOL_SIZE", "50"))
)

@contextmanager
def db_conn():
    conn = None
    try:
        conn = connection_pool.get_connection()
        yield conn
    finally:
        connection_pool.return_connection(conn)

executor = ThreadPoolExecutor(
    max_workers=int(os.getenv("MAX_WORKERS", "50"))
)