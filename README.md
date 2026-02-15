# Knowledge Graph Generator

A Streamlit application that extracts graph data (entities and relationships) from text input using LangChain and various LLM providers (OpenAI, Ollama, Anthropic, Google), and generates interactive graphs.

**Now supports multiple LLM providers - use it without OpenAI API!**

![CleanShot 2025-05-28 at 13 11 46](https://github.com/user-attachments/assets/4fef9158-8dd8-432d-bb8a-b53953a82c6c)

👉 This repo is part of my project tutorial on Youtube:
[![](https://img.youtube.com/vi/O-T_6KOXML4/0.jpg)](https://www.youtube.com/watch?v=O-T_6KOXML4)

## Features

- **Multiple LLM Provider Support**: Choose from OpenAI, Ollama (local), Anthropic Claude, or Google Gemini
- Two input methods: text upload (.txt files) or direct text input
- Interactive knowledge graph visualization
- Customizable graph display with physics-based layout
- Entity relationship extraction powered by advanced language models
- **Free option available**: Use Ollama locally without any API costs!

## Installation

### Prerequisites

- Python 3.8 or higher
- **One of the following** (depending on your preferred LLM provider):
  - OpenAI API key (for GPT models)
  - Ollama installed locally (for free, local models) - [Install Ollama](https://ollama.ai)
  - Anthropic API key (for Claude models)
  - Google API key (for Gemini models)

### Dependencies

The application requires the following Python packages:

**Core dependencies:**
- langchain (>= 0.1.0): Core LLM framework
- langchain-experimental (>= 0.0.45): Experimental LangChain features
- python-dotenv (>= 1.0.0): Environment variable support
- pyvis (>= 0.3.2): Graph visualization
- streamlit (>= 1.32.0): Web UI framework

**LLM Provider dependencies** (install based on your choice):
- langchain-openai (>= 0.1.0): For OpenAI GPT models
- langchain-ollama (>= 0.1.0): For Ollama local models
- langchain-anthropic (>= 0.1.0): For Anthropic Claude models
- langchain-google-genai (>= 0.0.11): For Google Gemini models

Install all dependencies using the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

### Setup

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd knowledge_graph_app_2
   ```

   Note: Replace `[repository-url]` with the actual URL of this repository.

2. Create a `.env` file in the root directory with your API key(s):

   **For OpenAI (GPT models):**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   **For Ollama (Local - No API key needed!):**
   ```
   # No API key required! Just install Ollama and run: ollama pull llama2
   OLLAMA_BASE_URL=http://localhost:11434  # Optional, this is the default
   ```

   **For Anthropic (Claude models):**
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

   **For Google (Gemini models):**
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

   You only need to configure the API key(s) for the provider(s) you want to use.

## Running the Application

### For Ollama (Free, Local Option)

If you want to use Ollama (no API costs!):

1. Install Ollama from [https://ollama.ai](https://ollama.ai)
2. Pull a model (e.g., llama2):
   ```bash
   ollama pull llama2
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. In the app, select "Ollama (Local)" from the LLM provider dropdown

### For Other Providers

To run the Streamlit app with any provider:

```bash
streamlit run app.py
```

This will start the application and open it in your default web browser (typically at http://localhost:8501).

## Usage

1. **Select LLM Provider**: Choose your preferred provider from the sidebar dropdown (OpenAI, Ollama, Anthropic, or Google)
2. **Select Model**: Choose the specific model you want to use
3. **Choose Input Method**: Select from the sidebar (Upload txt or Input text)
4. If uploading a file, select a .txt file from your computer
5. If using direct input, type or paste your text into the text area
6. Click the "Generate Knowledge Graph" button
7. Wait for the graph to be generated (this may take a few moments depending on the length of the text and the provider)
8. Explore the interactive knowledge graph:
   - Drag nodes to rearrange the graph
   - Hover over nodes and edges to see additional information
   - Zoom in/out using the mouse wheel
   - Filter the graph for specific nodes and edges.

## How It Works

The application uses LangChain's experimental graph transformers with your chosen LLM provider to:
1. Extract entities from the input text
2. Identify relationships between these entities
3. Generate a graph structure representing this information
4. Visualize the graph using PyVis, a Python interface for the vis.js visualization library

### Supported LLM Providers

| Provider | Models | Cost | Setup |
|----------|--------|------|-------|
| **Ollama** | llama2, llama3, mistral, codellama, phi | **FREE** (runs locally) | [Install Ollama](https://ollama.ai) |
| **OpenAI** | gpt-4o, gpt-4-turbo, gpt-3.5-turbo | Paid API | Requires API key |
| **Anthropic** | claude-3-opus, claude-3-sonnet, claude-3-haiku | Paid API | Requires API key |
| **Google** | gemini-pro, gemini-1.5-pro | Free tier available | Requires API key |

## Why Use This Without OpenAI?

While the original version used OpenAI's API exclusively, this updated version supports multiple providers:

- **Cost savings**: Use Ollama locally with no API costs
- **Privacy**: Keep your data local with Ollama
- **Flexibility**: Choose the model that best fits your needs
- **Availability**: No dependency on a single provider

## Troubleshooting

### "API key not found" error
- Ensure you have created a `.env` file in the root directory
- Verify the API key variable name matches your provider (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- Check that there are no extra spaces or quotes around the key

### Ollama connection error
- Ensure Ollama is installed and running: `ollama serve`
- Verify the model is downloaded: `ollama list`
- Check the base URL in your `.env` file (default: `http://localhost:11434`)

### Module import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- You may need to install provider-specific packages separately if not all are installed

## License

This project is licensed under the MIT License - a permissive open source license that allows for free use, modification, and distribution of the software.

For more details, see the [MIT License](https://opensource.org/licenses/MIT) documentation.
