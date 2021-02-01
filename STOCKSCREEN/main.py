from fastapi import FastAPI, Request
# FastAPI is a framework to create apis and web apps
from fastapi.templating import Jinja2Templates

app = FastAPI()

# look for templates in the templates directory
templates = Jinja2Templates(directory="templates") 

@app.get("/") # you can test in the browser
def home(request: Request):
    """
        Displays the stock screener dashboard / homepage
    """
    return templates.TemplateResponse("home.html", {
        "request": request,
    })

@app.post("/stock") # you need to test in a client like Postman or Insominia
def create_stock():
    """
        Creates a sstock and stores it in the database
    """
    return {
        "code": "success",
        "message": "stock"
    }
