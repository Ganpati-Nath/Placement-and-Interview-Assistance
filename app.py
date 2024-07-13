import json
import streamlit as st
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
import os
import google.generativeai as genai
import time
from googlesearch import search
import requests

# Set Streamlit page configuration
st.set_page_config(
    page_title="Placement and Interview Guide...",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="auto",
)

# Load environment variables and configure generative AI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate response using Gemini Pro
def generate_gemini_response(query):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(query)
    return response.text

# Function to fetch resources using Google Search with error handling and retry mechanism
def fetch_resources(query):
    attempts = 0
    max_attempts = 5
    backoff_time = 1

    while attempts < max_attempts:
        try:
            search_results = search(query, stop=5, pause=2)
            resources = [{"title": f"Resource {i+1}", "link": link} for i, link in enumerate(search_results)]
            return resources
        except Exception as e:
            if "429" in str(e):
                attempts += 1
                st.warning(f"Rate limited. Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
                backoff_time *= 2
            else:
                st.error(f"Error fetching resources: {str(e)}")
                return []
    st.error("Max retries exceeded. Please try again later.")
    return []

# Function to load Lottie animation
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        st.text(r.text)  # Print the response text for debugging
        return None

# Load Lottie animation
lottie_url = "https://lottie.host/f6c2a0ec-981a-43d5-a3b9-ebe90532628e/7eSvhWa3nC.json"
lottie_animation = load_lottieurl(lottie_url)

# CSS for Typewriter Effect and Layout Adjustments
st.markdown(
    """
    <style>
    body {
        margin: 0;
        padding: 0;
        overflow: hidden;
        font-family: 'Monospace', sans-serif;
        background: black;
    }

    .typewriter h1 {
        overflow: hidden; 
        border-right: .15em solid orange; 
        white-space: nowrap; 
        margin: 0 auto; 
        letter-spacing: .15em; 
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        position: relative;
        z-index: 1;
    }

    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: orange }
    }

    /* Responsive adjustments */
    @media (max-width: 1200px) {
        .typewriter h1 {
            font-size: 1.8em;
        }
    }
    @media (max-width: 992px) {
        .typewriter h1 {
            font-size: 1.6em;
        }
    }
    @media (max-width: 768px) {
        .typewriter h1 {
            font-size: 1.4em;
        }
    }
    @media (max-width: 576px) {
        .typewriter h1 {
            font-size: 1.2em;
            width: 100%;
        }
    }

    .lottie-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Main application with Typewriter Effect for the Title
st.markdown(
    """
    <div class="typewriter">
        <h1>Placement and Interview Guide...</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Display Lottie animation as background using a container
if lottie_animation:
    st_lottie(lottie_animation, key="lottie_animation", height=350)

# Tabs for different sections
tabs = st.tabs(["Placement and Interview Questions", "Placement Queries", "Resources"])

# Handling the tabs content
with tabs[0]:
    st.header("Placement and Interview Questions")
    question = st.text_area("Ask a placement or interview question:")

    if st.button("Get Answer", key="answer_btn_1"):
        if question:
            with st.spinner("Generating response..."):
                time.sleep(2)
                response = generate_gemini_response(question)
            st.markdown("## Chatbot Response")
            st.write(response)
        else:
            st.warning("Please enter a question before clicking 'Get Answer'.")

with tabs[1]:
    st.header("Placement Queries")
    query = st.text_area("Ask a placement-related query:")

    if st.button("Get Response", key="response_btn_1"):
        if query:
            with st.spinner("Generating response..."):
                time.sleep(2)
                response = generate_gemini_response(query)
            st.markdown("## Chatbot Response")
            st.write(response)
        else:
            st.warning("Please enter a query before clicking 'Get Response'.")

with tabs[2]:
    st.header("Resources")
    resource_query = st.text_input("Resource Type:", value='')

    if st.button("Get Resources", key="resources_btn_1"):
        if resource_query:
            with st.spinner("Fetching resources..."):
                resources = fetch_resources(resource_query)
            if resources:
                st.markdown(f"Here are some resources related to '{resource_query}':")
                for idx, resource in enumerate(resources, start=1):
                    st.markdown(f"{idx}. [{resource['title']}]({resource['link']})")
            else:
                st.warning(f"No resources found for '{resource_query}'.")
        else:
            st.warning("Please enter a resource type before clicking 'Get Resources'.")

# CSS for interactive animations
st.markdown(
    """
    <style>
    .stButton>button:hover {
        background-color: #4CAF50;
    }
    .stMarkdown a:hover {
        color: #007bff;
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
