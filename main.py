from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/hello")
def read_hello(request: Request, is_teacher: bool = None, name: str = "Non défini"):
    accept_headers = request.headers.get("Accept")
    if accept_headers != "text/plain":
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
    if name == "Non défini" and is_teacher is None:
        return JSONResponse({"message": "Hello world"}, status_code=200)
    if is_teacher is None:
        is_teacher = False
    if is_teacher:
        return JSONResponse({"message": f"Hello teacher {name}"}, status_code=200)
    else:
        return JSONResponse({"message": f"Hello {name}"}, status_code=200)


class WelcomeRequest(BaseModel):
    name: str


@app.post("/welcome")
def welcome_user(request: WelcomeRequest):
    return {f"Bienvenue {request.name}"}


class SecretPayload(BaseModel):
    secret_code: int


@app.put("/top-secret")
def put_top_secret(request: Request, request_body: SecretPayload):
    auth_header = request.headers.get("Authorization")
    if auth_header != "my-secret-key":
        return JSONResponse(
            status_code=403,
            content={"error": f"Unauthorized header received: {auth_header}"}
        )

    secret_code = request_body.secret_code
    code_length = len(str(secret_code))
    if code_length != 4:
        return JSONResponse(
            status_code=400,
            content={"error": f"Le code fourni n’est pas à 4 chiffres mais {code_length} chiffres."}
        )

    return JSONResponse(content={"message": f"Voici le code {secret_code}"}, status_code=200)
