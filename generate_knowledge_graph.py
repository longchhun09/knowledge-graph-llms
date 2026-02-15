from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from pyvis.network import Network

from dotenv import load_dotenv
import os
import asyncio


# Load the .env file
load_dotenv()


def get_llm(provider="openai", model=None, **kwargs):
    """
    Initialize and return an LLM based on the specified provider.
    
    Args:
        provider (str): The LLM provider to use. Options: 'openai', 'ollama', 'anthropic', 'google'
        model (str): The specific model name to use (optional, uses defaults if not specified)
        **kwargs: Additional arguments to pass to the LLM constructor
    
    Returns:
        An initialized LLM instance
    
    Raises:
        ValueError: If the provider is not supported or required API keys are missing
    """
    provider = provider.lower()
    
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return ChatOpenAI(
            temperature=kwargs.get("temperature", 0),
            model_name=model or "gpt-4o",
            api_key=api_key
        )
    
    elif provider == "ollama":
        from langchain_ollama import OllamaLLM
        # Ollama runs locally, no API key needed
        return OllamaLLM(
            model=model or "llama2",
            temperature=kwargs.get("temperature", 0),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
    
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        return ChatAnthropic(
            temperature=kwargs.get("temperature", 0),
            model_name=model or "claude-3-sonnet-20240229",
            api_key=api_key
        )
    
    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        return ChatGoogleGenerativeAI(
            temperature=kwargs.get("temperature", 0),
            model=model or "gemini-pro",
            google_api_key=api_key
        )
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers: openai, ollama, anthropic, google")


# Extract graph data from input text
async def extract_graph_data(text, llm_instance):
    """
    Asynchronously extracts graph data from input text using a graph transformer.

    Args:
        text (str): Input text to be processed into graph format.
        llm_instance: The LLM instance to use for extraction.

    Returns:
        list: A list of GraphDocument objects containing nodes and relationships.
    """
    graph_transformer = LLMGraphTransformer(llm=llm_instance)
    documents = [Document(page_content=text)]
    graph_documents = await graph_transformer.aconvert_to_graph_documents(documents)
    return graph_documents


def visualize_graph(graph_documents):
    """
    Visualizes a knowledge graph using PyVis based on the extracted graph documents.

    Args:
        graph_documents (list): A list of GraphDocument objects with nodes and relationships.

    Returns:
        pyvis.network.Network: The visualized network graph object.
    """
    # Create network
    net = Network(height="1200px", width="100%", directed=True,
                      notebook=False, bgcolor="#222222", font_color="white", filter_menu=True, cdn_resources='remote') 

    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships

    # Build lookup for valid nodes
    node_dict = {node.id: node for node in nodes}
    
    # Filter out invalid edges and collect valid node IDs
    valid_edges = []
    valid_node_ids = set()
    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])

    # Track which nodes are part of any relationship
    connected_node_ids = set()
    for rel in relationships:
        connected_node_ids.add(rel.source.id)
        connected_node_ids.add(rel.target.id)

    # Add valid nodes to the graph
    for node_id in valid_node_ids:
        node = node_dict[node_id]
        try:
            net.add_node(node.id, label=node.id, title=node.type, group=node.type)
        except:
            continue  # Skip node if error occurs

    # Add valid edges to the graph
    for rel in valid_edges:
        try:
            net.add_edge(rel.source.id, rel.target.id, label=rel.type.lower())
        except:
            continue  # Skip edge if error occurs

    # Configure graph layout and physics
    net.set_options("""
        {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -100,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }
    """)

    output_file = "knowledge_graph.html"
    try:
        net.save_graph(output_file)
        print(f"Graph saved to {os.path.abspath(output_file)}")
        return net
    except Exception as e:
        print(f"Error saving graph: {e}")
        return None


def generate_knowledge_graph(text, provider="openai", model=None):
    """
    Generates and visualizes a knowledge graph from input text.

    This function runs the graph extraction asynchronously and then visualizes
    the resulting graph using PyVis.

    Args:
        text (str): Input text to convert into a knowledge graph.
        provider (str): LLM provider to use ('openai', 'ollama', 'anthropic', 'google'). Default: 'openai'
        model (str): Specific model name to use (optional, uses provider defaults if not specified)

    Returns:
        pyvis.network.Network: The visualized network graph object.
    """
    # Initialize the LLM based on the selected provider
    llm_instance = get_llm(provider=provider, model=model)
    
    # Extract graph data and visualize
    graph_documents = asyncio.run(extract_graph_data(text, llm_instance))
    net = visualize_graph(graph_documents)
    return net