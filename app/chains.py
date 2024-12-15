import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv() # set up the environment variable 

class Chain:
    """
    A class that handles job extraction from career pages and email generation using the Groq LLM.
    
    This class provides functionality to:
    1. Extract job postings from scraped website text
    2. Generate cold emails for business development purposes
    """
    def __init__(self):
        """
        Initialize the Chain class with a Groq LLM configuration.
        
        Sets up the language model with:
        - Zero temperature for deterministic outputs
        - Groq API key from environment variables
        - llama-3.1-70b-versatile model
        """
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile"
        )

    def extract_jobs(self,cleaned_text):
        """
        Extract job postings from cleaned website text and return them in JSON format.
        
        Args:
            cleaned_text (str): The cleaned text from a career's page website
            
        Returns:
            dict or list: Parsed job postings containing role, experience, skills, and description
            
        Raises:
            OutputParserException: If the context is too large to parse
        """
        prompt_extract=PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing
            following keys: `role`, `experience` ,`skills` and `description`.
            Strictly output ONLY valid JSON without any preamble, explanations, 
            formatting characters like triple backticks (```), or any additional text.
            ### OUTPUT (STRICTLY VALID JSON WITHOUT TRIPLE BACKTICKS):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser=JsonOutputParser()
            res=json_parser.parse(res.content)
        except OutputParserException :
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, dict) else [res]
    
    def write_mail(self, job, links):
        """
        Generate a cold email for business development based on job description.
        
        Args:
            job (dict): Job posting information to reference in the email
            links (list): Portfolio links to include in the email
            
        Returns:
            str: Generated email content from the perspective of a BDE at AtliQ
        """
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
            Remember you are Mohan, BDE at AtliQ. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
    
if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
