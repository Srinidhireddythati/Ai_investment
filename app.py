import streamlit as st
import openai
import yfinance as yf  # Import yfinance for financial data
from dotenv import load_dotenv  # For secure API key loading
import os

# Load environment variables (recommended for production)
load_dotenv()

# Securely retrieve OpenAI API key from environment variable (if set)
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    # Prompt user for API key if not found in environment variables
    openai_api_key = st.text_input("OpenAI API Key", type="password")

# Set OpenAI API key (securely stored)
if openai_api_key:
    openai.api_key = openai_api_key
    st.info("Using provided API key for OpenAI communication.")
else:
    st.warning("No API key found in environment variables. Ensure 'OPENAI_API_KEY' is set for optimal functionality.")

# Streamlit app title and description
st.title("AI Investment Agent ")
st.caption("This app allows you to compare the performance of two stocks and generate detailed reports using OpenAI.")

# Input fields for the stocks to compare
with st.sidebar:  # Move input fields to sidebar for better organization
    st.title("Stock Comparison")
    stock1 = st.text_input("Enter the first stock symbol")
    stock2 = st.text_input("Enter the second stock symbol")

if stock1 and stock2:

    # Craft the query for OpenAI
    query = f"Compare the performance of {stock1} and {stock2}. Analyze their historical data, current market trends, analyst recommendations, and generate a comprehensive report highlighting key investment insights."

    # Use OpenAI Completion API
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Adjust engine based on desired focus
            prompt=query,
            max_tokens=2048,  # Adjust based on desired report detail
            n=1,
            stop=None,
            temperature=0.7,  # Adjust for creativity vs. factuality
        )
        st.write("**OpenAI Report:**")
        st.write(response.choices[0].text)
    except openai.OpenAIError as e:
        st.error(f"Error generating report: {e}")

    # Retrieve financial data using yfinance
    ticker1 = yf.Ticker(stock1)
    ticker2 = yf.Ticker(stock2)

    # Handle potential missing data with error handling
    try:
        # Try alternative key for previous close price (adjust based on yfinance data structure)
        closing_price1 = ticker1.info.get("regularMarketPreviousClose")
        if closing_price1:
            st.write(f"**{stock1} Closing Price:** {closing_price1}")
        else:
            st.warning(f"Previous close data unavailable for {stock1}.")
    except (KeyError, AttributeError):
        st.warning(f"Error retrieving financial data for {stock1}.")

    try:
        # Try alternative key for previous close price (adjust based on yfinance data structure)
        closing_price2 = ticker2.info.get("regularMarketPreviousClose")
        if closing_price2:
            st.write(f"**{stock2} Closing Price:** {closing_price2}")
        else:
            st.warning(f"Previous close data unavailable for {stock2}.")
    except (KeyError, AttributeError):
        st.warning(f"Error retrieving financial data for {stock2}.")

# Optional: Code optimization with OpenAI Assistant completion (outside code execution)
# This section is for demonstration purposes and should not be included in the running code.
# You can comment it out or use it for separate analysis.
# completion_prompt = f"Code Assistance: Here's the provided Python code:\n {''.join(open(__file__).readlines())}\nPlease provide insights on how to optimize the code for better performance and readability."
