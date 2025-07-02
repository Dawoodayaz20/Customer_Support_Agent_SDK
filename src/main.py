from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.agentsdk import kickoff

app = FastAPI()

# @app.get("/")
# async def health_check():
#     return "The health checkk was successful"

# app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        result = await kickoff(request.question)
        return result.final_output
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}