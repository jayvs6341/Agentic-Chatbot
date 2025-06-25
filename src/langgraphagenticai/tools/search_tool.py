from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools(self):
    """
    Get the tools for the agentic AI application.
    
    Returns:
        list: A list of ToolNode instances for the available tools.
    """
    # Define the Tavily search tool
    tools=[TavilySearchResults(max_results=2)]
    return tools

def create_tool_nodes(tools):
    """
    Create tool nodes for the agentic AI application.
    
    Returns:
        list: A list of ToolNode instances for the available tools.
    """

    tool_nodes = ToolNode(tools=tools)
    return tool_nodes