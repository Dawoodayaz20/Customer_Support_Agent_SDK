from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def health_check():
    return "The health checkk was successful"