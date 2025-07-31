import base64
from datetime import datetime
from typing import List

from botocore import auth
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

app = FastAPI()

class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

posts: List[PostModel] = []

def serialized_posts():
    serialized_post_created = []
    for post in posts:
        serialized_post_created.append(post.model_dump())
    return serialized_post_created


@app.get("/ping")
def ping():
    return Response(content="pong", status_code=200)

@app.get("/welcome")
def welcome():
    with open("home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
        return Response(content=html_content, status_code=200, media_type="text/html")


app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("not_found.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")

@app.post("/posts")
def new_posts(posts_to_add: List[PostModel]):
    posts.extend(posts_to_add)
    return JSONResponse({"posts": serialized_posts()}, status_code=201)

@app.get("/posts")
def list_posts():
    return JSONResponse({"posts": serialized_posts()}, status_code=200)

@app.put("/posts")
def add_or_update_posts(update_posts: List[PostModel]):
    global posts
    for new_post in update_posts:
        found = False
        for i, old_post in enumerate(posts):
            if new_post.title == old_post.title:
                found = True
                posts[i] = new_post
                break
            if not found:
                posts.append(new_post)
    return JSONResponse({"posts": serialized_posts()}, status_code=200)

app.get('/ping/auth')
def ping_auth():
    def check_basic_auth(request: Request):
        auth = request.headers.get('Authorization')
    if not auth:
        return False
    method, credentials = auth.split(' ', 1)
    if method.lower() != 'basic':
        return False

    decoded_credentials = base64.b64decode(credentials).decode('utf-8')
    username, password = decoded_credentials.split(':', 1)
    return username == 'admin' and password == '123456'
    if not check_basic_auth(request):
        return Response('Accès non autorisé',status=401,mimetype='text/plain')
    return JSONResponse("Athentifié", status_code=200)



