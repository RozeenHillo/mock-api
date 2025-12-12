from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
import logging

app = FastAPI(title="Mock API", version="1.0.0")

logger = logging.getLogger("mock-api")
logging.basicConfig(level=logging.INFO)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/mock")
def mock(mode: str = Query(..., description="valid | bad | error")):
    """
    Mock endpoint that simulates:
    - 200 OK      -> mode=valid
    - 400 BadRequest -> mode=bad (or unexpected values)
    - 500 InternalError -> mode=error
    """
    if mode == "valid":
        return {"result": "success", "mode": mode}

    if mode == "bad":
        # Return 400 in a controlled way
        return JSONResponse(
            status_code=400,
            content={"error": "Bad Request", "details": "Malformed or unexpected input"}
        )

    if mode == "error":
        # Simulate an internal server error
        raise RuntimeError("Simulated server failure")

    return JSONResponse(
        status_code=400,
        content={"error": "Bad Request", "details": f"Unsupported mode: {mode}"}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Ensure realistic 500 response payload without exposing stack traces to the client.
    """
    logger.exception("Unhandled error on path=%s: %s", request.url.path, str(exc))
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": "Something went wrong"}
    )
