import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    """
    Creates a Streamlit web application for generating cold emails based on job postings.

    Parameters:
        llm: Language model interface for extracting job information and generating emails
        portfolio: Portfolio object containing user's work examples and relevant links
        clean_text: Function to preprocess and clean the scraped text data

    Flow:
        1. Displays a URL input field for job posting
        2. On submission, scrapes the webpage content
        3. Extracts job details using the language model
        4. Matches user's portfolio links with required skills
        5. Generates personalized cold emails
        6. Displays the generated emails in the UI

    Returns:
        None - Displays results directly in Streamlit interface

    Raises:
        Exception: Displays error message in Streamlit UI if any step fails
    """
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job[0].get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)