from flask import Blueprint, request, jsonify
from app.services.comic_service import ComicService

# Create a blueprint for the comic routes
comic_blueprint = Blueprint('comic', __name__)

# Instance of ComicService
comic_service = ComicService()

# POST route to generate comic
@comic_blueprint.route('/generate_comic', methods=['POST'])
def generate_comic():
    try:
        # Get environment and characters from the request body
        data = request.json
        environment = data.get('environment', '')
        characters = data.get('characters', '')

        # Generate comic image URL via the service
        image_url = comic_service.create_comic(environment, characters)

        if image_url:
            return jsonify({"image_url": image_url}), 200
        else:
            return jsonify({"error": "Failed to generate comic."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
