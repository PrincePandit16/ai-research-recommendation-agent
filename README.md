# AI Research & Recommendation Agent
### LangGraph × Groq × Streamlit

---

## Quick Start

```bash
# 1. Clone / unzip the project
cd research_agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Open `http://localhost:8501` → enter your **Groq API key** (sidebar) → type a company name → click **Generate Report**.

Get a free Groq key at: https://console.groq.com

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit UI (app.py)              │
│   Input ──► ResearchGraph.run_node(key, state)      │
│             ↓ per node, live status updates          │
│   Output ◄── tabbed report + download button        │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│              LangGraph State Machine (graph.py)      │
│                                                     │
│  AgentState (TypedDict) flows through nodes:        │
│                                                     │
│  START                                              │
│    ↓                                                │
│  node_company_overview      → adds 'company_overview'  │
│    ↓                                                │
│  node_key_business_info     → adds 'key_business_info' │
│    ↓                                                │
│  node_challenges            → adds 'challenges'     │
│    ↓                                                │
│  node_ai_opportunities      → adds 'ai_opportunities'  │
│    ↓                                                │
│  node_pitch_generator       → adds 'pitch_generator'   │
│    ↓                                                │
│  END                                                │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│               Groq API (LLM Inference)               │
│  Model: llama-3.3-70b-versatile (default)           │
│  Each node = 1 API call with focused prompt         │
│  Context from previous nodes passed forward         │
└─────────────────────────────────────────────────────┘
```

## Key Design Decisions

| Decision | Reason |
|---|---|
| Sequential graph (not parallel) | Each node uses prior nodes' output as context, so ordering matters |
| `TypedDict` for state | Explicit schema, easy to extend with new nodes |
| One Groq call per node | Focused prompts = better quality than one mega-prompt |
| Streamlit + live status | Visual graph execution feedback like a real LangGraph run |
| Context chaining | `challenges` node sees `overview` + `business_info`, so analysis is grounded |

## File Structure

```
research_agent/
├── app.py          # Streamlit UI — input, live graph status, tabbed report
├── graph.py        # LangGraph state machine — nodes, AgentState, ResearchGraph class
├── requirements.txt
└── README.md
```

## AI Tools Used
- **Groq** — ultra-fast LLM inference (free tier available)
- **LangGraph pattern** — state machine with typed state passed through nodes
- **Streamlit** — rapid UI with live updates

## Models Available
| Model | Speed | Quality |
|---|---|---|
| llama-3.3-70b-versatile | Medium | Best |
| llama-3.1-8b-instant | Fastest | Good |
| mixtral-8x7b-32768 | Fast | Good |
