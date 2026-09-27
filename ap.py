import os
import certifi
import requests
import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor


# =========================================================
# CONFIG
# =========================================================

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Wheather & Search AI Agent",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# BARBIE CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Pacifico&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255, 105, 180, 0.18), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(255, 182, 193, 0.25), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(255, 20, 147, 0.12), transparent 30%),
        linear-gradient(135deg, #fff0f7 0%, #ffe4f1 45%, #fff7fb 100%);
    font-family: 'DM Sans', sans-serif;
}


/* Main container */

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* Hero */

.hero {
    text-align: center;
    padding: 35px 20px 25px 20px;
}

.hero-title {
    font-family: 'Pacifico', cursive;
    font-size: 64px;
    color: #e91e8c;
    margin-bottom: 5px;
    text-shadow: 0 4px 18px rgba(233, 30, 140, 0.18);
}

.hero-subtitle {
    color: #8c466d;
    font-size: 17px;
    letter-spacing: 0.5px;
}

.sparkle {
    color: #ff4fa3;
}


/* Cards */

.glass-card {
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(255, 105, 180, 0.25);
    border-radius: 28px;
    padding: 25px;
    box-shadow:
        0 15px 45px rgba(214, 51, 132, 0.12),
        inset 0 1px 0 rgba(255,255,255,0.8);
    backdrop-filter: blur(16px);
    color: #6d214f;
}

.glass-card h2, .glass-card p, .glass-card li, .glass-card b, .glass-card span {
    color: inherit;
}


/* Agent badge */

.agent-badge {
    display: inline-block;
    background: linear-gradient(90deg, #ff4fa3, #ff8ac5);
    color: white;
    padding: 7px 16px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 700;
    box-shadow: 0 6px 18px rgba(255, 79, 163, 0.25);
}


/* Tool pills */

.tool-pill {
    display: inline-block;
    background: #fff0f7;
    color: #d63384;
    border: 1px solid #ffc1dd;
    padding: 8px 13px;
    border-radius: 50px;
    margin: 4px;
    font-size: 13px;
    font-weight: 600;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #ffedf7 0%,
            #ffd9eb 50%,
            #fff0f7 100%
        );
    border-right: 1px solid rgba(255, 105, 180, 0.2);
}

section[data-testid="stSidebar"] * {
    color: #6d214f !important;
}


/* Inputs */

.stTextInput > div > div > input,
.stTextArea textarea {
    border-radius: 18px !important;
    border: 1.5px solid #ffb6d8 !important;
    background: rgba(255,255,255,0.85) !important;
    color: #6d214f !important;
    padding: 14px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #ff4fa3 !important;
    box-shadow: 0 0 0 3px rgba(255,79,163,0.12) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder {
    color: #b06a90 !important;
    opacity: 1 !important;
}


/* Chat input box (bottom bar) */

[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.85) !important;
}

[data-testid="stChatInput"] textarea {
    color: #6d214f !important;
    background: rgba(255,255,255,0.85) !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #b06a90 !important;
    opacity: 1 !important;
}


/* Buttons */

.stButton > button {
    border: none !important;
    border-radius: 18px !important;
    background: linear-gradient(135deg, #ff4fa3, #e91e8c) !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 12px 25px !important;
    box-shadow: 0 8px 22px rgba(233,30,140,0.25);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(233,30,140,0.32);
}


/* Chat messages */

[data-testid="stChatMessage"] {
    border-radius: 24px;
    border: 1px solid rgba(255,105,180,0.15);
    background: rgba(255,255,255,0.72);
    margin-bottom: 12px;
    color: #6d214f !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] code {
    color: #6d214f !important;
}

/* General markdown body text (covers cards, welcome block, etc.) */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: #6d214f;
}


/* Expander */

.streamlit-expanderHeader {
    border-radius: 18px !important;
    color: #c21870 !important;
    font-weight: 700 !important;
}


/* Divider */

hr {
    border-color: rgba(255,105,180,0.18);
}


/* Footer */

.footer {
    text-align: center;
    color: #a95a82;
    font-size: 13px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TOOLS
# =========================================================

search_tool = TavilySearchResults(max_results=2)


@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url, timeout=15)
    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )


# =========================================================
# LLM
# =========================================================

@st.cache_resource
def create_agent():

    llm = ChatOpenAI(
        model="qwen/qwen3.8-27b",
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY,
        temperature=0,
        max_tokens=900,
        streaming=False,
    )

    prompt = hub.pull("hwchase17/react")

    tools = [
        search_tool,
        get_weather_data
    ]

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=False,
        max_iterations=5
    )

    return executor


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
    Barbie AI Agent 🎀
</div>

<div class="hero-subtitle">
    Your pretty little research assistant with serious agentic skills ✨
</div>

<br>

<span class="agent-badge">
    ✦ ReAct Agent
</span>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center">

    <div style="
        font-family:Pacifico;
        font-size:34px;
        color:#e91e8c;
    ">
        Barbie AI
    </div>

    <div style="
        color:#9c4774;
        font-size:13px;
    ">
        Smart. Pretty. Agentic. 💅
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🎀 Agent Stack")

    st.markdown("""
    <span class="tool-pill">Qwen 3.8</span>
    <span class="tool-pill">Groq</span>
    <span class="tool-pill">LangChain</span>
    <span class="tool-pill">ReAct</span>
    <span class="tool-pill">Tavily</span>
    <span class="tool-pill">WeatherStack</span>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### ✨ What I can do")

    st.markdown("""
    🔎 **Search the web**

    🌳 **Find factual information**

    🌤️ **Get current weather**

    🧠 **Reason through multiple steps**

    🔗 **Use multiple tools sequentially**
    """)

    st.divider()

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="🎀" if message["role"] == "assistant" else "💗"
    ):
        st.markdown(message["content"])


# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.markdown("""
    <div class="glass-card">

    <h2 style="
        color:#d63384;
        margin-bottom:5px;
    ">
        Hi Barbie! 💕
    </h2>

    <p style="
        color:#7d4564;
        font-size:16px;
    ">
        Ask me something and I'll figure out which tools
        I need to get the answer.
    </p>

    <br>

    <b style="color:#c21870;">Try asking:</b>

    <ul style="color:#7d4564;">
        <li>Find the capital of India and its current weather.</li>
        <li>Find the number of trees in Delhi and tell me today's weather.</li>
        <li>Search for the latest AI news and summarize it.</li>
        <li>Find today's weather in Mumbai.</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.write("")


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "✨ Ask Barbie AI anything..."
)


# =========================================================
# RUN AGENT
# =========================================================

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user", avatar="💗"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🎀"):

        with st.spinner("✨ Barbie is thinking..."):

            try:

                agent_executor = create_agent()

                response = agent_executor.invoke({
                    "input": user_input
                })

                answer = response["output"]

            except Exception as e:

                answer = (
                    "Oops! 💕 Something went wrong while "
                    "my agent was working.\n\n"
                    f"`{str(e)}`"
                )

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    Made with 💗 + LangChain + Groq + ReAct
    <br>
    <span style="opacity:0.7;">
        Pretty UI. Serious AI.
    </span>
</div>
""", unsafe_allow_html=True)
