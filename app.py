import streamlit as st
import ast  # Safer than eval for string-to-list conversion
from agent_engine import get_stock_agent

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stMarkdown { font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 AI Equity Research Agent")

ticker = st.text_input("Enter Ticker (e.g., HDFCBANK.NS, RELIANCE.NS, NVDA):", "HDFCBANK.NS")
query = st.text_area("What do you want to know?",
                     f"Provide a detailed fundamental and technical analysis for {ticker}.")

if st.button("Run Analysis"):
    if query:
        with st.spinner("🔍 Agent is fetching market data and analyzing..."):
            try:
                agent = get_stock_agent()

                # 1. Get the raw result from the agent
                result = agent.invoke({"messages": [("user", query)]})

                # 2. Extract the content from the LAST AI message
                final_content = result["messages"][-1].content

                # 3. CLEANING LOGIC: Extract only the readable text
                if isinstance(final_content, list):
                    # If it's a list of blocks, join only the 'text' parts
                    report_text = "".join(
                        [block.get("text", "") for block in final_content if block.get("type") == "text"])
                elif isinstance(final_content, str) and final_content.startswith("[{'type'"):
                    # If it's a string representation of a list, parse it safely
                    try:
                        parsed_list = ast.literal_eval(final_content)
                        report_text = "".join(
                            [block.get("text", "") for block in parsed_list if block.get("type") == "text"])
                    except:
                        report_text = final_content
                else:
                    report_text = str(final_content)

                # 4. Display in UI
                st.subheader(f"Analysis Report: {ticker}")
                st.markdown("---")
                st.markdown(report_text)

                # 5. Download Button with clean string
                st.download_button(
                    label="📥 Download Report as TXT",
                    data=report_text,
                    file_name=f"{ticker}_analysis.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")