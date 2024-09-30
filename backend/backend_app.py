from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """Retrieve the list of posts."""
    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_posts():
    """Add a new post to the list."""
    if "title" in request.json and "content" in request.json:
        new_post = {
            "id": len(POSTS) + 1,  # generate a new ID
            "title": request.json["title"],
            "content": request.json["content"],
        }
        POSTS.append(new_post)
        return jsonify(new_post), 201
    else:
        return jsonify({"error": "Title and content are required"}), 400


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_posts(id):
    """Delete a post by ID."""
    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return {"message": f"Post with id {post['id']} has been deleted."}
    return jsonify({"error": "Post not found."}), 404


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update(id):
    """Update an existing post by ID."""
    for post in POSTS:
        if post["id"] == id:
            data = request.json
            if "title" in data:
                post["title"] = data["title"]
            if "content" in data:
                post["content"] = data["content"]
            return jsonify(post), 200
    return jsonify({"error": "Post not found"}), 404


@app.route("/api/posts/search", methods=["GET"])
def search():
    """Search for posts by title or content."""
    title_query = request.args.get("title", "").lower()  # lowercase for comparison
    content_query = request.args.get("content", "").lower()

    results = []
    for post in POSTS:
        title_matches = title_query in post["title"].lower() if title_query else False
        content_matches = (
            content_query in post["content"].lower() if content_query else False
        )

        if title_matches or content_matches:
            results.append(post)

    if not results:
        return jsonify({"error": "No posts found."}), 404

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
