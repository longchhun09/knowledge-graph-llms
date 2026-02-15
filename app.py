# Import necessary modules
import streamlit as st
import streamlit.components.v1 as components  # For embedding custom HTML
from generate_knowledge_graph import generate_knowledge_graph

# Set up Streamlit page configuration
st.set_page_config(
    page_icon=None, 
    layout="wide",  # Use wide layout for better graph display
    initial_sidebar_state="auto", 
    menu_items=None
)

# Set the title of the app
st.title("Knowledge Graph From Text")

# Sidebar section for LLM provider configuration
st.sidebar.title("LLM Configuration")
provider = st.sidebar.selectbox(
    "Choose LLM Provider:",
    ["OpenAI", "Ollama (Local)", "Anthropic (Claude)", "Google (Gemini)"],
    help="Select the language model provider to use for graph extraction"
)

# Map display names to provider keys
provider_map = {
    "OpenAI": "openai",
    "Ollama (Local)": "ollama",
    "Anthropic (Claude)": "anthropic",
    "Google (Gemini)": "google"
}
selected_provider = provider_map[provider]

# Model selection based on provider
model_options = {
    "openai": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    "ollama": ["llama2", "llama3", "mistral", "codellama", "phi"],
    "anthropic": ["claude-3-sonnet-20240229", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
    "google": ["gemini-pro", "gemini-1.5-pro"]
}

selected_model = st.sidebar.selectbox(
    "Choose Model:",
    model_options[selected_provider],
    help="Select the specific model to use"
)

# Display configuration info
if selected_provider == "openai":
    st.sidebar.info("💡 Requires OPENAI_API_KEY in .env file")
elif selected_provider == "ollama":
    st.sidebar.info("💡 Requires Ollama running locally (default: http://localhost:11434)")
elif selected_provider == "anthropic":
    st.sidebar.info("💡 Requires ANTHROPIC_API_KEY in .env file")
elif selected_provider == "google":
    st.sidebar.info("💡 Requires GOOGLE_API_KEY in .env file")

st.sidebar.markdown("---")

# Sidebar section for user input method
st.sidebar.title("Input document")
input_method = st.sidebar.radio(
    "Choose an input method:",
    ["Upload txt", "Input text"],  # Options for uploading a file or manually inputting text
)

# Case 1: User chooses to upload a .txt file
if input_method == "Upload txt":
    # File uploader widget in the sidebar
    uploaded_file = st.sidebar.file_uploader(label="Upload file", type=["txt"])
    
    if uploaded_file is not None:
        # Read the uploaded file content and decode it as UTF-8 text
        text = uploaded_file.read().decode("utf-8")
 
        # Button to generate the knowledge graph
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                try:
                    # Call the function to generate the graph from the text
                    net = generate_knowledge_graph(text, provider=selected_provider, model=selected_model)
                    st.success("Knowledge graph generated successfully!")
                    
                    # Save the graph to an HTML file
                    output_file = "knowledge_graph.html"
                    net.save_graph(output_file) 

                    # Open the HTML file and display it within the Streamlit app
                    HtmlFile = open(output_file, 'r', encoding='utf-8')
                    components.html(HtmlFile.read(), height=1000)
                except Exception as e:
                    st.error(f"Error generating knowledge graph: {str(e)}")
                    st.info("Please check your API keys in the .env file and ensure all dependencies are installed.")

# Case 2: User chooses to directly input text
else:
    # Text area for manual input
    text = st.sidebar.text_area("Input text", height=300)

    if text:  # Check if the text area is not empty
        if st.sidebar.button("Generate Knowledge Graph"):
            with st.spinner("Generating knowledge graph..."):
                try:
                    # Call the function to generate the graph from the input text
                    net = generate_knowledge_graph(text, provider=selected_provider, model=selected_model)
                    st.success("Knowledge graph generated successfully!")
                    
                    # Save the graph to an HTML file
                    output_file = "knowledge_graph.html"
                    net.save_graph(output_file) 

                    # Open the HTML file and display it within the Streamlit app
                    HtmlFile = open(output_file, 'r', encoding='utf-8')
                    components.html(HtmlFile.read(), height=1000)
                except Exception as e:
                    st.error(f"Error generating knowledge graph: {str(e)}")
                    st.info("Please check your API keys in the .env file and ensure all dependencies are installed.")