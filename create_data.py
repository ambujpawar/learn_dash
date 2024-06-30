import pandas as pd
import random
from datetime import datetime, timedelta

# Define the number of rows to generate
num_rows = 1000

# Define the column names
columns = ['timestamp', 'temperature', 'humidity', 'label']

# Generate data for each row
data = []
start_time = datetime.now()
for i in range(num_rows):
    timestamp = start_time + timedelta(minutes=i)
    # Center temperature at 30 with minor anomalies
    if i % 50 == 0:  # Introduce an anomaly every 50 rows
        temperature = random.uniform(25, 35)
    else:
        temperature = random.uniform(29, 31)
    # Center humidity at 45 with minor anomalies
    if i % 50 == 0:  # Introduce an anomaly every 50 rows
        humidity = random.uniform(40, 50)
    else:
        humidity = random.uniform(44, 46)
    label = 0
    data.append([timestamp, temperature, humidity, label])

# Create a pandas DataFrame from the data
df = pd.DataFrame(data, columns=columns)

# Write the data to a CSV file
filename = '/Users/ambujpawar/Desktop/GithubProjects/learn_dash/data.csv'  # Replace with your desired file path
df.to_csv(filename, index=False)

print(f"CSV file '{filename}' created successfully!")