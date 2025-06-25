from langgraph.graph import StateGraph,START,END

from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_nodes

from langgraph.prebuilt import ToolNode,tools_condition

from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode

from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder = StateGraph(State)


    def basic_chatbot_build_graph(self):
        """
        
        Build the basic Graph using langgraph
        
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self):
        """
        Build the chatbot with tools graph using langgraph
        """
        # Placeholder for future implementation
        tools= get_tools(self)
        tool_nodes = create_tool_nodes(tools)

        llm=self.llm

        chatbot_with_tool_node = ChatbotWithToolNode(llm).create_chatbot(tools)

        self.graph_builder.add_node("chatbot",chatbot_with_tool_node)
        self.graph_builder.add_node("tools", tool_nodes)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder_graph(self):
        """
        Build the AI News graph using langgraph
        """

        ai_node = AINewsNode(self.llm)

        # Placeholder for future implementation
        self.graph_builder.add_node("fetch_news",ai_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_node.save_results)

        # adding edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result", END)

        print("AI News Graph built successfully")

    def setup_graph(self, use_case: str):
        """
        Sets up the graph for use case
        """
        if use_case == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if use_case == "Chatbot with Web":
            self.chatbot_with_tools_build_graph()
        if use_case == "AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()