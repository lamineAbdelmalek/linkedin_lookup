import os
from typing import List, Union

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_openai import ChatOpenAI

from linkedin_lookup.constants import ENV_VAR_OPENAI_KEY
from linkedin_lookup.tools import get_all_tools

if ENV_VAR_OPENAI_KEY not in os.environ:
    load_dotenv(".env")
api_key = os.environ[ENV_VAR_OPENAI_KEY]

tools = get_all_tools()

client = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0).bind_tools(
    tools=tools
)

name_2_tool = {tool.name: tool for tool in tools}


def call_llm(
    messages: List[Union[AIMessage, HumanMessage, SystemMessage, ToolMessage]]
) -> BaseMessage:
    return client.invoke(input=messages)


# Streamlit UI
st.title("Linkedin lookup")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize LLM interactions tracking
if "llm_interactions" not in st.session_state:
    st.session_state.llm_interactions = [
        SystemMessage(
            "You are a helpful assistant, answer the users query. Use the tools available to you only WHEN NEEDED."
        )
    ]

# Print the user history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Hello, what can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.llm_interactions.append(HumanMessage(prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        llm_answer = call_llm(st.session_state.llm_interactions)
        while llm_answer.tool_calls:
            st.session_state.llm_interactions.append(llm_answer)
            for tool_call in llm_answer.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_call_id = tool_call["id"]
                tool_to_invoke = name_2_tool[tool_name]
                try:
                    output = tool_to_invoke.invoke(tool_args)
                except Exception as e:
                    output = (
                        f"error occured when calling tool: '{tool_name}' with args: {tool_args} \n"
                        f"error details: {str(e)}"
                    )
                tool_message = ToolMessage(output, tool_call_id=tool_call_id)
                st.session_state.llm_interactions.append(tool_message)
            llm_answer = client.invoke(input=st.session_state.llm_interactions)
        st.session_state.llm_interactions.append(llm_answer)
        response = st.markdown(llm_answer.content)
        st.session_state.messages.append(
            {"role": "assistant", "content": llm_answer.content}
        )
