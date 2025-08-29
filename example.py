from main import NotSoFastAPI

def global_middleware(request):
    print("this was executed before any route")

app = NotSoFastAPI(middlewares =[global_middleware])

@app.get("/users")
def get_user(req, res):
    res.send(status_code= "200 OK", text = "response from get method")

def route_middleware(request):
    print("running route middleware")
@app.post("/users/{id}", middlewares = [route_middleware])
def post_user(req, res,id):
    res.send(status_code="200 OK", text = f"response from post method")

@app.route()
class User:

    def __init__(self):
        pass
    
    def get(req, res):
        res.send("hi aniket i am from class", "200 OK")

    def post(req, res):
        res.send("this is post method of class")
        
    def hello(self):
        pass