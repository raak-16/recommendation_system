import pandas as pd
import numpy as np

# Read the dataset
df = pd.read_csv('ssndatd.csv')

# Clean 'Event Name' column by stripping extra spaces
df['Event Name'] = df['Event Name'].str.strip()

# Check for missing or inconsistent event names
print("Missing event names in 'Event Name':", df['Event Name'].isnull().sum())
print("Unique event names:", df['Event Name'].unique())

# Define event names and their corresponding feedback ranges
event_feedback_mapping = {
    "AI in Healthcare Summit": (4, 6),
    "AI for Smart Cities": (3, 6),
    "Tech Entrepreneurship Expo": (1, 4),
    "Space Robotics Symposium": (1, 6),
    "Renewable Energy Innovations Summit": (4, 6),
    "FinTech AI Expo": (4, 6),
    "Advanced Materials Conference": (4, 6),
    "Sustainable Building Design Workshop": (4, 6),
    "5G & IoT Technologies Forum": (4, 6),
    "AI and Cybersecurity Conference": (3, 6),
    "Blockchain for Supply Chain Summit": (3, 6),
    "Smart Manufacturing Expo": (3, 6),
    "Quantum Computing for Business": (3, 5),
    "Autonomous Vehicles Expo": (3, 6),
    "AI for Climate Change Summit": (3, 5)
}

# Iterate through the dictionary and assign random feedback for each event
for event, (low, high) in event_feedback_mapping.items():
    condition = df['Event Name'] == event
    df.loc[condition, 'feedback'] = np.random.randint(low, high, size=condition.sum())

# Check if there are any rows with missing feedback
print(df[df['feedback'].isnull()])
print("Missing feedback count:", df['feedback'].isnull().sum())

# Fill any remaining NaN values in 'feedback' column
#df['feedback'].fillna(3, inplace=True)  # Replace NaNs with a placeholder (-1)

# Verify that all NaN values are filled
print("Remaining NaN values after filling:", df['feedback'].isnull().sum())

# Display a few rows to check the result
#print(df[df['Event Name'] == 'AI & Machine Learning Expo'])
print(df[df['Event Name'] == 'AI for Climate Change Summit'])





df.to_csv("ssnfeedbackaddedcsv.csv")




