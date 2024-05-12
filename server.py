from flask import Flask, request, jsonify, send_from_directory, send_file
import os

app = Flask(__name__)

# Serve the HTML file


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Optional: Handle favicon.ico requests to avoid 404 in logs


@app.route('/favicon.ico')
def favicon():
    # If you have a favicon.ico, you can return it with:
    # return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    # Or, to simply avoid 404 errors without a real favicon:
    return ('', 204)

# Endpoint to receive coordinates


@app.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    data = request.json
    # save the coordinates to a file name coordinates.txt
    with open('coordinates.txt', 'w') as file:
        file.write(f"{data['lat']}, {data['lng']}\n")
    print(
        f"Coordinates received: Latitude {data['lat']}, Longitude {data['lng']}")
    return jsonify({'status': 'success', 'message': 'Coordinates saved'})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
