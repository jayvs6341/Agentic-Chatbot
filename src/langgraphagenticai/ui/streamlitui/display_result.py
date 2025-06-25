import json
import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage

class DisplayResultStreamlit:

    def __init__(self,usecase,graph,user_message):
        self.use_case = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):

        usecase = self.use_case
        graph = self.graph
        user_message = self.user_message
        print("display_result_on_ui")
        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages' : ("user",user_message)}):
                print(event)
                for key, value in event.items():
                    print(f"Node: {key}")
                    print(f"Values: {value}")
                for value in event.values():
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)
        elif usecase == "Chatbot with Web":
            initial_state = {"messages": [user_message]}
            res = graph.invoke(initial_state)
            # for event in graph.stream(initial_state):
            #     for message in event.get("messages", []):
            #         if isinstance(message, ToolMessage):
            #             with st.chat_message("ai"):
            #                 st.write("Calling tool...")
            #                 st.write(message.content)
            for message in res["messages"]:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool call started")
                        st.write(message.content)
                        st.write("Tool call ended")
                elif type(message) == AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)

        elif usecase == "AI News":
            frequency = self.user_message
            print(f"Fetching AI News for frequency: {frequency}")
            with st.spinner("Fetching AI News..."):
                result = graph.invoke({"messages": frequency})
                try:
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, 'r') as file:
                        news_content = file.read()

                    st.markdown(news_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error("No news found for the selected frequency.")
                    return
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    return