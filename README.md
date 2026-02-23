# 📊 Data Transformer Pro
**Advanced Hierarchical Table-to-JSON Engine with AI-Driven Semantic Analysis**

<img width="1909" height="899" alt="image" src="https://github.com/user-attachments/assets/49b61159-0b29-4300-9870-f07d0c35e18c" />

This project is a high-performance data engineering tool designed to convert messy, irregular Excel and CSV tables into structured, context-aware JSON. It bridges the gap between raw data and AI analysis by implementing sophisticated hierarchical cleaning before LLM processing.

---

## 🏗️ System Architecture & Enhancements
Built with **SOLID** and **Clean Code** principles, the architecture focuses on a "Preprocessing-First" philosophy to ensure data integrity and minimize LLM hallucinations.

### 1. Core Foundations (The "Under the Hood" Upgrades)
* **Hierarchical Cleaning Engine:** A specialized module (`app/hierarchical_cleaner.py`) that handles multi-level/merged headers and irregular row starts through heuristic detection.
* **Client Factory Pattern:** Decouples the UI from the LLM provider, allowing seamless switching between OpenAI-compatible APIs and local Ollama models.
* **Custom Exception Hierarchy:** Implements a robust error handling system (`core/exceptions.py`) to manage table structure failures and API service errors.
* **Template-Based Prompting:** Uses isolated `.txt` prompt files for different analysis modes (Generic vs. Persian-Optimized), enabling easy tuning without modifying the core logic.

---

## 🛠️ Main Features & Services

### 🧬 Hierarchical Header Resolution
* **Dual-Directional ffill:** Automatically resolves merged cells (NaNs in CSV) by filling values horizontally and vertically to reconstruct full-context keys.
* **Linguistic Normalization:** Standardizes local characters (e.g., `۰۱۲۳` to `0123`) and removes Persian thousand separators for accurate statistical processing.

### 💥 Semantic Splitting (Multi-value Explosion)
* **Atomic Record Conversion:** Identifies composite values (e.g., "Girls / Boys") and "explodes" them into separate atomic rows, improving data granularity for downstream tasks.
* **Delimiter Intelligence:** Supports multiple separators like `/`, `,`, `;`, and linguistic conjunctions to handle various table styles.

### 🧠 Context-Rich JSON Generation
* **Statistical Context Injection:** Computes global statistics (Mean, Max, Min) via Pandas and injects them into the AI prompt, allowing the LLM to provide benchmarking narratives.
* **Regex-Based Sanitization:** A robust cleaning layer (`app/llm_json_service.py`) that strips Markdown backticks and conversational fillers to ensure 100% valid JSON parsing.

---

## 💎 UI/UX & Data Features
* **Download Component:** A dedicated `gr.DownloadButton` that generates a physical `transformation_result.json` file only after successful processing.
* **Clean Timer:** A minimal, limit-less progress tracker that accurately measures model inference and data processing speed.

---

## 🚀 How to Run

1.  **Clone the Repo**
2.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Setup Environment:**
    Create a `.env` file and add your `API_KEY`, `BASE_URL`, and `MODEL_NAME`.
4.  **Launch:**
    ```bash
    python main.py
    Running on local URL: http://127.0.0.1:7860
    ```

---

## 🛠️ Tech Stack
* **UI Framework:** Gradio
* **Data Engine:** Pandas & NumPy
* **AI Providers:** OpenAI API & Ollama (Local)
* **File Processing:** OpenPyXL & xlrd (for .xlsx and .xls)
* **Logging:** Python Standard Logging Library
---
