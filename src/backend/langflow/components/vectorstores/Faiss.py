from typing import Optional, Union
from langflow import CustomComponent

from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStore
from langchain.schema import BaseRetriever
from langchain.schema import Document
from langchain.embeddings.base import Embeddings


class FAISSComponent(CustomComponent):
    """
    A custom component for implementing a Vector Store using FAISS.
    """

    display_name: str = "FAISS (Custom Component)"
    description: str = "Implementation of Vector Store using FAISS"
    documentation = "https://python.langchain.com/docs/integrations/vectorstores/faiss"
    beta = True

    def build_config(self):
        return {
            "persistence": {
                "display_name": "Persistence",
                "options": ["In-Memory", "LocalDirectory"],
                "value": "In-Memory",
            },
            "folder_path": {
                "display_name": "Folder Path",
                "required": False,
            },
            "index_name": {"display_name": "Index Name", "value": "faiss_index"},
            "documents": {"display_name": "Documents", "is_list": True},
            "embeddings": {"display_name": "Embeddings"},
            "code": {"display_name": "Code", "show": False},
        }

    def build(
        self,
        persistence: str,
        index_name: str,
        folder_path: Optional[str] = None,
        documents: Optional[Document] = None,
        embeddings: Optional[Embeddings] = None,
    ) -> Union[VectorStore, BaseRetriever]:
        if persistence == "LocalDirectory" and not folder_path:
            raise ValueError("Folder path is required for local directory persistence")

        if documents is None:
            return FAISS.load_local(
                folder_path=folder_path, embeddings=embeddings, index_name=index_name
            )

        db = FAISS.from_documents(documents=documents, embedding=embeddings)

        # Save if persistence is LocalDirectory
        if persistence == "LocalDirectory":
            db.save_local(folder_path=folder_path, index_name=index_name)

        return db
