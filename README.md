# AI Research & Recommendation Agent

### LangGraph-Style Multi-Step Company Research System
**Built with Groq, Streamlit, and Sequential AI Workflows**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-LLM-black?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LangGraph-Agent_Workflow-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Llama_3.3-70B-orange?style=for-the-badge" />
</p>

<p align="center">
  <strong>
    AI-powered company research agent that analyzes businesses, identifies challenges,
    recommends AI opportunities, and generates CEO-ready strategic reports.
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

- Research any company
- Generate business intelligence reports
- Identify operational and strategic challenges
- Discover practical AI opportunities
- Generate CEO-ready recommendations
- Download complete reports
- Watch the workflow execute node-by-node in real time

---

# Why This Project?

Most AI research tools rely on a single prompt, which often produces generic and surface-level insights.

This project mimics how a human business analyst works:

1. Understand the company
2. Gather business context
3. Identify operational and strategic challenges
4. Discover AI opportunities tied to those challenges
5. Present recommendations as an executive pitch

Instead of generating everything from one prompt, the system follows a structured multi-step workflow where each stage builds on the previous one.

This results in more grounded, contextual, and actionable business recommendations.

---

# Features

✅ Multi-step AI research workflow

✅ LangGraph-style sequential state machine

✅ Company overview generation

✅ Business intelligence analysis

✅ Challenge identification

✅ AI opportunity mapping

✅ CEO-ready strategic recommendations

✅ 90-Day implementation roadmap

✅ Real-time workflow tracking

✅ Downloadable reports

✅ Multiple Groq model support

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
| LangGraph Pattern | Workflow orchestration |
| TypedDict | State management |
| Llama Models | Research and analysis generation |

---

# Project Workflow

```text
Company Name
      │
      ▼
Company Overview
      │
      ▼
Key Business Information
      │
      ▼
Business Challenges
      │
      ▼
AI Opportunities
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
│ Input Company Name                                  │
│      │                                              │
│      ▼                                              │
│ ResearchGraph.run_node()                            │
│      │                                              │
│      ▼                                              │
│ Live Status Updates                                 │
│      │                                              │
│      ▼                                              │
│ Tabbed Research Report + Download                   │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│         LangGraph-Style State Machine               │
│                                                     │
│ START                                               │
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
                          ▼
┌─────────────────────────────────────────────────────┐
│                  Groq API                           │
│                                                     │
│ llama-3.3-70b-versatile                             │
│ llama-3.1-8b-instant                                │
│ mixtral-8x7b-32768                                  │
└─────────────────────────────────────────────────────┘
```

---

# Approach

The objective was to build a system that reasons like a business analyst rather than generating a generic AI report.

Instead of one large prompt, the workflow is decomposed into five specialized research stages.

## Research Stages

### 1. Company Overview

Generates:

- Industry
- Company background
- Market presence
- Company scale
- Geographic footprint

### 2. Key Business Information

Identifies:

- Products and services
- Recent developments
- Partnerships
- Growth initiatives
- Strategic priorities

### 3. Business Challenges

Analyzes:

- Sales challenges
- Operational bottlenecks
- Customer experience issues
- Data limitations
- Competitive pressures

### 4. AI Opportunities

Maps AI solutions directly to business challenges.

Provides:

- AI use cases
- Business value
- Expected impact
- Feasibility ratings

### 5. CEO Pitch Generator

Creates:

- Executive summary
- Strategic recommendations
- AI transformation narrative
- 90-Day roadmap

---

# State Management

The application uses a TypedDict-based state object.

```python
AgentState
│
├── company
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

Each node receives the current state and returns an enriched version.

---

# Node Summary

| Node | Input Context | Output |
|--------|---------------|---------|
| Company Overview | Company Name | Company profile, industry, scale |
| Key Business Info | Company Overview | Products, initiatives, developments |
| Challenges | Overview + Business Info | Strategic and operational challenges |
| AI Opportunities | Challenges + Overview | AI recommendations and feasibility |
| Pitch Generator | Full Context | Executive pitch and roadmap |

---

# Key Design Decisions

| Decision | Reason |
|-----------|---------|
| Sequential workflow | Later stages require earlier insights |
| TypedDict state | Explicit and extensible schema |
| One API call per node | Better output quality and modularity |
| Streamlit UI | Fast development and interactive UX |
| Context chaining | Recommendations remain grounded |
| Temperature = 0.55 | Balance between creativity and accuracy |

---

# AI Models Supported

| Model | Speed | Best For |
|---------|--------|-----------|
| llama-3.3-70b-versatile | Medium | Highest quality analysis |
| llama-3.1-8b-instant | Fastest | Live demos and testing |
| mixtral-8x7b-32768 | Fast | Large-context research |

---

# Challenges Faced & Solutions

## Challenge 1: Generic Outputs

Early versions generated recommendations that could apply to almost any company.

### Solution

Added strict prompt instructions:

> "Do NOT provide generic recommendations. Every insight must be tied to the company's industry, scale, geography, and business model."

---

## Challenge 2: Context Window Growth

Passing outputs between nodes increased token usage.

### Solution

- Applied word-count limits
- Limited node output sizes
- Configured max_tokens limits
- Structured context passing

---

## Challenge 3: Output Structure Consistency

Models occasionally changed markdown formatting.

### Solution

Created fixed markdown templates and required section headers for every node.

---

## Challenge 4: Streamlit State Management

Maintaining live execution status was challenging because Streamlit reruns scripts on state changes.

### Solution

- Stored status inside `st.session_state`
- Managed node lifecycle states
- Triggered reruns only when required

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

---

## Step 2

Launch the application.

---

## Step 3

Paste your API key into the sidebar.

---

## Step 4

Select a model:

- llama-3.3-70b-versatile
- llama-3.1-8b-instant
- mixtral-8x7b-32768

---

## Step 5

Enter a company name.

Examples:

```text
Tesla
Netflix
NVIDIA
OpenAI
Microsoft
```

---

## Step 6

Click:

```text
Generate Report
```

---

## Step 7

Review the generated sections:

- Company Overview
- Business Information
- Challenges
- AI Opportunities
- CEO Pitch
- 90-Day Roadmap

---

## Step 8

Download the final report.

---

# Deploy Your Own Version

## Streamlit Cloud

1. Fork this repository
2. Create a Streamlit account
3. Connect GitHub
4. Select the repository
5. Deploy
6. Add your Groq API key

Your application will be live in minutes.

---

# Performance

| Setting | Value |
|----------|--------|
| Default Model | llama-3.3-70b-versatile |
| Temperature | 0.55 |
| Max Tokens | 1024 |
| Workflow Type | Sequential |
| Average Runtime | 15–25 seconds |

---

# Future Improvements

- Real-time web search integration
- Competitor benchmarking
- PDF export support
- Multi-company comparison
- Historical report storage
- Interactive workflow visualization
- AI implementation cost estimation
- Vector database integration
- RAG-powered company research

---

# Highlights

✔ Multi-Step AI Agent Workflow

✔ LangGraph-Style State Machine

✔ Context-Aware Sequential Reasoning

✔ Groq LLM Integration

✔ Streamlit Dashboard

✔ Real-Time Workflow Visualization

✔ CEO-Level Strategic Recommendations

✔ Downloadable Research Reports

---

# Author

**Prince Pandit**

💼 AI/ML Developer | Generative AI Enthusiast

---
