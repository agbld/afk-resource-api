from flask import Flask, request, jsonify
from api import get_character_info, get_character_list

app = Flask(__name__)

@app.route('/api/characters', methods=['GET'])
def api_get_character_list():
    characters = get_character_list()
    return jsonify({'characters': characters})

@app.route('/api/character/<string:character_name>', methods=['GET'])
def api_get_character_info(character_name):
    info = get_character_info(character_name)
    return jsonify({'character_name': character_name, 'info': info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
