from ctransformers import AutoModelForCausalLM
import gradio as gr
import logging

def main():
    logging.info("Starting main server...")
    
    logging.info("Loading model...")
    # Computer is old with very lousy GPU, hope the CPU version is sufficient
    llm = AutoModelForCausalLM.from_pretrained(
        "TheBloke/Llama-2-7B-Chat-GGUF", 
        model_type="llama", 
        gpu_layers=0)
        
    logging.info("Model loaded.")
        
    def generate(input_text: str, history=[]):
        return llm(input_text)
    
    chatbot = gr.ChatInterface(generate)
    chatbot.launch()

if __name__ == "__main__":
    main()