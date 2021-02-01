from fastapi import FastAPI
# FastAPI is a framework to create apis and web apps

app = FastAPI()

@app.get("/") # you can test in the browser
def dashboard():
    """
        Displays the stock screener dashboard / homepage
    """
    return {"Dashboard": "Home Page"}

@app.post("/stock") # you need to test in a client like Postman or Insominia
def create_stock():
    """
        Creates a sstock and stores it in the database
    """
    return {
        "code": "success",
        "message": "stock"
    }
