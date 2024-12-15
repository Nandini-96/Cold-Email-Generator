import pandas as pd
import chromadb
import uuid


class Portfolio:
    """
    A class to manage a portfolio of technical skills and associated links using ChromaDB for vector storage.
    
    The portfolio data is loaded from a CSV file and stored in a vector database for efficient querying.
    """
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        """
        Initialize the Portfolio instance.

        Args:
            file_path (str): Path to the CSV file containing portfolio data.
                           Defaults to 'app/resource/my_portfolio.csv'
        """
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        """
        Load portfolio data into the ChromaDB collection if it's empty.
        
        Reads technology stack and links from the CSV file and adds them to the vector database
        with unique UUIDs as identifiers.
        """
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        """
        Query the portfolio for links related to specified skills.

        Args:
            skills (str or list): The technical skills to query for

        Returns:
            list: A list of metadata dictionaries containing matching links,
                 limited to top 2 results
        """
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])