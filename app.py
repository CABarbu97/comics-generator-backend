from flask import Flask
from app.controllers.comic_controller import comic_blueprint

app = Flask(__name__)

# Register the comic controller
app.register_blueprint(comic_blueprint)

# Any additional app configurations can go here

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Start the Flask application
