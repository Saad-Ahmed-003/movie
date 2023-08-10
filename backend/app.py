from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/movies', methods=['GET'])
def get_movies():
    """Returns a list of movies from the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saad$123",
            database="mydatabase"
        )
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor
        cursor.execute("""SELECT
                        name,
                        release_date,
                        genre,
                        image_url,
                        about,
                        actors
                        FROM movies;""")
        movies_data = []
        for movie in cursor:
            movie_data = {
                "Name": movie["name"],
                "date": movie["release_date"],
                "genre": movie["genre"],
                "image": movie["image_url"],
                "about": movie["about"],
                "actors": movie["actors"].split(', ')
            }
            movies_data.append(movie_data)
        connection.close()
        return jsonify(movies_data)
    except mysql.connector.Error as err:
        print(f"Error fetching data from database: {err}")
        return jsonify({"error": "Failed to retrieve data from the database."}), 500
    
if __name__ == "__main__":
    app.run(debug=True)