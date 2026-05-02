from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq

def initialize_agent(db_path, groq_api_key):
    """
    Initializes the LangChain SQL Agent with Groq LLM.
    """
    # 1. Setup the LLM
    llm = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name="llama3-70b-8192", 
        temperature=0
    )
    
    # 2. Setup the Database connection
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    
    # 3. Create the Agent
    agent_executor = create_sql_agent(
        llm, 
        db=db, 
        agent_type="tool-calling", 
        verbose=True
    )
    
    return agent_executor
