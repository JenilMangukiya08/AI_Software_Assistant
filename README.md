# 🤖 AI Software Assistant

An intelligent **AI-powered Software Development Assistant** that helps developers understand, analyze, review, and interact with software repositories using **Multi-Agent AI**, **LangGraph**, **Retrieval-Augmented Generation (RAG)**, and **Large Language Models (LLMs)**.

The assistant enables developers to upload a repository, ask natural language questions, generate documentation, review code, detect bugs, explain source files, analyze databases, generate UML diagrams, and much more through a conversational interface.

---

# 🚀 Features

## Multi-Agent AI Workflow

The assistant uses a planner-based multi-agent architecture to solve complex software engineering tasks.

### Available AI Agents

* 📂 Repository Agent
* 📖 Documentation Agent
* 🔍 Code Review Agent
* 🐞 Bug Detection Agent
* 🧪 Test Case Generation Agent

---

## Development Tools

The assistant intelligently invokes specialized tools depending on the user's question.

### Available Tools

* 📄 File Reader
* 🔎 Code Search
* 📊 Code Metrics
* 🔒 Security Scanner
* 🗄 Database Parser
* 📐 UML Generator
* ⚙ Code Execution
* 🔀 File Compariso

---

# 🏗 System Architecture

```text
                    +----------------------+
                    |      React UI        |
                    +----------+-----------+
                               |
                               |
                     Django REST APIs
                               |
                               |
                    Authentication Layer
                               |
                               |
                     LangGraph Workflow
                               |
                     +---------+---------+
                     |                   |
                 Planner           Conversation Memory
                     |
                     |
             Multi-Agent Executor
                     |
      +--------------+---------------+
      |              |               |
 Repository     Documentation      Review
    Agent           Agent           Agent
      |              |               |
      +--------------+---------------+
                     |
                 Tool Router
                     |
      +--------------+------------------------------+
      |              |              |              |
 File Reader   Code Search   Security Scanner  UML Generator
      |              |              |              |
      +--------------+--------------+--------------+
                     |
               Repository Retriever
                     |
                 Chroma Vector DB
                     |
                 Groq Llama 3.3
                     |
               Final AI Response
```

---

# 🧠 AI Workflow

```text
User Question
      │
      ▼
Planner
      │
      ▼
Execution Graph
      │
      ▼
Repository Agent
      │
      ▼
Appropriate Tool
      │
      ▼
Repository Retrieval
      │
      ▼
Relevant Context
      │
      ▼
Groq LLM
      │
      ▼
Synthesizer
      │
      ▼
Final Answer
```

---

# 🧩 Technology Stack

## Frontend

* React.js
* React Router
* Axios
* React Markdown
* Mermaid.js
* CSS

---

## Backend

* Python
* Django
* Django REST Framework

---

## AI Stack

* LangGraph
* LangChain
* Groq Llama 3.3
* ChromaDB
* Sentence Transformers

---

## Database

* SQLite (Development)
* Chroma Vector Database

---

## Authentication

* Django Authentication
* JWT Authentication

---

# 📁 Project Structure

```text
AI_Software_Assistant/

│
├── backend/
│   ├── api/
│   ├── graph/
│   ├── llm/
│   ├── rag/
│   ├── repositories/
│   ├── tools/
│   ├── utils/
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   └── package.json
│
├── requirements.txt
├── README.md
└── .env
```

---

# 🤖 Agent Responsibilities

## Repository Agent

* Understand repository-level questions
* Route requests to the correct development tool
* Coordinate repository analysis

---

## Documentation Agent

Generates:

* Repository documentation
* Code explanations
* Module summaries
* API descriptions

---

## Code Review Agent

Performs:

* Code quality review
* Best practice analysis
* Maintainability suggestions
* Refactoring recommendations

---

## Bug Detection Agent

Helps identify:

* Potential bugs
* Logical issues
* Risky code
* Error-prone implementations

---

## Test Case Generation Agent

Generates:

* Unit test ideas
* Edge cases
* Functional test scenarios
* Suggested testing strategies

---

# 🛠 Tool Responsibilities

## 📄 File Reader

Explains the contents of a specific source file.

---

## 🔎 Code Search

Searches across the repository and returns relevant code snippets with context.

---

## 📊 Code Metrics

Analyzes:

* Total files
* Python files
* Classes
* Functions
* Lines of Code (LOC)
* Project statistics

---

## 🔒 Security Scanner

Reviews the repository for common security concerns and provides recommendations.

---

## 🗄 Database Parser

Parses Django models and generates:

* Entity Relationship (ER) Diagram
* Database schema explanation
* Relationships
* Foreign Keys
* One-to-One relationships
* Many-to-Many relationships

---

## 📐 UML Generator

Creates UML diagrams such as:

* Class Diagram
* Sequence Diagram
* Flow Diagram

using Mermaid syntax.

---

## ⚙ Code Execution

Safely executes supported Python files and returns execution output.

---

## 🔀 File Comparison

Compares two source files and highlights structural or logical differences.

---

# 💬 Example Questions

### Repository

* Summarize this repository.
* Explain this project.

### Documentation

* Generate documentation for this module.
* Explain the authentication workflow.

### Code Review

* Review this repository.
* Suggest improvements.

### Bug Detection

* Find bugs in this project.
* Identify possible runtime issues.

### File Reader

* Explain `views.py`.
* What does `workflow.py` do?

### Code Search

* Where is `report_node` defined?
* Find the login API implementation.

### Database

* Explain the database schema.
* Generate the ER diagram.

### UML

* Generate the class diagram.
* Create a sequence diagram.

### Security

* Scan this repository for vulnerabilities.

### Code Metrics

* Analyze the project metrics.
* Show code statistics.

---

# 🔐 Authentication

The application supports authenticated users.

Features include:

* User Registration
* User Login
* Protected APIs
* Chat History
* Repository Management

---

# 📚 API Overview

| Method | Endpoint                  | Description            |
| ------ | ------------------------- | ---------------------- |
| POST   | `/api/register/`          | Register user          |
| POST   | `/api/login/`             | User login             |
| POST   | `/api/upload-repository/` | Upload repository      |
| GET    | `/api/repositories/`      | List repositories      |
| POST   | `/api/chat/`              | Chat with AI assistant |
| GET    | `/api/history/`           | Conversation history   |
| GET    | `/api/history/<id>/`      | Load a conversation    |
| GET    | `/api/file-tree/`         | Repository file tree   |
| GET    | `/api/debug/`             | Execution trace        |

---

# 💡 Key Highlights

* Multi-Agent AI Architecture
* Planner-based Task Execution
* LangGraph Workflow
* Retrieval-Augmented Generation (RAG)
* Chroma Vector Database
* Natural Language Repository Analysis
* Interactive Repository Explorer
* Chat History Management
* AI-Powered Software Engineering Assistant

---

# 🔮 Future Enhancements

* Docker Support
* CI/CD Integration
* Multi-Repository Chat
* Multi-LLM Support
* Code Generation Agent
* Automated Refactoring Suggestions
* Git Integration
* Cloud Deployment
* Team Collaboration
* Repository Version Comparison

---

# 👨‍💻 Author

**Jenil Mangukiya**

**Roles**

* AI Engineer
* Python Developer
* Backend Developer
* Generative AI Enthusiast

---

# ⭐ Acknowledgements

Special thanks to the open-source communities behind:

* Django
* React
* LangChain
* LangGraph
* ChromaDB
* Groq
* Sentence Transformers
* Mermaid
* OpenAI research community

---

# 📜 License

This project is intended for educational, research, and portfolio purposes.
