import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    # def load_portfolio(self):
    #     if not self.collection.count():
    #         for _, row in self.data.iterrows():
    #             self.collection.add(documents=row["Techstack"],
    #                                 metadatas={"links": row["Links"]},
    #                                 ids=[str(uuid.uuid4())])

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],  # Wrap in list
                                    metadatas=[{"links": row["Links"]}],  # Wrap in list
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        if not skills or not isinstance(skills, str):  # Ensure skills is a valid string
            return []
        result = self.collection.query(
        query_texts=skills.strip(),  # Wrap input string in a list
        n_results=2
        )

        return result.get('metadatas', [])
