# from fastapi import FastAPI

# app = FastAPI()

# # This is the main file for our FastAPI application. We will define our routes and logic here.
# @app.get("/")
# def home():
#     return {
#         "message": "Welcome to AI Engineering"
#     }

# # This route will return some information about Tanveer when accessed.
# @app.get("/about")
# def about():
#     return {
#         "name": "Tanveer",
#         "goal": "AI Engineer"
#     }

# # This route will greet the user by their name. The name will be passed as a query parameter.
# @app.get("/greet")
# def greet(name: str):
#     return {
#         "message": f"Hello {name}"
#     }

from fastapi import FastAPI

app = FastAPI()

@app.get("/student")

def student():
    return {
     "name": "Tanveer",
     "country": "Bangladesh",
     "goal": "Generative AI Engineer"
}


@app.get("/welcome")

def welcome(name : str):
    return {
        "message": f"Welcome {name}"
    }
