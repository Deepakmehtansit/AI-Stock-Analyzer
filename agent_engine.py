import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools import fetch_fundamental_data, get_advanced_tech_analysis

load_dotenv()


def get_stock_agent():
    # Use the stable model ID we found earlier
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0,
        # Gemini 3 often requires v1beta for advanced tool use
        version="v1beta"
    )

    # llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
    #     temperature=0,
    #     # Explicitly setting the version can sometimes resolve 404s if the SDK is slightly behind
    #     version="v1")

    tools = [fetch_fundamental_data, get_advanced_tech_analysis]

    system_instructions = (
        "You are a Senior Equity Research Analyst. "
        "Structure your response with clear headings: 'Key Metrics', "
        "'Fundamental Analysis', 'Technical Trend', and 'Risk Factors'. "
        "Always include a disclaimer that you are an AI and not a financial advisor."
    )

    # If state_modifier failed, your version likely uses 'prompt'
    # OR you can pass it as the first message in the logic.
    try:
        agent = create_react_agent(
            llm,
            tools,
            state_modifier=system_instructions
        )
    except TypeError:
        # Fallback for different LangGraph versions
        agent = create_react_agent(
            llm,
            tools,
            prompt=system_instructions
        )

    return agent





































# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.prebuilt import create_react_agent
# from tools import fetch_fundamental_data, get_technical_summary
#
# load_dotenv()
#
# from langchain_core.messages import SystemMessage
#
#
# def get_stock_agent():
#     llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)
#
#     tools = [fetch_fundamental_data, get_technical_summary]
#
#     # Define a persona for the agent
#     system_prompt = (
#         "You are a Senior Equity Research Analyst. "
#         "When analyzing a stock, use a professional tone. "
#         "Structure your response with clear headings: 'Key Metrics', 'Fundamental Analysis', 'Technical Trend', and 'Risk Factors'. "
#         "Always include a disclaimer that you are an AI and not a financial advisor."
#     )
#
#     # Create the agent with the system prompt
#     agent = create_react_agent(
#         llm,
#         tools,
#         state_modifier=system_prompt  # This is how we set the 'Persona' in 2026
#     )
#
#     return agent
#
#
#
#
#
#
# # def get_stock_agent():
# #     # 1. Initialize Gemini 3 Flash (Fast & Free Tier available)
# #     # The 'google_api_key' is automatically read from your .env
# #     llm = ChatGoogleGenerativeAI(
# #         model="gemini-3-flash-preview",
# #         temperature=0,
# #         max_retries=2
# #     )
# #
# #     # 2. List your tools
# #     tools = [fetch_fundamental_data, get_technical_summary]
# #
# #     # 3. Create the Agent
# #     # In 2026, this is the standard way to create a 'Thinking' agent.
# #     # It returns a 'CompiledGraph' which is much more robust than the old Executor.
# #     agent = create_react_agent(llm, tools)
# #
# #     return agent