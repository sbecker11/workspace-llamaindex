"""
Module for loading email and Outlook message content.

This module includes functions to load email data from various file formats.
"""

# Create a download loader
from llama_index.readers.file import UnstructuredReader

# Initialize the UnstructuredReader
loader = UnstructuredReader()

def load_email_data(file_path: str):
    """Load email data from file path."""
    eml_documents = loader.load_data(file_path)
    email_content = eml_documents[0].text
    print("\n\n Email contents")
    print(email_content)
    return email_content

def load_outlook_message(file_path: str):
    """Load outlook message data from file path."""
    msg_documents = loader.load_data(file_path)
    msg_content = msg_documents[0].text
    print("\n\n Outlook contents")
    print(msg_content)
    return msg_content
