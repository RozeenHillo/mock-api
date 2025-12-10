from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/valid")
async def valid_endpoint():
    return JSONResponse(content={"message": "OK - valid request"}, status_code=200)

@app.get("/bad-request")
async def bad_request_endpoint():
    return JSONResponse(content={"error": "Bad Request - invalid input"}, status_code=400)

@app.get("/server-error")
async def server_error_endpoint():
    return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)
