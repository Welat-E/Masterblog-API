from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['DELETE'])
def add_posts():
    if "title" in request.json and "content" in request.json:
        new_post = {
            "id": len(POSTS) + 1,  #a new ID gets generated
            "title": request.json["title"],
            "content": request.json["content"]
        }
        POSTS.append(new_post)
        return jsonify(new_post), 201  #201 Created
    else:
        return jsonify({"error": "Title and content are required"}), 400  #400 Bad Request

@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_posts(id):
    for post in POSTS:
        if post['id'] == id:
            del post
        return {"message": "Post with id {post['id']} has been deleted successfully."}
    return jsonify({"error": "Post could not find."}), 404  #404 Bad Request


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update(id):
    for post in POSTS:
        if post['id'] == id:
            data = request.json
            if 'title' in data:
                post['title'] = data['title']
            if 'content' in data:
                post['content'] = data['content']
            return jsonify(post), 200
    return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/search', methods=['GET'])
def search():
    title_query = request.args.get('title', '')
    content_query = request.args.get('content', '')
    
    results = []
    for post in POSTS:
        if title_query.lower() in post['title'].lower() or content_query.lower() in post['content'].lower():
            results.append(post)
    
    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

