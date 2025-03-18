#  Linkedin lookup

##  Description
linkedin-lookup is an LLM powered agent allowing you to look up for publically visible linkedin profile and query informations related to those profiles using natural language.

##  Features
- ✅ Internet search using Tavily
- ✅ Linkedin profile lookup using scrapin.io API as a tool

![Screenshot](https://i.imgur.com/j1WQkBr.png)

##  Tech Stack
- **Programming Language:** Python
- **Frameworks & Libraries:** LangChain, OpenAI


##  Installation & Setup
1. **Get API access**
- Go to https://app.scrapin.io/ and request your linkedin API key
- Go to https://docs.tavily.com/ and request your Tavily API key
- Go to https://platform.openai.com/ and request your Tavily API key
- Replace the file .env-example with a .env file and put all your API keys in it
  
2.  **Clone the repository**
   ```bash
   git clone https://github.com/lamineAbdelmalek/linkedin_lookup.git
   cd agenda_helper
```
   To run the project localy:
  ```bash
  poetry install
  streamlit run linkedin_lookup/app.py --server.port=8589 --server.address=0.0.0.0
```
  To run the project via docker:
  ```bash
    docker build . -t linkedin_lookup
    docker run --env-file .env -p 8589:8589 linkedin_lookup
```
  
