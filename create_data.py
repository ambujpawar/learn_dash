import pandas as pd
import random
from datetime import datetime, timedelta

# Define the number of rows to generate
num_rows = 1000

# Define the column names
columns = ['timestamp', 'temperature', 'humidity']

# Generate data for each row
data = []
start_time = datetime.now()
for i in range(num_rows):
    timestamp = start_time + timedelta(minutes=i)
    temperature = random.uniform(20, 30)
    humidity = random.uniform(40, 60)
    data.append([timestamp, temperature, humidity])

# Create a pandas DataFrame from the data
df = pd.DataFrame(data, columns=columns)

# Write the data to a CSV file
filename = '/Users/ambujpawar/Desktop/GithubProjects/learn_dash/data.csv'  # Replace with your desired file path
df.to_csv(filename, index=False)

print(f"CSV file '{filename}' created successfully!")
