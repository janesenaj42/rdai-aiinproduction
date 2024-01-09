import gradio as gr
import requests
from pydantic import BaseModel
import logging
import json
import os

# Docker networking
backend_url = "http://rdai-aiinproducion-backend:8000"

class Query(BaseModel):
    data: str
    
class Response(BaseModel):
    data: str

def main():
    logging.info("Starting main server...")
    
    def generate(input_text: str, history=[]):
        response = requests.post(f"{backend_url}/llm", json=Query(data=input_text).model_dump())
        output = Response.model_validate_json(json.dumps(response.json()))
        return output.data
    
    with gr.Blocks() as demo:
        gr.Markdown("Excited to start talking to me? Please be patient with my response. I'm running on CPU.")
        with gr.Row():
            spongebob = os.path.join(os.path.dirname(__file__), "images/spongebob.jpg")
            llama = os.path.join(os.path.dirname(__file__), "images/llama.jpg")
            image1 = gr.Image(value=spongebob)
            image2 = gr.Image(value=llama)
        chatbot = gr.ChatInterface(generate)

    demo.launch()

if __name__ == "__main__":
    main()