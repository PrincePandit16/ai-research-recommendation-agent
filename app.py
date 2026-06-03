import streamlit as st
import time
from graph import ResearchGraph

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem; font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle { color: #6b7280; font-size: 1rem; margin-bottom: 2rem; }
    .node-card {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 1rem;
    }
    .node-header { font-weight: 600; font-size: 0.95rem; color: #374151; }
    .status-badge { font-size: 0.75rem; padding: 2px 8px; border-radius: 999px; font-weight: 500; float: right; }
    .status-waiting  { background: #f3f4f6; color: #6b7280; }
    .status-running  { background: #fef3c7; color: #92400e; }
    .status-done     { background: #d1fae5; color: #065f46; }
    .status-error    { background: #fee2e2; color: #991b1b; }
    .status-skipped  { background: #e0e7ff; color: #3730a3; }
    .graph-flow {
        display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
        padding: 0.8rem; background: #f1f5f9; border-radius: 10px;
        margin-bottom: 1.5rem; font-size: 0.82rem; color: #475569; font-family: monospace;
    }
    .node-pill { background: white; border: 1px solid #cbd5e1; border-radius: 6px; padding: 3px 10px; font-weight: 500; }
    .node-pill-search { background: #eff6ff; border: 1px solid #93c5fd; border-radius: 6px; padding: 3px 10px; font-weight: 500; color: #1d4ed8; }
    .arrow { color: #94a3b8; }
    .source-card {
        background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
        padding: 0.7rem 1rem; margin-bottom: 0.5rem; font-size: 0.85rem;
    }
    .source-card a { color: #2563eb; text-decoration: none; font-weight: 500; }
    .source-card a:hover { text-decoration: underline; }
    .source-date { color: #9ca3af; font-size: 0.75rem; margin-top: 2px; }
    .live-badge {
        background: #dcfce7; color: #166534; border: 1px solid #86efac;
        border-radius: 999px; padding: 2px 10px; font-size: 0.75rem; font-weight: 600;
    }
    .no-tavily-note {
        background: #fffbeb; border: 1px solid #fcd34d; border-radius: 8px;
        padding: 0.7rem 1rem; font-size: 0.85rem; color: #92400e; margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; border: none; border-radius: 8px;
        padding: 0.6rem 1rem; font-weight: 600; font-size: 1rem;
    }
    .stButton > button:hover { opacity: 0.9; border: none; }
</style>
""", unsafe_allow_html=True)

NODES = [
    ("web_search",        "🌐", "Web Search"),
    ("company_overview",  "🏢", "Company Overview"),
    ("key_business_info", "📊", "Key Business Info"),
    ("challenges",        "⚠️",  "Business Challenges"),
    ("ai_opportunities",  "🤖", "AI Opportunities"),
    ("pitch_generator",   "🎯", "CEO Pitch"),
]

def init_session():
    for k, default in [("node_status", {k: "waiting" for k,_,_ in NODES}),
                       ("node_output", {k: "" for k,_,_ in NODES}),
                       ("node_time",   {k: 0.0 for k,_,_ in NODES}),
                       ("web_sources", []),
                       ("running", False), ("done", False), ("error_msg", "")]:
        if k not in st.session_state:
            st.session_state[k] = default

def reset_state():
    st.session_state.node_status = {k: "waiting" for k,_,_ in NODES}
    st.session_state.node_output = {k: "" for k,_,_ in NODES}
    st.session_state.node_time   = {k: 0.0 for k,_,_ in NODES}
    st.session_state.web_sources = []
    st.session_state.running = False
    st.session_state.done    = False
    st.session_state.error_msg = ""

init_session()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    groq_key = st.text_input("Groq API Key *", type="password",
                              placeholder="gsk_...",
                              help="Required. Free at console.groq.com")

    st.markdown("---")
    st.markdown("#### 🌐 Real-Time Search (Optional)")
    tavily_key = st.text_input("Tavily API Key", type="password",
                                placeholder="tvly-...",
                                help="Optional. Free at app.tavily.com — enables live web search before analysis")

    if tavily_key:
        st.markdown('<span class="live-badge">✓ Live web search enabled</span>', unsafe_allow_html=True)
    else:
        st.caption("Without Tavily, the agent uses LLM training data only.")

    st.markdown("---")
    model_choice = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )

    st.markdown("---")
    st.markdown("### 🔗 Graph Flow")
    if tavily_key:
        st.markdown("""
```
START
  ↓
🌐 web_search (Tavily)
  ↓
🏢 company_overview
  ↓
📊 key_business_info
  ↓
⚠️  challenges
  ↓
🤖 ai_opportunities
  ↓
🎯 pitch_generator
  ↓
END
```""")
    else:
        st.markdown("""
```
START
  ↓
🌐 web_search (skipped)
  ↓
🏢 company_overview
  ...
```""")

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🔍 AI Research & Recommendation Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">LangGraph × Groq × Tavily — real-time intelligence reports for any company</div>', unsafe_allow_html=True)

# Graph flow visual
search_pill = '<span class="node-pill-search">🌐 web_search</span>' if tavily_key else '<span class="node-pill" style="opacity:0.5">🌐 web_search</span>'
st.markdown(f"""
<div class="graph-flow">
  <span>START</span> <span class="arrow">→</span>
  {search_pill} <span class="arrow">→</span>
  <span class="node-pill">🏢 company_overview</span> <span class="arrow">→</span>
  <span class="node-pill">📊 key_business_info</span> <span class="arrow">→</span>
  <span class="node-pill">⚠️ challenges</span> <span class="arrow">→</span>
  <span class="node-pill">🤖 ai_opportunities</span> <span class="arrow">→</span>
  <span class="node-pill">🎯 pitch_generator</span> <span class="arrow">→</span>
  <span>END</span>
</div>
""", unsafe_allow_html=True)

if not tavily_key:
    st.markdown('<div class="no-tavily-note">💡 <strong>Tip:</strong> Add a free <strong>Tavily API key</strong> in the sidebar to enable real-time web search — the agent will fetch live news and recent data before generating your report.</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    company_name = st.text_input("Company Name", placeholder="e.g. Prestige Group, Adani Realty, Sobha…", label_visibility="collapsed")
with col2:
    run_btn = st.button("▶ Generate Report", disabled=st.session_state.running)

if run_btn and company_name.strip():
    if not groq_key.strip():
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
    else:
        reset_state()
        st.session_state.running = True
        st.rerun()

if run_btn and not company_name.strip():
    st.warning("Please enter a company name.")

# ── Live execution ─────────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    graph = ResearchGraph(
        groq_api_key=groq_key,
        tavily_api_key=tavily_key,
        model=model_choice
    )

    progress_bar = st.progress(0, text="Initialising graph…")
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("#### Graph Execution")
        status_containers = {}
        for key, icon, label in NODES:
            status_containers[key] = st.empty()
            status_containers[key].markdown(
                f'<div class="node-card"><div class="node-header">{icon} {label}'
                f'<span class="status-badge status-waiting">waiting</span></div></div>',
                unsafe_allow_html=True)

    with col_right:
        st.markdown("#### Live Output")
        output_containers = {k: st.empty() for k,_,_ in NODES}

    state = {"company": company_name.strip()}
    total = len(NODES)

    for idx, (key, icon, label) in enumerate(NODES):
        status_containers[key].markdown(
            f'<div class="node-card"><div class="node-header">{icon} {label}'
            f'<span class="status-badge status-running">⏳ running</span></div></div>',
            unsafe_allow_html=True)
        progress_bar.progress(idx / total, text=f"Running: {label}…")

        t0 = time.time()
        try:
            state = graph.run_node(key, state)
            elapsed = round(time.time() - t0, 1)

            # web_search node: check if skipped
            if key == "web_search":
                skipped = "skipped" in state.get("web_search", "")
                badge_class = "status-skipped" if skipped else "status-done"
                badge_text  = "⊘ skipped" if skipped else f"✓ done ({elapsed}s)"
                st.session_state.web_sources = state.get("web_sources", [])
                preview = f"**Sources found:** {len(state.get('web_sources', []))}" if not skipped else "No Tavily key — using LLM training data."
                output_containers[key].markdown(f"**🌐 Web Search**\n\n{preview}")
            else:
                badge_class = "status-done"
                badge_text  = f"✓ done ({elapsed}s)"
                content = state.get(key, "")
                output_containers[key].markdown(
                    f"**{icon} {label}**\n\n{content[:600]}…" if len(content) > 600 else f"**{icon} {label}**\n\n{content}"
                )

            st.session_state.node_status[key] = "done"
            st.session_state.node_output[key] = state.get(key, "")
            st.session_state.node_time[key]   = elapsed
            status_containers[key].markdown(
                f'<div class="node-card"><div class="node-header">{icon} {label}'
                f'<span class="status-badge {badge_class}">{badge_text}</span></div></div>',
                unsafe_allow_html=True)

        except Exception as e:
            st.session_state.node_status[key] = "error"
            st.session_state.error_msg = str(e)
            status_containers[key].markdown(
                f'<div class="node-card"><div class="node-header">{icon} {label}'
                f'<span class="status-badge status-error">✗ error</span></div></div>',
                unsafe_allow_html=True)
            st.error(f"Error in node `{key}`: {e}")
            break

    progress_bar.progress(1.0, text="✅ Report complete!")
    st.session_state.running = False
    st.session_state.done    = True
    time.sleep(0.4)
    st.rerun()

# ── Final Report ───────────────────────────────────────────────────────────────
if st.session_state.done:
    outputs  = st.session_state.node_output
    sources  = st.session_state.web_sources

    st.markdown("---")
    st.markdown("## 📋 Intelligence Report")

    tabs = st.tabs(["🌐 Sources", "🏢 Overview", "📊 Business Info", "⚠️ Challenges", "🤖 AI Opportunities", "🎯 CEO Pitch"])

    with tabs[0]:
        if sources:
            st.markdown(f'<span class="live-badge">🌐 {len(sources)} live sources used</span>', unsafe_allow_html=True)
            st.markdown("")
            for s in sources:
                st.markdown(
                    f'<div class="source-card">📄 <a href="{s["url"]}" target="_blank">{s["title"]}</a>'
                    f'<div class="source-date">🕐 {s.get("date","")}</div></div>',
                    unsafe_allow_html=True)
        else:
            st.info("No live sources — Tavily key was not provided. Add one in the sidebar for real-time data.")

    with tabs[1]: st.markdown(outputs.get("company_overview", "—"))
    with tabs[2]: st.markdown(outputs.get("key_business_info", "—"))
    with tabs[3]: st.markdown(outputs.get("challenges", "—"))
    with tabs[4]: st.markdown(outputs.get("ai_opportunities", "—"))
    with tabs[5]:
        st.markdown("""<div style="background:#f0f4ff;border-left:4px solid #667eea;
            border-radius:8px;padding:1rem 1.2rem;margin-bottom:1rem;font-size:0.85rem;color:#374151;">
            📌 <strong>Personalized CEO Pitch</strong></div>""", unsafe_allow_html=True)
        st.markdown(outputs.get("pitch_generator", "—"))

    # Download
    st.markdown("---")
    sources_md = ""
    if sources:
        sources_md = "\n## Sources (Live Web Data)\n" + "\n".join(
            [f"- [{s['title']}]({s['url']}) — {s.get('date','')}" for s in sources])

    full_report = f"""# AI Intelligence Report: {company_name}
Generated by AI Research Agent (LangGraph × Groq × Tavily)
{sources_md}

---

## 1. Company Overview
{outputs.get('company_overview', '')}

---

## 2. Key Business Information
{outputs.get('key_business_info', '')}

---

## 3. Business Challenges
{outputs.get('challenges', '')}

---

## 4. AI Opportunities
{outputs.get('ai_opportunities', '')}

---

## 5. CEO Pitch
{outputs.get('pitch_generator', '')}
"""
    st.download_button("⬇️ Download Full Report (.md)", data=full_report,
                       file_name=f"{company_name.replace(' ','_')}_report.md", mime="text/markdown")

    if st.button("🔄 New Report"):
        reset_state()
        st.rerun()

# ── Empty state ────────────────────────────────────────────────────────────────
if not st.session_state.running and not st.session_state.done:
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;color:#9ca3af;">
        <div style="font-size:3rem;margin-bottom:1rem;">🔍</div>
        <div style="font-size:1.1rem;font-weight:500;color:#6b7280;">
            Enter a company name and your Groq API key to generate a report
        </div>
        <div style="font-size:0.9rem;margin-top:0.5rem;">
            Add a Tavily key for real-time web search enrichment
        </div>
    </div>
    """, unsafe_allow_html=True)
