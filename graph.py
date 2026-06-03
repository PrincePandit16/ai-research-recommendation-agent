from typing import TypedDict
from groq import Groq

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False




class AgentState(TypedDict, total=False):
    company: str
    web_search: str         
    web_sources: list        
    company_overview: str
    key_business_info: str
    challenges: str
    ai_opportunities: str
    pitch_generator: str




def node_web_search(state: AgentState, tavily_client=None) -> AgentState:
    """Fetch real-time company data from the web using Tavily."""
    company = state['company']

    if tavily_client is None or not TAVILY_AVAILABLE:
        return {
            **state,
            "web_search": f"[Web search skipped — no Tavily key provided. Analysis will use LLM training data only.]",
            "web_sources": []
        }

    queries = [
        f"{company} latest news 2024 2025",
        f"{company} expansion plans recent developments",
        f"{company} revenue business performance",
    ]

    all_results = []
    sources = []

    for query in queries:
        try:
            response = tavily_client.search(
                query=query,
                search_depth="basic",
                max_results=3,
                include_answer=True,
            )
            if response.get("answer"):
                all_results.append(f"**Query:** {query}\n**Summary:** {response['answer']}")

            for r in response.get("results", []):
                snippet = r.get("content", "")[:400]
                all_results.append(f"**Source:** {r.get('title', '')}\n{snippet}")
                sources.append({
                    "title": r.get("title", ""),
                    "url":   r.get("url", ""),
                    "date":  r.get("published_date", "recent"),
                })
        except Exception as e:
            all_results.append(f"[Search error for '{query}': {str(e)}]")

    combined = "\n\n---\n\n".join(all_results[:8])  # cap context size
    return {
        **state,
        "web_search": combined,
        "web_sources": sources[:9],
    }



def node_company_overview(state: AgentState, client: Groq, model: str) -> AgentState:
    live_data = state.get("web_search", "")
    live_section = f"\n\nRECENT WEB DATA (use this to enrich your answer with current facts):\n---\n{live_data}\n---" if live_data and "skipped" not in live_data else ""

    prompt = f"""You are a senior business analyst. Write a concise company overview for **{state['company']}**.{live_section}

Cover exactly these points (use markdown headers):
### What the Company Does
### Industry & Sector
### Scale (employees, revenue range, market position)
### Geographic Presence

Be specific and factual. Where recent web data is available, reference it. 200-250 words. Use bullet points."""

    return {**state, "company_overview": _call_groq(client, model, prompt)}



def node_key_business_info(state: AgentState, client: Groq, model: str) -> AgentState:
    live_data = state.get("web_search", "")
    live_section = f"\nRecent web data:\n---\n{live_data[:1200]}\n---" if live_data and "skipped" not in live_data else ""

    prompt = f"""You are a business intelligence analyst. Provide key business information for **{state['company']}**.

Company overview context:
---
{state.get('company_overview', '')}
---{live_section}

Provide:
### Major Products & Services
### Recent Developments (last 1-2 years — prioritise any web data above)
### Expansion Plans & Strategic Moves
### Key Partnerships / Clients / Awards

Be specific. If web data contradicts training data, prefer web data as more recent. 220-260 words."""

    return {**state, "key_business_info": _call_groq(client, model, prompt)}



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

    return {**state, "challenges": _call_groq(client, model, prompt)}



def node_ai_opportunities(state: AgentState, client: Groq, model: str) -> AgentState:
    live_data = state.get("web_search", "")
    live_section = f"\nLatest company context from web:\n{live_data[:800]}" if live_data and "skipped" not in live_data else ""

    prompt = f"""You are an AI solutions architect. Recommend concrete AI use cases for **{state['company']}**.

Company context:
---
{state.get('company_overview', '')}
Challenges identified:
{state.get('challenges', '')}
---{live_section}

For each opportunity, give:
- **What to build** (1 sentence)
- **How it helps** (specific to this company's pain)
- **Feasibility** (Easy / Medium / Complex)

### 1. Sales & Lead Intelligence AI
### 2. Customer Engagement & Chatbots
### 3. Operations & Process Automation
### 4. Document Processing & Compliance
### 5. Analytics & Forecasting Dashboard

Be hyper-specific. Reference actual pain points. 280-320 words."""

    return {**state, "ai_opportunities": _call_groq(client, model, prompt)}



def node_pitch_generator(state: AgentState, client: Groq, model: str) -> AgentState:
    company = state['company']
    prompt = f"""You are an AI consultant preparing to meet the CEO of **{company}**.

Write a one-page personalized pitch:

---
**Subject: Unlocking AI-Driven Growth for {company}**

**Opening — Why I Reached Out**
(2-3 sentences referencing specific recent developments or scale.)

**What I Found — Your Key Opportunities**
(3-4 bullets. Each: specific challenge → specific AI solution.)

**My Recommendation — Where to Start**
(Highest-ROI initiative. 3-step 90-day roadmap.)

**Why Now**
(Industry trends, competitive pressure, timing.)

**Call to Action**
(One clear ask.)
---

Use all research below:
Overview: {state.get('company_overview', '')}
Challenges: {state.get('challenges', '')}
AI Opportunities: {state.get('ai_opportunities', '')}

Tone: confident, CEO-ready, no fluff. 300-350 words."""

    return {**state, "pitch_generator": _call_groq(client, model, prompt)}



def _call_groq(client: Groq, model: str, prompt: str, temperature: float = 0.55) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": (
                "You are an expert business analyst and AI consultant. "
                "Provide accurate, specific, actionable insights. "
                "Never give generic content. Ground analysis in the company's specific context. "
                "When recent web data is provided, prioritise it over older training knowledge."
            )},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()




class ResearchGraph:
    """
    Sequential LangGraph-style graph.
    Flow: web_search → company_overview → key_business_info
          → challenges → ai_opportunities → pitch_generator
    """

    def __init__(self, groq_api_key: str, tavily_api_key: str = "",
                 model: str = "llama-3.3-70b-versatile"):
        self.groq_client = Groq(api_key=groq_api_key)
        self.model = model
        self.tavily_client = None
        if tavily_api_key and TAVILY_AVAILABLE:
            self.tavily_client = TavilyClient(api_key=tavily_api_key)

    def run_node(self, node_key: str, state: AgentState) -> AgentState:
        if node_key == "web_search":
            return node_web_search(state, self.tavily_client)
        node_map = {
            "company_overview":  node_company_overview,
            "key_business_info": node_key_business_info,
            "challenges":        node_challenges,
            "ai_opportunities":  node_ai_opportunities,
            "pitch_generator":   node_pitch_generator,
        }
        fn = node_map.get(node_key)
        if fn is None:
            raise ValueError(f"Unknown node: {node_key}")
        return fn(state, self.groq_client, self.model)

    def run_all(self, company: str) -> AgentState:
        state: AgentState = {"company": company}
        for key in ["web_search", "company_overview", "key_business_info",
                    "challenges", "ai_opportunities", "pitch_generator"]:
            state = self.run_node(key, state)
        return state
