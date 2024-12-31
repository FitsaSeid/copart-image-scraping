from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import random
import time

app = Flask(__name__)

def scrape_vehicle_image(url):
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=False)  # Set headless=True for production
            page = browser.new_page()

            # Set headers to mimic a real browser
            USER_AGENTS = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            ]
            page.set_extra_http_headers({
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.google.com/",
                "DNT": "1",
                "Connection": "keep-alive",
            })

            # Navigate to the URL
            page.goto(url)

            # Add delay and scrolling
            print("Scrolling to load lazy images...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to bottom
            page.wait_for_timeout(5000)  # Wait 5 seconds

            # Capture the HTML and screenshot
            print("Capturing debugging information...")
            html_content = page.content()
            # print("HTML Content:")
            # print(html_content)
            page.screenshot(path="debug.png")
            print("Screenshot saved as debug.png")

            # Attempt to find the image
            img_tag = page.query_selector("div.p-image-container-box img")

            # Fallback to searching all <img> tags if specific selector fails
            if not img_tag:
                print("Specific selector not found. Searching all <img> tags.")
                img_tags = page.query_selector_all("img")
                for img in img_tags:
                    src = img.get_attribute("src")
                    if src and "copart" in src:  # Look for Copart-related images
                        img_tag = img
                        break

            # Extract image URL
            img_url = img_tag.get_attribute("src") if img_tag else None

            # Close the browser
            browser.close()
            return img_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/scrape-image', methods=['POST'])
def scrape_image():
    try:
        data = request.json
        website_url = data.get("WebsiteURL")

        if not website_url:
            return jsonify({"error": "WebsiteURL is required"}), 400

        # Scrape the image
        image_url = scrape_vehicle_image(website_url)

        if image_url:
            return jsonify({"VehicleImage": image_url})
        else:
            return jsonify({"error": "No image found"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=False)
