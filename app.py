import os
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Resolve USER_AGENT environment variable issue
os.environ["USER_AGENT"] = "web-agent"

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# List of 10 news article URLs
urls = [
    "https://www.example.com/news/world-economy/article1",
    "https://www.example.com/news/world-economy/article2",
    # Add more URLs up to 10
]

# Load multiple web pages
loader = WebBaseLoader(urls)
data = loader.load()

# Initialize the language model
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
)

# Prepare the messages
messages = [
    (
        "system",
        "Your task is to summarize the following news articles into a cohesive blog post with sections on World Economy and AI Industry. Organize the summaries in an engaging and readable format suitable for publishing on a blog.",
    ),
    ("human", "\n\n".join([doc.page_content for doc in data])),
]

# Generate the blog post
ai_msg = llm.invoke(messages)
print(ai_msg.content)
