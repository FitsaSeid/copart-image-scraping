# Import libraries (like requiring modules in JS)
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)

# Define a route for the API
@app.route('/scrape', methods=['POST'])
def scrape_vehicles():
    # Get the data from the request (like req.body in JS)
    data = request.json
    vehicles = data.get('vehicles', [])  # Get list of vehicles

    results = []  # Store the results here

    for vehicle in vehicles:
        vehicle_name = vehicle['VehicleName']
        website_url = vehicle['WebsiteURL']

        try:
            # Fetch the webpage (like axios.get in JS)
            response = requests.get(website_url, timeout=10)
            response.raise_for_status()

            # Parse the HTML (like DOMParser in JS)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the first image tag
            img_tag = soup.find('img')  # Find the first <img>
            img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

            # Append the result
            results.append({
                'VehicleName': vehicle_name,
                'WebsiteURL': website_url,
                'ImageURL': img_url
            })

        except Exception as e:
            # Handle errors (e.g., page not found, no images)
            results.append({
                'VehicleName': vehicle_name,
                'WebsiteURL': website_url,
                'ImageURL': None,
                'Error': str(e)
            })

    # Return the results as JSON
    return jsonify(results)

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
