from typing import TypedDict, Optional
from groq import Groq



class AgentState(TypedDict, total=False):
    company: str
    company_overview: str
    key_business_info: str
    challenges: str
    ai_opportunities: str
    pitch_generator: str




def node_company_overview(state: AgentState, client: Groq, model: str) -> AgentState:
    prompt = f"""You are a senior business analyst. Write a concise company overview for **{state['company']}**.

Cover exactly these points (use markdown headers):
### What the Company Does
### Industry & Sector
### Scale (employees, revenue range, market position)
### Geographic Presence

Be specific and factual. 200-250 words max. Use bullet points inside each section."""

    result = _call_groq(client, model, prompt)
    return {**state, "company_overview": result}


def node_key_business_info(state: AgentState, client: Groq, model: str) -> AgentState:
    prompt = f"""You are a business intelligence analyst. Based on your knowledge of **{state['company']}**, provide key business information.

Use the context below for reference:
---
{state.get('company_overview', '')}
---

Now provide:
### Major Products & Services
### Recent Developments (last 1-2 years)
### Expansion Plans & Strategic Moves
### Key Partnerships / Clients / Awards

Be specific to this company. 220-260 words. Use bullet points."""

    result = _call_groq(client, model, prompt)
    return {**state, "key_business_info": result}


def node_challenges(state: AgentState, client: Groq, model: str) -> AgentState:
    prompt = f"""You are a management consultant. Analyze **{state['company']}** and identify its real, specific business challenges.

Context:
---
{state.get('company_overview', '')}
{state.get('key_business_info', '')}
---

Identify challenges under these categories. For each challenge, explain WHY it applies to this specific company:

### Sales & Lead Generation Challenges
### Operational Bottlenecks
### Customer Experience Gaps
### Data & Technology Gaps
### Market / Competitive Pressures

Do NOT give generic answers. Tie each point back to the company's scale, geography, and sector. 250-300 words."""

    result = _call_groq(client, model, prompt)
    return {**state, "challenges": result}


def node_ai_opportunities(state: AgentState, client: Groq, model: str) -> AgentState:
    prompt = f"""You are an AI solutions architect. Based on the specific challenges of **{state['company']}**, recommend concrete AI use cases.

Company context:
---
{state.get('company_overview', '')}
Challenges identified:
{state.get('challenges', '')}
---

For each opportunity below, give:
- **What to build** (1 sentence)
- **How it helps** (specific to this company's pain)
- **Feasibility** (Easy / Medium / Complex)

### 1. Sales & Lead Intelligence AI
### 2. Customer Engagement & Chatbots
### 3. Operations & Process Automation
### 4. Document Processing & Compliance
### 5. Analytics & Forecasting Dashboard

Be hyper-specific. Reference actual pain points from the challenges section. 280-320 words."""

    result = _call_groq(client, model, prompt)
    return {**state, "ai_opportunities": result}


def node_pitch_generator(state: AgentState, client: Groq, model: str) -> AgentState:
    company = state['company']
    prompt = f"""You are an AI consultant preparing to meet the CEO of **{company}**.

Write a one-page personalized pitch. Use this structure:

---
**Subject: Unlocking AI-Driven Growth for {company}**

**Opening — Why I Reached Out**
(2-3 sentences. Reference something specific about the company's scale, expansion, or recent news.)

**What I Found — Your Key Opportunities**
(3-4 bullet points. Each maps a specific company challenge → an AI solution. Be precise.)

**My Recommendation — Where to Start**
(Pick the single highest-ROI AI initiative. Explain the 90-day roadmap in 3 steps.)

**Why Now**
(1 paragraph. Reference industry trends, competitive pressure, or timing specific to their sector.)

**Call to Action**
(One clear ask — a 30-minute call, a pilot proposal, etc.)

---

Use the research below to personalize every line:
Company Overview: {state.get('company_overview', '')}
Challenges: {state.get('challenges', '')}
AI Opportunities: {state.get('ai_opportunities', '')}

Tone: confident, respectful, CEO-ready. No fluff. 300-350 words total."""

    result = _call_groq(client, model, prompt)
    return {**state, "pitch_generator": result}



def _call_groq(client: Groq, model: str, prompt: str, temperature: float = 0.55) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert business analyst and AI consultant. "
                    "You provide accurate, specific, and actionable insights. "
                    "Never give generic or filler content. "
                    "Always ground your analysis in the company's specific context."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


class ResearchGraph:
    """
    Sequential LangGraph-style graph.
    Each node enriches the shared AgentState.
    """

    NODE_MAP = {
        "company_overview":  node_company_overview,
        "key_business_info": node_key_business_info,
        "challenges":        node_challenges,
        "ai_opportunities":  node_ai_opportunities,
        "pitch_generator":   node_pitch_generator,
    }

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model  = model

    def run_node(self, node_key: str, state: AgentState) -> AgentState:
        """Run a single named node and return the updated state."""
        fn = self.NODE_MAP.get(node_key)
        if fn is None:
            raise ValueError(f"Unknown node: {node_key}")
        return fn(state, self.client, self.model)

    def run_all(self, company: str) -> AgentState:
        """Run the full graph from START to END."""
        state: AgentState = {"company": company}
        for key in self.NODE_MAP:
            state = self.run_node(key, state)
        return state
