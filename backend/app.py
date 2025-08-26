import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This allows your React frontend to communicate with the API

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row  # This allows fetching rows as dictionaries
    return conn

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """
    Endpoint to get all recipes with pagination and sorting.
    Query parameters: page (int), limit (int)
    """
    conn = get_db_connection()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    # Count total number of recipes for pagination
    total_recipes = conn.execute('SELECT COUNT(*) FROM recipes').fetchone()[0]

    # Fetch recipes, sorted by rating in descending order.
    # We use COALESCE to put NULL ratings at the end.
    recipes = conn.execute(
        'SELECT * FROM recipes ORDER BY rating DESC NULLS LAST LIMIT ? OFFSET ?',
        (limit, offset)
    ).fetchall()
    conn.close()

    data = [dict(recipe) for recipe in recipes]
    for recipe in data:
        recipe['nutrients'] = json.loads(recipe['nutrients'])
        
    return jsonify({
        'page': page,
        'limit': limit,
        'total': total_recipes,
        'data': data
    })

@app.route('/api/recipes/search', methods=['GET'])
def search_recipes():
    """
    Endpoint to search recipes with various filters.
    Query parameters: title, cuisine, calories, total_time, rating
    """
    conn = get_db_connection()
    query_params = request.args

    conditions = []
    args = []

    # Filter by title (partial match, case-insensitive)
    if 'title' in query_params:
        conditions.append('title LIKE ?')
        args.append(f'%{query_params["title"]}%')
    
    # Filter by cuisine (exact match, case-insensitive)
    if 'cuisine' in query_params:
        conditions.append('LOWER(cuisine) = LOWER(?)')
        args.append(query_params["cuisine"])

    # Filter by numeric fields (calories, total_time, rating)
    for param in ['calories', 'total_time', 'rating']:
        if param in query_params:
            value_with_op = query_params[param]
            if '<=' in value_with_op:
                op = '<='
                value = value_with_op.replace('<=', '')
            elif '>=' in value_with_op:
                op = '>='
                value = value_with_op.replace('>=', '')
            elif '=' in value_with_op:
                op = '='
                value = value_with_op.replace('=', '')
            else:
                op = '='
                value = value_with_op
            
            # The nutrients JSON is stored as a string, so we need to search within it
            if param == 'calories':
                conditions.append("json_extract(nutrients, '$.calories') " + op + " ?")
                args.append(f"{value} kcal")
            else:
                conditions.append(f"{param} {op} ?")
                args.append(value)

    where_clause = ' AND '.join(conditions)
    
    if where_clause:
        sql_query = f'SELECT * FROM recipes WHERE {where_clause}'
    else:
        sql_query = 'SELECT * FROM recipes'

    recipes = conn.execute(sql_query, args).fetchall()
    conn.close()

    data = [dict(recipe) for recipe in recipes]
    for recipe in data:
        recipe['nutrients'] = json.loads(recipe['nutrients'])

    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True)