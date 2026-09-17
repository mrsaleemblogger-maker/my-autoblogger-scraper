from flask import Flask, request, jsonify
from googlesearch import search
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/')
def home():
    return "AutoBlogger Scraper API is Running Successfully!"

@app.route('/scrape', methods=['GET'])
def scrape_data():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Please provide query ?q="}), 400

    try:
        # 1. Google Web Search (Title, URL, Snippet)
        web_results = []
        for res in search(query, num_results=6, advanced=True):
            web_results.append({
                "title": res.title,
                "link": res.url,
                "description": res.description
            })

        # 2. DuckDuckGo High-Res Images (Bypasses all Google Captchas)
        image_results = []
        with DDGS() as ddgs:
            images = list(ddgs.images(query, max_results=5))
            for img in images:
                if 'image' in img:
                    image_results.append(img['image'])

        return jsonify({
            "status": "success",
            "web_results": web_results,
            "image_results": image_results
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
