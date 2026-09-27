# 🎀 Weather & Search ReAct Agent

An AI-powered **ReAct agent** that can search the web, fetch current weather data, and combine information from multiple tools to answer user queries.

### 🚀 Live Demo

**[Try the AI Agent](https://search-wheatherreactagent.onrender.com/)**

---

## ✨ Features

* 🔎 **Web Search** — retrieves relevant information from the web
* 🌤️ **Weather Tool** — fetches current weather for a city
* 🧠 **ReAct Agent** — reasons through a task and decides which tool to use
* 🔗 **Multi-step Queries** — combines multiple tools to answer complex questions
* 💬 **Streamlit UI** — simple interactive chat interface

---

## 🛠️ Tech Stack

* **Python**
* **LangChain**
* **Groq / Qwen**
* **Tavily Search**
* **Weatherstack API**
* **Streamlit**
* **Render**

---

## ⚙️ How It Works

```text
User Query
    ↓
ReAct Agent
    ↓
Decides which tool to use
    ↓
┌───────────────┬────────────────┐
│ Web Search    │ Weather Tool   │
│   (Tavily)    │ (Weatherstack) │
└───────────────┴────────────────┘
    ↓
Combines Results
    ↓
Final Answer
```

The agent follows the **ReAct (Reason + Act)** approach, allowing it to dynamically select tools instead of relying only on the language model's knowledge.

---

## 💡 Example

Try asking:

> Find the capital of the country with the largest land area, find its current weather, and compare its temperature with New Delhi.

The agent can:

1. Search for the country with the largest land area
2. Identify its capital
3. Fetch the capital's current weather
4. Fetch New Delhi's weather
5. Compare the temperatures
6. Return the final answer

---

## 🔑 Environment Variables

Create a `.env` file locally:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
```

**Never commit your `.env` file to GitHub.**

---

## ▶️ Run Locally

```bash
git clone <your-repository-url>
cd 01_AiAgent

pip install -r requirements.txt

streamlit run ap.py
```

---

## 🌐 Live Application

[**Open the deployed AI Agent →**](https://search-wheatherreactagent.onrender.com/)

---

### 👩‍💻 Built with Python + LangChain + ReAct

Made by **Sanju Rohilla**

This project is provided under an open source-friendly license. Add a license file if you want to publish this repository publicly.
