from main import NotSoFastAPI

def global_middleware(request):
    print("this was executed before any route")

app = NotSoFastAPI(middlewares =[global_middleware])

@app.get("/users")
def get_user(req, res):
    # res.status_code = "200 OK"
    # res.text = "this is response object"
    res.send(status_code= "200 OK", text = "response from get method")

@app.post("/users/{id}")
def post_user(req, res,id):
    # print(id)
    res.send(status_code="200 OK", text = f"response from post method")

