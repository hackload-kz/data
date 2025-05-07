# before running this script, make sure to install the required libraries:
# python3 -m pip install pandas numpy
# This script generates a large dataset of user information for a ticketing system.
# It creates a CSV file and an SQL script to insert the data into a database.
# The dataset includes user IDs, emails, hashed passwords, names, birthdays, registration dates,
# active status, and last login dates.

import random
import string
import hashlib
import csv
import datetime
import numpy as np
import pandas as pd

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Number of users to generate
NUM_USERS = 1000000

# Domain names for emails
DOMAINS = ['cool.ti', 'grab.coffee', 'hackhload.kz', 'ticket.world', 'event.me', 
           'quick.pass', 'show.go', 'concert.fun', 'fest.tix', 'live.now']

# Read first names and last names from CSV files
first_names_df = pd.read_csv('first_names.csv')
last_names_df = pd.read_csv('last_names.csv')

# Separate names by gender
male_first_names = first_names_df[first_names_df['Sex'] == 'M']
female_first_names = first_names_df[first_names_df['Sex'] == 'F']
male_last_names = last_names_df[last_names_df['Sex'] == 'M']
female_last_names = last_names_df[last_names_df['Sex'] == 'F']

# Function to capitalize the first letter and lowercase the rest
def format_name(name):
    if not name:
        return name
    return name[0].upper() + name[1:].lower()

# Function to generate a user's first name, last name, and email consistent by gender
def generate_name_and_email(user_id):
    # Determine gender
    gender = 'M' if random.random() < 0.5 else 'F'
    
    if gender == 'M':
        # Select a random male name
        first_name_row = male_first_names.sample(1).iloc[0]
        last_name_row = male_last_names.sample(1).iloc[0]
    else:
        # Select a random female name
        first_name_row = female_first_names.sample(1).iloc[0]
        last_name_row = female_last_names.sample(1).iloc[0]
    
    # Get the appropriate name versions
    first_name_kz = first_name_row['NameKZ']
    first_name_en = first_name_row['NameEn']
    last_name_kz = last_name_row['NameKZ']
    last_name_en = last_name_row['NameEn']
    
    # Format the KZ names
    formatted_first_name = format_name(first_name_kz)
    formatted_last_name = format_name(last_name_kz)
    
    # Generate email using English names
    email = f"{first_name_en.lower()}_{last_name_en.lower()}_{user_id}@{random.choice(DOMAINS)}"
    
    return formatted_first_name, formatted_last_name, email, gender

# Function to generate a password and its hash
def generate_password():
    # Generate a random password
    length = random.randint(8, 16)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    
    # Hash the password
    hashed = hashlib.sha256(password.encode()).hexdigest()
    
    return password, hashed

# Function to generate a birthdate (or None with 30% probability)
def generate_birthdate():
    if random.random() < 0.3:  # 30% chance of None
        return None
    
    # Calculate date range for ages 13-65
    today = datetime.datetime.now()
    min_date = today - datetime.timedelta(days=65*365)
    max_date = today - datetime.timedelta(days=13*365)
    
    # Generate random date within range
    days_range = (max_date - min_date).days
    random_days = random.randint(0, days_range)
    return min_date + datetime.timedelta(days=random_days)

# Function to generate registration date
def generate_registration_date():
    # Registration between 1 and 5 years ago
    now = datetime.datetime.now()
    days_ago = random.randint(1, 5*365)
    return now - datetime.timedelta(days=days_ago)

# Function to generate last login date (after registration)
def generate_last_login(registration_date):
    now = datetime.datetime.now()
    # Last login between registration and now
    days_since_reg = (now - registration_date).days
    if days_since_reg <= 0:
        days_since_reg = 1
    days_after_reg = random.randint(0, days_since_reg)
    return registration_date + datetime.timedelta(days=days_after_reg)

# Generate CSV file
def generate_csv():
    with open('users.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['user_id', 'email', 'password_hash', 'password_plain', 'first_name', 
                     'surname', 'birthday', 'registered_at', 'is_active', 'last_logged_in']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for user_id in range(1, NUM_USERS + 1):
            if user_id % 10000 == 0:  # Progress indicator
                print(f"Generating user {user_id}/{NUM_USERS}")
            
            # Generate user data
            first_name, surname, email, _ = generate_name_and_email(user_id)
            password_plain, password_hash = generate_password()
            birthday = generate_birthdate()
            registered_at = generate_registration_date()
            is_active = random.random() < 0.8  # 80% chance of being active
            last_logged_in = generate_last_login(registered_at)
            
            # Write to CSV
            writer.writerow({
                'user_id': user_id,
                'email': email,
                'password_hash': password_hash,
                'password_plain': password_plain,
                'first_name': first_name,
                'surname': surname,
                'birthday': birthday.strftime('%Y-%m-%d') if birthday else None,
                'registered_at': registered_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_active': is_active,
                'last_logged_in': last_logged_in.strftime('%Y-%m-%d %H:%M:%S')
            })

# Generate SQL script
def generate_sql():
    with open('users.sql', 'w', encoding='utf-8') as sqlfile:
        # Write SQL table creation
        sqlfile.write("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    password_plain VARCHAR(255),  -- For testing purposes only, would not exist in production
    first_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    birthday DATE,
    registered_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL,
    last_logged_in TIMESTAMP NOT NULL
);

-- Insert data
BEGIN TRANSACTION;
""")
        
        # Process in batches to avoid memory issues
        batch_size = 1000
        total_batches = NUM_USERS // batch_size
        
        for batch in range(total_batches):
            start_id = batch * batch_size + 1
            end_id = (batch + 1) * batch_size
            
            if batch % 10 == 0:  # Progress indicator
                print(f"Generating SQL batch {batch+1}/{total_batches}")
            
            batch_values = []
            for user_id in range(start_id, end_id + 1):
                # Generate user data (same as CSV function)
                first_name, surname, email, _ = generate_name_and_email(user_id)
                password_plain, password_hash = generate_password()
                birthday = generate_birthdate()
                registered_at = generate_registration_date()
                is_active = random.random() < 0.8
                last_logged_in = generate_last_login(registered_at)
                
                # Format SQL values - escape single quotes in names and other strings
                first_name_sql = first_name.replace("'", "''")
                surname_sql = surname.replace("'", "''")
                email_sql = email.replace("'", "''")
                password_plain_sql = password_plain.replace("'", "''")
                
                birth_sql = f"'{birthday.strftime('%Y-%m-%d')}'" if birthday else "NULL"
                is_active_sql = "TRUE" if is_active else "FALSE"
                
                value = f"({user_id}, '{email_sql}', '{password_hash}', '{password_plain_sql}', '{first_name_sql}', '{surname_sql}', {birth_sql}, '{registered_at.strftime('%Y-%m-%d %H:%M:%S')}', {is_active_sql}, '{last_logged_in.strftime('%Y-%m-%d %H:%M:%S')}')"
                batch_values.append(value)
            
            # Write batch insert
            sqlfile.write("INSERT INTO users (user_id, email, password_hash, password_plain, first_name, surname, birthday, registered_at, is_active, last_logged_in) VALUES\n")
            sqlfile.write(",\n".join(batch_values))
            sqlfile.write(";\n")
        
        # Close transaction
        sqlfile.write("\nCOMMIT;\n")

if __name__ == "__main__":
    print("Generating user data...")
    print("Generating CSV file...")
    generate_csv()
    print("Generating SQL file...")
    generate_sql()
    print("Done!")