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

@app.route('/privacy', methods=['GET'])
def privacy():
    with open('./privacy_policy.txt', 'r') as file:
        privacy_policy = file.read()
        return privacy_policy

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1206, debug=False)
