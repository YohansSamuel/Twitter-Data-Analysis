import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error

def DBConnect(dbName=None):
    """
    Parameters
    ----------
    dbName :
        Default value = None)
    Returns
    -------
    #os.getenv('mysqlPass')
    """
    conn = mysql.connect(host='localhost', user='root', password='root',
                         database=dbName, buffered=True)
    cur = conn.cursor()
    return conn, cur