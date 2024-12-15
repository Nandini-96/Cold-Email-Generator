import re

def clean_text(text):
    """
    Clean and normalize text by removing HTML tags, URLs, special characters, and excess whitespace.

    Args:
        text (str): The input text string to be cleaned.

    Returns:
        str: The cleaned text string with:
            - HTML tags removed
            - URLs removed
            - Special characters removed (keeping only alphanumeric and spaces)
            - Multiple spaces replaced with single spaces
            - Leading/trailing whitespace removed

    Example:
        >>> clean_text("<p>Hello  World! https://example.com</p>")
        'Hello World'
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text