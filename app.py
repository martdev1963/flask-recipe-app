import requests
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore, credentials

# Using a free service that does not require an API key for immediate use.
# This can be replaced with the Unsplash API key later.
LOREM_PICSUM_URL = "https://picsum.photos/600/400"

# Use the environment variables from the canvas, with fallbacks for local testing.
if '__firebase_config' in locals() or '__firebase_config' in globals():
    firebase_config = json.loads(__firebase_config)
else:
    # A placeholder configuration for local development.
    # IMPORTANT: Replace "YOUR_PRIVATE_KEY_GOES_HERE" with your actual private key from your Firebase service account JSON file.
    firebase_config = {
}


if '__app_id' in locals() or '__app_id' in globals():
    app_id = __app_id
else:
    app_id = "default-app-id"

# The private key must be a valid PEM formatted string. A service account JSON file
# stores it with escaped newlines ('\\n'). We need to replace these to make it a
# valid key for the `credentials.Certificate` function.
private_key_string = firebase_config.get('private_key')
if private_key_string == ""
    raise ValueError("You must replace the placeholder private key with your actual private key from your Firebase service account JSON file.")

if private_key_string:
    firebase_config['private_key'] = private_key_string.replace('\\n', '\n')

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)

# The collection path must be structured as /artifacts/{appId}/users/{userId}/{collectionName}
# to enforce the correct security rules and ensure data is private to each user.
# The user_id is passed from the front end.
RECIPES_COLLECTION_PATH = f'artifacts/{app_id}/users/{{user_id}}/recipes'
RECIPES_COLLECTION = db.collection(RECIPES_COLLECTION_PATH)


def get_image_url(query: str) -> str:
    """Gets a random image URL using the Lorem Picsum service."""
    # The 'query' parameter isn't used for Lorem Picsum as it provides random images,
    # but the function signature remains the same for easy swapping later.
    return LOREM_PICSUM_URL + "?random=1"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recipes', methods=['POST'])
def generate_recipe():
    data = request.json
    prompt = data.get('prompt')
    user_id = data.get('user_id')
    
    if not prompt or not user_id:
        return jsonify({'error': 'Prompt and user ID are required'}), 400

    # Call the recipe generation LLM
    gemini_api_key = "" # The canvas will automatically provide this key.
    llm_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={gemini_api_key}'
    
    llm_payload = {
        'contents': [
            {
                'role': 'user',
                'parts': [
                    {'text': f"Generate a recipe for {prompt}. The recipe should be in JSON format with a 'title', a 'description', a 'prep_time', and a list of 'ingredients'."}
                ]
            }
        ],
        'generationConfig': {
            'responseMimeType': 'application/json'
        }
    }

    try:
        llm_response = requests.post(llm_url, json=llm_payload)
        llm_response.raise_for_status()
        recipe_data = llm_response.json()['candidates'][0]['content']['parts'][0]['text']
        recipe = json.loads(recipe_data)

        # Get an image for the recipe
        image_url = get_image_url(recipe['title'])
        recipe['image_url'] = image_url

        # Save the new recipe to Firestore
        doc_ref = db.collection(RECIPES_COLLECTION_PATH.format(user_id=user_id)).document()
        doc_ref.set(recipe)
        
        recipe['id'] = doc_ref.id
        return jsonify(recipe)

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return jsonify({'error': 'Failed to generate recipe from API'}), 500
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Invalid API response: {e}")
        return jsonify({'error': 'Invalid response from recipe generator'}), 500


@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
        
    try:
        recipes_ref = db.collection(RECIPES_COLLECTION_PATH.format(user_id=user_id))
        docs = recipes_ref.stream()
        recipes = [{'id': doc.id, **doc.to_dict()} for doc in docs]
        return jsonify(recipes)
    except Exception as e:
        print(f"Error fetching recipes: {e}")
        return jsonify({'error': 'Failed to fetch recipes'}), 500


@app.route('/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        doc_ref = db.collection(RECIPES_COLLECTION_PATH.format(user_id=user_id)).document(recipe_id)
        doc_ref.delete()
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Error deleting recipe: {e}")
        return jsonify({'error': 'Failed to delete recipe'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)