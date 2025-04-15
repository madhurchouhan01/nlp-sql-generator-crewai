from crewai.tools import tool
import mysql.connector
@tool("Query Executer")
def query_executer(sql_query: str) -> str:
    """Executes the given SQL query and returns the result as a plain string."""

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="employee"
    )
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return str(result)
    except Exception as e:
        return f"Error executing query: {e}"
    finally:
        cursor.close()
        conn.close()
