import csv
import mysql.connector
from datetime import datetime

# Connect to the MySQL database using new credentials
db = mysql.connector.connect(
    host="localhost",
    user="newuser",
    passwd="newpassword",  # Replace with your new password
    database="temperature_data"
)
cursor = db.cursor()

# Function to insert data into the database
def insert_into_db(record):
    query = "INSERT INTO temperature_log (timestamp, temperature) VALUES (%s, %s)"
    cursor.execute(query, record)
    db.commit()

# Function to get the maximum timestamp from the database
def get_max_timestamp():
    query = "SELECT MAX(timestamp) FROM temperature_log"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result[0] else datetime.min

# Path to the CSV file (ensure it's accessible)
csv_file_path = '/home/mithun/Desktop/temperature_log.csv'

# Get the maximum timestamp from the database
max_timestamp = get_max_timestamp()

# Load CSV and import data into the database starting from the last timestamp in the database
with open(csv_file_path, 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        # Parse and format the timestamp and temperature correctly
        timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        temperature = float(row[1])
        # Check if the timestamp is greater than the maximum timestamp in the database
        if timestamp > max_timestamp:
            insert_into_db((timestamp, temperature))

# Close the cursor and the database connection
cursor.close()
db.close()

print("Data imported successfully.")
