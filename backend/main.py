from ctransformers import AutoModelForCausalLM
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging

class Query(BaseModel):
    data: str
    
class Response(BaseModel):
    data: str

logging.info("Loading model...")
# Computer is old with very lousy GPU, hope the CPU version is sufficient
#llm = AutoModelForCausalLM.from_pretrained(
#    "TheBloke/Llama-2-7B-Chat-GGUF",
    #model_file="llama-2-7b-chat.Q2_K.gguf",
#    model_type="llama", 
#    gpu_layers=0)   
logging.info("Model loaded.")

app = FastAPI()

@app.post("/llm")
async def query_llm(query: Query):
    logging.info(f"Received query: {query.data}")
    #response = Response(data=llm(query.data))
    response = Response(data='Hello there ' + query.data)
    logging.info(f"Responding with: {response.data}")
    return response
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
