import pandas as pd
import random
import string

# Please masure you install pandas with the command "pip install pandas" before running this code

# Function to add random characters before '@'
def add_random_chars(email):
    local_part, domain = email.split('@')
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 5)))
    return f"{local_part}{random_chars}@{domain}"

# Load your CSV file
df = pd.read_csv('NiyiTest_original.csv') # Name Of Original csv file exported from postgress db table

# Apply the function to the 'email' column
df['email'] = df['email'].apply(add_random_chars)

# Save the updated DataFrame to a new CSV file
df.to_csv('NiyiTest_modified.csv', index=False) # Name you want to give to the modified csv file