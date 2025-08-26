import sqlite3
import json
import pandas as pd

def initialize_database():
    """Initializes the database, creates the recipes table, and populates it with data."""
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    # Create the recipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cuisine TEXT,
            title TEXT,
            rating REAL,
            prep_time INTEGER,
            cook_time INTEGER,
            total_time INTEGER,
            description TEXT,
            nutrients TEXT,
            serves TEXT
        )
    ''')
    conn.commit()

    # Load data from the JSON file
    with open('../US_recipes.json', 'r') as f:
        data = json.load(f)

    # Convert to a pandas DataFrame for easy NaN handling
    df = pd.DataFrame.from_dict(data, orient='index')

    # Convert numeric columns to numeric types and replace NaN with None (NULL in SQL)
    for col in ['rating', 'prep_time', 'cook_time', 'total_time']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].replace({float('nan'): None})

    # Prepare data for insertion
    recipes_to_insert = []
    for _, row in df.iterrows():
        recipes_to_insert.append((
            row['cuisine'],
            row['title'],
            row['rating'],
            row['prep_time'],
            row['cook_time'],
            row['total_time'],
            row['description'],
            json.dumps(row['nutrients']),  # Store nutrients as a JSON string
            row['serves']
        ))

    # Insert data into the table
    cursor.executemany('''
        INSERT INTO recipes (cuisine, title, rating, prep_time, cook_time, total_time, description, nutrients, serves)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', recipes_to_insert)
    conn.commit()
    conn.close()

    print("Database has been initialized and populated with data.")

if __name__ == '__main__':
    initialize_database()