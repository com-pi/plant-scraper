from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


def value_error_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exception)},
    )

def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )