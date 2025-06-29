from flask import Flask, render_template
import mysql.connector
import os
import time
#Testowy Commit na potrzeby Dokumentacji :D
app = Flask(__name__)

def get_db_connection(retries=5, delay=3):
    for i in range(retries):
        try:
            conn = mysql.connector.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASSWORD", ""),
                database=os.environ.get("DB_NAME", "")
            )
            return conn
        except mysql.connector.Error as e:
            print(f"Database connection  failed (attempt {i+1}/{retries}): {e}")
            time.sleep(delay)
    return None

@app.route('/')
def home():
    conn = get_db_connection()
    users = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"Query failed: {e}")
        finally:
            conn.close()
    else:
        print("Brak połączenia z bazą danych.")
    return render_template("index.html", users=users)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
