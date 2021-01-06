import sqlite3

DB_NAME = "data/puppy_activity.db"

def reset_table():
    try:
        sqliteConnection = sqlite3.connect(DB_NAME)
        sqlite_drop_table_query = "DROP TABLE IF EXISTS activities;"
        sqlite_create_table_query = '''
        CREATE TABLE activities (
        timestamp datetime NOT NULL,
        activity TEXT NOT NULL);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_drop_table_query)
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def insert_activity(activity):
    query = "INSERT INTO activities (timestamp, activity) VALUES (?, ?)"
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(query, (activity['timestamp'], activity['activity']))
        conn.commit()

def fetch_all_activities():
    query = "SELECT * FROM activities"
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

    return rows

def fetch_most_recent_activity():
    query = "SELECT activity, max(timestamp) from activities group by activity"
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

    most_recent = {r[0]: r[1] for r in rows}
    return most_recent

if __name__ == "__main__":
    reset_table()