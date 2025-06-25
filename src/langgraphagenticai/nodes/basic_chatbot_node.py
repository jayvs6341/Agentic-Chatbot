from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
        Basic Chatbot logic Implementation
    """

    def __init__(self,model):
        self.llm = model

    def process(self,state:State):
        """
        Process the input state and generate LLM response
        """
        return {"messages":self.llm.invoke(state['messages'])}