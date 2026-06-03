# AI Research & Recommendation Agent

### LangGraph-Style Multi-Step Company Research System
**Built with Groq, Tavily, Streamlit, and Sequential AI Workflows**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-LLM-black?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LangGraph-Agent_Workflow-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Llama_3.3-70B-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Tavily-Web_Search-blueviolet?style=for-the-badge" />
</p>

<p align="center">
  <strong>
    AI-powered company research agent that fetches live web data, analyzes businesses,
    identifies challenges, recommends AI opportunities, and generates CEO-ready strategic reports.
  </strong>
</p>

<p align="center">
  🚀 <strong>Live Demo:</strong><br>
  https://ai-research-recommendation-agent.streamlit.app/
</p>

---

# Live Demo

Try the application instantly without any installation:

### 🌐 Live Application

https://ai-research-recommendation-agent.streamlit.app/

The platform allows you to:

- Research any company with real-time web data (via Tavily)
- Generate business intelligence reports grounded in live news
- Identify operational and strategic challenges
- Discover practical AI opportunities
- Generate CEO-ready recommendations
- Download complete reports with live sources cited
- Watch the workflow execute node-by-node in real time

---

# Why This Project?

Most AI research tools rely on a single prompt and stale training data, which often produces generic, outdated insights.

This project mimics how a human business analyst works:

1. **Search** the web for the latest news and developments
2. Understand the company using live + trained knowledge
3. Gather key business context
4. Identify operational and strategic challenges
5. Discover AI opportunities tied to those challenges
6. Present recommendations as an executive pitch

Instead of generating everything from one prompt, the system follows a structured multi-step workflow where each stage builds on the previous one — starting with fresh, real-time data from the web.

This results in more grounded, current, contextual, and actionable business recommendations.

---

# Features

✅ **Real-time web search** via Tavily (latest news, financials, expansions)

✅ Multi-step AI research workflow

✅ LangGraph-style sequential state machine

✅ Company overview generation (grounded in live data)

✅ Business intelligence analysis

✅ Challenge identification

✅ AI opportunity mapping

✅ CEO-ready strategic recommendations

✅ 90-Day implementation roadmap

✅ Real-time workflow tracking

✅ Live sources listed in the final report

✅ Downloadable reports

✅ Multiple Groq model support

✅ Graceful fallback when no Tavily key is provided

✅ Modular and extensible architecture

---

# Built With

<p align="center">

<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="70" />

<img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="70" />

</p>

| Technology | Purpose |
|------------|----------|
| Python | Core application logic |
| Streamlit | Interactive user interface |
| Groq API | Ultra-fast LLM inference |
| Tavily API | Real-time web search & news retrieval |
| LangGraph Pattern | Workflow orchestration |
| TypedDict | State management |
| Llama Models | Research and analysis generation |

---

# Project Workflow

```text
Company Name
      │
      ▼
🌐 Web Search (Tavily)        ← NEW: live news, financials, recent events
      │
      ▼
Company Overview              ← grounded in live search results
      │
      ▼
Key Business Information      ← uses overview + live data
      │
      ▼
Business Challenges
      │
      ▼
AI Opportunities              ← uses challenges + live data
      │
      ▼
CEO Pitch & 90-Day Roadmap
```

Each stage enriches the shared application state and passes context forward to the next stage.

---

# Architecture

```text
┌─────────────────────────────────────────────────────┐
│                   Streamlit UI                      │
│                                                     │
│ Input Company Name + API Keys (sidebar)             │
│      │                                              │
│      ▼                                              │
│ ResearchGraph.run_node()                            │
│      │                                              │
│      ▼                                              │
│ Live Status Updates                                 │
│      │                                              │
│      ▼                                              │
│ Tabbed Research Report + Sources + Download         │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│         LangGraph-Style State Machine               │
│                                                     │
│ START                                               │
│   │                                                 │
│   ▼                                                 │
│ node_web_search                   │
│   │                                                 │
│   ▼                                                 │
│ node_company_overview                               │
│   │                                                 │
│   ▼                                                 │
│ node_key_business_info                              │
│   │                                                 │
│   ▼                                                 │
│ node_challenges                                     │
│   │                                                 │
│   ▼                                                 │
│ node_ai_opportunities                               │
│   │                                                 │
│   ▼                                                 │
│ node_pitch_generator                                │
│   │                                                 │
│   ▼                                                 │
│ END                                                 │
└─────────────────────────────────────────────────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
┌────────────────────┐    ┌─────────────────────────┐
│   Tavily Search    │    │        Groq API          │
│                    │    │                          │
│ 3 targeted queries │    │ llama-3.3-70b-versatile  │
│ per company        │    │ llama-3.1-8b-instant     │
│ Up to 9 sources    │    │ mixtral-8x7b-32768        │
└────────────────────┘    └─────────────────────────┘
```

---

# How Tavily Integration Works

### Web Search Node (new first step)

Before any LLM analysis begins, the agent runs three targeted Tavily searches:

```text
"{company} latest news 2024 2025"
"{company} expansion plans recent developments"
"{company} revenue business performance"
```

Each query fetches up to 3 results. The top 8 snippets are combined into a live context block that is passed into subsequent nodes.

### Context Injection

The live web data is injected into the prompts of four downstream nodes:

| Node | Uses Live Data |
|------|---------------|
| Company Overview | ✅ Full context |
| Key Business Info | ✅ First 1200 chars |
| AI Opportunities | ✅ First 800 chars |
| Challenges | Uses enriched overview |
| Pitch Generator | Uses enriched outputs |

When live data is available, prompts explicitly instruct the model to **prioritise web data over training data** for recency.

### Sources in the Report

All source URLs, titles, and publication dates collected during the web search step are stored in the agent state and displayed in the final report's **Web Sources** tab. They are also included in the downloaded report.

### Graceful Fallback

The Tavily API key is **optional**. If not provided:
- The web search node is skipped
- A clear note is shown in the UI
- The agent continues using LLM training data only
- No errors or interruptions occur

---

# State Management

The application uses a TypedDict-based state object.

```python
AgentState
│
├── company
├── web_search       
├── web_sources       
├── company_overview
├── key_business_info
├── challenges
├── ai_opportunities
└── pitch_generator
```

State Flow:

```text
company
   │
   ▼
web_search + web_sources   
   │
   ▼
company_overview
   │
   ▼
key_business_info
   │
   ▼
challenges
   │
   ▼
ai_opportunities
   │
   ▼
pitch_generator
```

---

# Node Summary

| Node | Input Context | Output |
|------|---------------|--------|
| **Web Search** *(new)* | Company name | Live news snippets + source list |
| Company Overview | Company name + live data | Company profile, industry, scale |
| Key Business Info | Company overview + live data | Products, initiatives, developments |
| Challenges | Overview + business info | Strategic and operational challenges |
| AI Opportunities | Challenges + overview + live data | AI recommendations and feasibility |
| Pitch Generator | Full context | Executive pitch and roadmap |

---

# Key Design Decisions

| Decision | Reason |
|----------|--------|
| Tavily as first node | LLM stages receive live context from the start |
| Three targeted queries | Covers news, strategy, and financials efficiently |
| Cap at 8 snippets | Prevents context window overflow in downstream nodes |
| Partial injection per node | Balances freshness vs. token budget |
| Prefer web data over training | Avoids outdated facts about fast-moving companies |
| Optional Tavily key | Keeps the tool usable without any search API |
| Sequential workflow | Later stages require earlier insights |
| TypedDict state | Explicit and extensible schema |
| One API call per node | Better output quality and modularity |
| Streamlit UI | Fast development and interactive UX |
| Temperature = 0.55 | Balance between creativity and accuracy |

---

# AI Models Supported

| Model | Speed | Best For |
|-------|-------|----------|
| llama-3.3-70b-versatile | Medium | Highest quality analysis |
| llama-3.1-8b-instant | Fastest | Live demos and testing |
| mixtral-8x7b-32768 | Fast | Large-context research |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/enterprise-ai-research-agent.git

cd enterprise-ai-research-agent
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# How To Use

## Step 1

Get a free Groq API key:

https://console.groq.com

## Step 2

*(Optional but recommended)* Get a free Tavily API key for live web search:

https://app.tavily.com

## Step 3

Launch the application.

## Step 4

Paste your **Groq API key** and (optionally) your **Tavily API key** into the sidebar.

> Without a Tavily key, the agent skips web search and uses LLM training data only. All other features work normally.

## Step 5

Select a model:

- llama-3.3-70b-versatile
- llama-3.1-8b-instant
- mixtral-8x7b-32768

## Step 6

Enter a company name.

Examples:

```text
Tesla
Netflix
NVIDIA
OpenAI
Microsoft
```

## Step 7

Click:

```text
Generate Report
```

## Step 8

Review the generated sections:

- **Web Sources** — live articles fetched by Tavily
- Company Overview
- Business Information
- Challenges
- AI Opportunities
- CEO Pitch
- 90-Day Roadmap

## Step 9

Download the final report (includes all live sources).

---

# Deploy Your Own Version

## Streamlit Cloud

1. Fork this repository
2. Create a Streamlit account
3. Connect GitHub
4. Select the repository
5. Deploy
6. Add your Groq API key (and optionally Tavily key) in the app sidebar

Your application will be live in minutes.

---

# Performance

| Setting | Value |
|---------|-------|
| Default Model | llama-3.3-70b-versatile |
| Temperature | 0.55 |
| Max Tokens | 1024 per node |
| Workflow Type | Sequential |
| Tavily Queries | 3 per run |
| Max Sources | 9 |
| Average Runtime | 20–35 seconds (with Tavily) / 15–25 seconds (without) |

---

# Challenges Faced & Solutions

## Challenge 1: Generic Outputs

Early versions generated recommendations that could apply to almost any company.

### Solution

Added strict prompt instructions:

> "Do NOT provide generic recommendations. Every insight must be tied to the company's industry, scale, geography, and business model."

---

## Challenge 2: Stale Training Data

LLM training data lags behind real-world events by months or years.

### Solution

Integrated Tavily as a dedicated first node. Prompts explicitly instruct the model to prefer live web data over training knowledge when both are available.

---

## Challenge 3: Context Window Growth

Passing outputs between nodes — now including live search results — increases token usage.

### Solution

- Applied word-count limits per node
- Capped Tavily output at 8 snippets
- Used partial injection (shorter slices of live data) for nodes with tighter budgets
- Configured max_tokens limits throughout

---

## Challenge 4: Output Structure Consistency

Models occasionally changed markdown formatting.

### Solution

Created fixed markdown templates and required section headers for every node.

---

## Challenge 5: Streamlit State Management

Maintaining live execution status was challenging because Streamlit reruns scripts on state changes.

### Solution

- Stored status inside `st.session_state`
- Managed node lifecycle states including the new web search node
- Triggered reruns only when required

---

# Future Improvements

- Competitor benchmarking using live search
- PDF export support
- Multi-company comparison
- Historical report storage
- Interactive workflow visualization
- AI implementation cost estimation
- Vector database integration
- RAG-powered document research
- Deeper Tavily `advanced` search mode option

---

# Highlights

✔ **Real-Time Web Search** via Tavily

✔ Multi-Step AI Agent Workflow

✔ LangGraph-Style State Machine

✔ Context-Aware Sequential Reasoning

✔ Groq LLM Integration

✔ Streamlit Dashboard

✔ Real-Time Workflow Visualization

✔ CEO-Level Strategic Recommendations

✔ Downloadable Research Reports with Live Sources

---

# Author

**Prince Pandit**

💼 AI/ML Developer | Generative AI Enthusiast

---
