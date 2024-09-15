from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
    
        all_text = soup.get_text(separator='\n')

        # Extract image links
        image_links = [img['src'] for img in soup.find_all('img')]

        # Extract text from <document> tag
        document_tag = soup.find('document')
        if document_tag:
            list_items = document_tag.find_all('b')
            extracted_text = '\n\n'.join([li.get_text(strip=True) for li in list_items])
        else:
            extracted_text = "No <document> tag found."
        
        return image_links, extracted_text
    else:
        raise Exception(f"Failed to retrieve the page: {response.status_code}")

@app.route('/image_links', methods=['GET'])
def get_image_links():
    url = request.args.get('url')
    if url:
        try:
            image_links, _ = fetch_data(url)
            return jsonify({"image_links": image_links})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "URL parameter is required"}), 400

@app.route('/extracted_text', methods=['GET'])
def get_extracted_text():
    url = request.args.get('url')
    if url:
        try:
            _, extracted_text = fetch_data(url)
            return jsonify({"extracted_text": extracted_text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "URL parameter is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)
﻿
