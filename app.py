import streamlit as st
import openai
import yfinance as yf  # Import yfinance for financial data
from dotenv import load_dotenv  # For secure API key loading
import os

# Load environment variables (replace with your actual logic)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

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

    # OpenAI Assistant completion for code optimization (optional)
    completion_prompt = f"Code Assistance: Here's the provided Python code:\n {''.join(open(__file__).readlines())}\nPlease provide insights on how to optimize the code for better performance and readability."






# import streamlit as st
# import openai
# import yfinance as yf  # Import yfinance for financial data

# # Streamlit app title and description
# st.title("AI Investment Agent ")
# st.caption("This app allows you to compare the performance of two stocks and generate detailed reports using OpenAI.")

# # Get OpenAI API key from user
# openai_api_key = st.text_input("OpenAI API Key", type="password")

# # Set OpenAI API key (securely store using environment variables)
# if openai_api_key:
#     openai.api_key = openai_api_key
#     st.info("Using provided API key for OpenAI communication.")
# else:
#     st.warning("No API key provided. Ensure your environment variable 'OPENAI_API_KEY' is set for optimal functionality.")

# # Input fields for the stocks to compare
# stock1 = st.text_input("Enter the first stock symbol")
# stock2 = st.text_input("Enter the second stock symbol")

# if stock1 and stock2:

#     # Craft the query for OpenAI
#     query = f"Compare the performance of {stock1} and {stock2}. Analyze their historical data, current market trends, analyst recommendations, and generate a comprehensive report highlighting key investment insights."

#     # Use OpenAI Completion API
#     response = openai.Completion.create(
#         engine="gpt-3.5-turbo-instruct",  # Adjust engine based on desired focus
#         prompt=query,
#         max_tokens=2048,  # Adjust based on desired report detail
#         n=1,
#         stop=None,
#         temperature=0.7,  # Adjust for creativity vs. factuality
#     )
#     st.write("**OpenAI Report:**")
#     st.write(response.choices[0].text)

#     # Retrieve financial data using yfinance
#     ticker1 = yf.Ticker(stock1)
#     ticker2 = yf.Ticker(stock2)

#     # Process and display financial data (optional)
#     # You can display relevant financial metrics like historical prices, analyst ratings, etc.
#     # Ensure proper data handling and formatting for user presentation.
#     st.write("**Financial Data:**")
#     # Example: Display historical closing prices
#     st.write(f"**{stock1} Closing Price:** {ticker1.info['previousClose']}")
#     st.write(f"**{stock2} Closing Price:** {ticker2.info['previousClose']}")

#     # OpenAI assistant completion
#     completion = openai.Completion.create(
#         engine="davinci-codex",
#         prompt="Code Assistance: Please provide insights on how to optimize the code for better performance and readability.",
#         max_tokens=150,
#     )
#     st.write("**OpenAI Assistant Suggestions:**")
#     st.write(completion.choices[0].text)
