import mysql.connector

db_config = {
    'host': 'localhost', 
    'user': 'root',  
    'password': 'Vibhav16', 
    'database': 'crypto_prediction'
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
