# app.py
from notsofastapi import NotSoFastAPI

# Create your app
app = NotSoFastAPI()

# --- Define a simple GET route ---
@app.get("/")
def home(request, response):
    response.send("<h1>Hello from NotSoFastAPI!</h1><p>Try <a href='/user/123'>/user/123</a></p>", "200 OK")
    response.headers.append(("Content-Type", "text/html"))

# --- Dynamic route with path parameter ---
@app.get("/user/{user_id}")
def get_user(request, response, user_id):
    response.send({
        "user_id": int(user_id),
        "name": f"User {user_id}",
        "endpoint": f"GET /user/{user_id}"
    })

# --- POST route that reads JSON body ---
@app.post("/echo")
def echo(request, response):
    # Request body is auto-parsed into request.body (if JSON)
    response.json({
        "message": "Here's what you sent",
        "data": request.body,
        "queries": dict(request.queries)
    })

# --- Class-based view ---
@app.route("/api")
class API:
    def GET(request, response):
        response.send({"status": "API is running"})

    def POST(request, response):
        response.send({
            "received": request.body,
            "method": "POST to /api"
        })

