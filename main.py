# main.py
import os
import json
import gradio as gr
from app.hierarchical_cleaner import HierarchicalCleaner
from app.llm_json_service import LLMJsonEngine
from infra.factory import ClientFactory
from core.logger import logger

# Absolute path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_DIR = os.path.join(BASE_DIR, "app", "prompts")
OUTPUT_FILE = os.path.join(BASE_DIR, "transformation_result.json")

def process(file_obj, provider, model_name, template_choice):
    """
    Core logic to handle table transformation.
    """
    try:
        if not file_obj: 
            return None, gr.update(visible=False)
        
        # 1. Load the specific prompt template
        prompt_path = os.path.join(PROMPT_DIR, f"{template_choice}.txt")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Template {template_choice} missing.")

        # 2. Advanced Pre-processing (Hierarchical & Semantic)
        cleaner = HierarchicalCleaner(file_obj.name)
        df = cleaner.get_clean_dataframe()
        
        # 3. AI Orchestration
        client = ClientFactory.get_client(provider, model_name)
        engine = LLMJsonEngine(client)
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
            
        json_str = engine.generate(df, template)
        
        # 4. JSON Validation and Saving
        json_data = json.loads(json_str)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            
        # Return result for the viewer and the path for the download button
        return json_data, gr.update(value=OUTPUT_FILE, visible=True)
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return {"error": str(e)}, gr.update(visible=False)

# UI with Soft Blue Theme
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), title="Data Transformer Pro") as demo:
    gr.Markdown("# 🚀 Data Transformer Pro\n### Professional Hierarchical Table-to-JSON Pipeline")
    
    with gr.Row():
        # Input Section
        with gr.Column(scale=1):
            f_in = gr.File(label="Step 1: Upload Table (.csv, .xlsx, .xls)")
            prov = gr.Dropdown(["OpenAI", "Ollama"], value="Ollama", label="AI Provider")
            mod = gr.Dropdown(["gemma3:4b", "llama3.1:8b"], value="gemma3:4b", label="Local Model")
            temp_in = gr.Dropdown(["generic_json", "persian_json"], value="generic_json", label="Analysis Mode")
            
            btn = gr.Button("Transform & Analyze", variant="primary")
            
            # Professional Download Button (Hidden by default)
            download_btn = gr.DownloadButton("📥 Download JSON Result", visible=False)
            
        # Output Section
        with gr.Column(scale=2):
            f_out = gr.JSON(label="Structured Insight Result")

    # Event Chaining Logic
    # 1. First, clear the previous result to make the UI look responsive
    # 2. Then, run the long processing function
    btn.click(
        fn=lambda: (None, gr.update(visible=False)), 
        outputs=[f_out, download_btn]
    ).then(
        fn=process, 
        inputs=[f_in, prov, mod, temp_in], 
        outputs=[f_out, download_btn], 
        show_progress="minimal"
    )

if __name__ == "__main__":
    logger.info("Application initialized with Soft Blue theme.")
    demo.launch()