from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Request/response models
class Query(BaseModel):
    query: str
    
class ResponseBody(BaseModel):
    output: str

# Main query endpoint
@app.post("/user-query")
async def send_query(request: Query):
    n8n_webhook_url = os.getenv("LINK")
    payload = {"query": request.query}

    if n8n_webhook_url is None:
        raise HTTPException(status_code=500, detail="n8n webhook URL not set in environment variables")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(n8n_webhook_url, json=payload)
            response.raise_for_status()
            n8n_response = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error calling n8n webhook: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error decoding n8n response: {str(e)}")

    return {
        "query": request.query,
        "answer": n8n_response.get("answer", "No answer returned from n8n.")
    }

# # receive the output from the llm   
# @app.post("/receive")
# def receive_data(data: ResponseBody):
#     print(data.output)
#     return {"status": "received"}