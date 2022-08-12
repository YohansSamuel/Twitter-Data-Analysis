import os
import pandas as pd
import mysql.connector as mysql
from mysql.connector import Error

# make a database connection
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
    conn = mysql.connect(host='localhost', user='root', password='********',
                         database=dbName, buffered=True)
    cur = conn.cursor()
    return conn, cur

def emojiDB(dbName: str) -> None:
    conn, cur = DBConnect(dbName)
    dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
    cur.execute(dbQuery)
    conn.commit()

# create database
def createDB(dbName: str) -> None:
    """
    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :
    Returns
    -------
    """
    conn, cur = DBConnect()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
    conn.commit()
    cur.close()

# create tables
def createTables(dbName: str) -> None:
    """
    Parameters
    ----------
    dbName :
        str:
    dbName :
        str:
    dbName:str :
    Returns
    -------
    """
    conn, cur = DBConnect(dbName)
    sqlFile = 'database_schema.sql'
    fd = open(sqlFile, 'r')
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(';')

    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as ex:
            print("Command skipped: ", command)
            print(ex)
    conn.commit()
    cur.close()

    return

# preprocess the dataframe
def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
        """
        Parameters
        ----------
        df :
            pd.DataFrame:
        df :
            pd.DataFrame:
        df:pd.DataFrame :
        Returns
        -------
        """
        cols_2_drop = ['Unnamed: 0', 'possibly_sensitive', 'original_text']
        try:
            df = df.drop(columns=cols_2_drop, axis=1)
            df = df.fillna(0)
        except KeyError as e:
            print("Error:", e)

        return df

 #
def insert_to_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    """
    Parameters
    ----------
    dbName :
        str:
    df :
        pd.DataFrame:
    table_name :
        str:
    dbName :
        str:
    df :
        pd.DataFrame:
    table_name :
        str:
    dbName:str :
    df:pd.DataFrame :
    table_name:str :
    Returns
    -------
    """
    conn, cur = DBConnect(dbName)

    df = preprocess_df(df)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} (created_at, 
        source, clean_text, polarity, subjectivity, language,
        favorite_count, retweet_count, original_author, 
        followers_count, friends_count,
        hashtags, user_mentions, place)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (row[0], row[1], row[13], row[2], (row[3]), row[4],(row[5]), row[6], 
                row[7], row[8], row[9], row[10], row[11],row[12])

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            conn.commit()
            print("Data Inserted Successfully")
        except Exception as e:
            conn.rollback()
            print("Error: ", e)
    return
