from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    A class representing a chatbot node that can interact with tools.
    This class is designed to be used within a state management system, 
    """
    def __init__(self,model):
        """
        Initializes the ChatbotWithToolNode with a model.
        
        Args:
            model: The model to be used by the chatbot.
        """
        self.llm = model

    # def process(self, state: State):
    #     """
    #     Processes the state and returns a response from the chatbot.
        
    #     Args:
    #         state (State): The current state of the chatbot.
        
    #     Returns:
    #         str: The response from the chatbot.
    #     """
    #     # Use the model to generate a response based on the current state
    #     user_input = state["messages"][-1] if state["messages"] else ""
    #     llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

    #     tools_response = f"Tool integration for: '{user_input}'"

    #     return {"messages": [llm_response, tools_response]}
    
    def create_chatbot(self, tools):
        """
        Creates a chatbot with the specified tools.
        
        Args:
            tools: The tools to be integrated with the chatbot.
        
        Returns:
            ChatbotWithToolNode: An instance of the chatbot with the specified tools.
        """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Processes the state and returns a response from the chatbot with tools.
            
            Args:
                state (State): The current state of the chatbot.
            
            Returns:
                str: The response from the chatbot with tools.
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        # This method can be extended to integrate specific tools with the chatbot
        return chatbot_node