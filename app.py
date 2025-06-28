from flask import Flask, render_template
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'example'),
            database=os.getenv('MYSQL_DATABASE', 'projekt')
        )
        return connection
    except Error as e:
        print("Database connection failed:", e)
        return None

@app.route("/")
def hello():
    connection = get_db_connection()
    data = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            data = [t[0] for t in tables]
        except Error as e:
            data = [f"Błąd zapytania: {e}"]
        finally:
            cursor.close()
            connection.close()
    else:
        data = ["Brak połączenia z bazą danych"]

    return render_template("index.html", tables=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
