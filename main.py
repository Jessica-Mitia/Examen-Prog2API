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

