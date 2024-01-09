# rdai-aiinproduction
Code for Red Dragon AI in Production coursework.

Simple Chatbot built with Gradio that runs Llama2 7B on CPU.

Model from https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF.

## Quick Start
```
docker compose up -d

# Check container logs
docker logs -f rdai-aiinproducion
```
You may check the docker logs to see if the model has loaded. The model takes a bit of time to download (around 15 minutes). Please be patient.

Go to http://localhost:7860.

