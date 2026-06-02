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
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .node-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .node-header {
        font-weight: 600;
        font-size: 0.95rem;
        color: #374151;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .status-badge {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 999px;
        font-weight: 500;
    }
    .status-waiting  { background: #f3f4f6; color: #6b7280; }
    .status-running  { background: #fef3c7; color: #92400e; }
    .status-done     { background: #d1fae5; color: #065f46; }
    .status-error    { background: #fee2e2; color: #991b1b; }
    .graph-flow {
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
        padding: 0.8rem;
        background: #f1f5f9;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        font-size: 0.82rem;
        color: #475569;
        font-family: monospace;
    }
    .node-pill {
        background: white;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 3px 10px;
        font-weight: 500;
    }
    .arrow { color: #94a3b8; }
    .section-divider {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1.5rem 0;
    }
    .report-section {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
    }
    .report-section h3 {
        color: #1e293b;
        font-size: 1.05rem;
        margin-top: 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    .pitch-box {
        background: linear-gradient(135deg, #667eea15, #764ba215);
        border: 1px solid #667eea40;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
    }
    .stButton > button:hover {
        opacity: 0.9;
        border: none;
    }
    .time-badge {
        font-size: 0.75rem;
        color: #9ca3af;
        float: right;
    }
</style>
""", unsafe_allow_html=True)


NODES = [
    ("company_overview",    "🏢", "Company Overview"),
    ("key_business_info",   "📊", "Key Business Info"),
    ("challenges",          "⚠️",  "Business Challenges"),
    ("ai_opportunities",    "🤖", "AI Opportunities"),
    ("pitch_generator",     "🎯", "CEO Pitch"),
]


def init_session():
    if "node_status" not in st.session_state:
        st.session_state.node_status = {k: "waiting" for k, _, _ in NODES}
    if "node_output" not in st.session_state:
        st.session_state.node_output = {k: "" for k, _, _ in NODES}
    if "node_time" not in st.session_state:
        st.session_state.node_time = {k: 0.0 for k, _, _ in NODES}
    if "running" not in st.session_state:
        st.session_state.running = False
    if "done" not in st.session_state:
        st.session_state.done = False
    if "error_msg" not in st.session_state:
        st.session_state.error_msg = ""


def reset_state():
    st.session_state.node_status = {k: "waiting" for k, _, _ in NODES}
    st.session_state.node_output = {k: "" for k, _, _ in NODES}
    st.session_state.node_time  = {k: 0.0 for k, _, _ in NODES}
    st.session_state.running = False
    st.session_state.done    = False
    st.session_state.error_msg = ""


init_session()

with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    groq_key = st.text_input("Groq API Key", type="password",
                              placeholder="gsk_...",
                              help="Get free key at console.groq.com")

    model_choice = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )

    st.markdown("---")
    st.markdown("### 🔗 LangGraph Flow")
    st.markdown("""
```
START
  ↓
company_overview
  ↓
key_business_info
  ↓
challenges
  ↓
ai_opportunities
  ↓
pitch_generator
  ↓
END
```
    """)

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
**Stack:**
- 🦜 LangGraph (state machine)
- ⚡ Groq (LLM inference)
- 🖥️ Streamlit (UI)

Each node is a LangGraph state
node that enriches a shared
`AgentState` dict passed along
the chain.
    """)

st.markdown('<div class="main-title">🔍 AI Research & Recommendation Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">LangGraph × Groq — generates structured intelligence reports for any company</div>', unsafe_allow_html=True)


st.markdown("""
<div class="graph-flow">
  <span>START</span>
  <span class="arrow">→</span>
  <span class="node-pill">company_overview</span>
  <span class="arrow">→</span>
  <span class="node-pill">key_business_info</span>
  <span class="arrow">→</span>
  <span class="node-pill">challenges</span>
  <span class="arrow">→</span>
  <span class="node-pill">ai_opportunities</span>
  <span class="arrow">→</span>
  <span class="node-pill">pitch_generator</span>
  <span class="arrow">→</span>
  <span>END</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g. Prestige Group, Adani Realty, Sobha, Brigade Group …",
        label_visibility="collapsed"
    )
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

if st.session_state.running and not st.session_state.done:
    graph = ResearchGraph(api_key=groq_key, model=model_choice)

    progress_bar = st.progress(0, text="Initialising graph…")
    status_containers = {}

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("#### Graph Execution")
        for key, icon, label in NODES:
            status_containers[key] = st.empty()
            status_containers[key].markdown(
                f'<div class="node-card"><div class="node-header">'
                f'{icon} {label}'
                f'<span class="status-badge status-waiting">waiting</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )

    with col_right:
        st.markdown("#### Live Output")
        output_containers = {k: st.empty() for k, _, _ in NODES}

    state = {"company": company_name.strip()}
    total = len(NODES)

    for idx, (key, icon, label) in enumerate(NODES):
        st.session_state.node_status[key] = "running"
        status_containers[key].markdown(
            f'<div class="node-card"><div class="node-header">'
            f'{icon} {label}'
            f'<span class="status-badge status-running">⏳ running</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )
        progress_bar.progress((idx) / total, text=f"Running: {label}…")

        t0 = time.time()
        try:
            state = graph.run_node(key, state)
            elapsed = round(time.time() - t0, 1)
            st.session_state.node_status[key] = "done"
            st.session_state.node_output[key] = state.get(key, "")
            st.session_state.node_time[key]   = elapsed

            status_containers[key].markdown(
                f'<div class="node-card"><div class="node-header">'
                f'{icon} {label}'
                f'<span class="status-badge status-done">✓ done ({elapsed}s)</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )
            output_containers[key].markdown(
                f"**{icon} {label}**\n\n{state.get(key, '')[:600]}…"
                if len(state.get(key, "")) > 600 else
                f"**{icon} {label}**\n\n{state.get(key, '')}"
            )

        except Exception as e:
            st.session_state.node_status[key] = "error"
            st.session_state.error_msg = str(e)
            status_containers[key].markdown(
                f'<div class="node-card"><div class="node-header">'
                f'{icon} {label}'
                f'<span class="status-badge status-error">✗ error</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )
            st.error(f"Error in node `{key}`: {e}")
            break

    progress_bar.progress(1.0, text="✅ Report complete!")
    st.session_state.running = False
    st.session_state.done    = True
    time.sleep(0.5)
    st.rerun()



if st.session_state.done:
    outputs = st.session_state.node_output

    st.markdown("---")
    st.markdown(f"## 📋 Intelligence Report")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 Overview", "📊 Business Info", "⚠️ Challenges", "🤖 AI Opportunities", "🎯 CEO Pitch"
    ])

    with tab1:
        st.markdown(outputs.get("company_overview", "—"))

    with tab2:
        st.markdown(outputs.get("key_business_info", "—"))

    with tab3:
        st.markdown(outputs.get("challenges", "—"))

    with tab4:
        st.markdown(outputs.get("ai_opportunities", "—"))

    with tab5:
        st.markdown("""
        <div style="background:#f0f4ff;border-left:4px solid #667eea;
                    border-radius:8px;padding:1rem 1.2rem;margin-bottom:1rem;
                    font-size:0.85rem;color:#374151;">
        📌 <strong>Personalized CEO Pitch</strong> — ready to use in a meeting or email.
        </div>""", unsafe_allow_html=True)
        st.markdown(outputs.get("pitch_generator", "—"))

    # Download
    st.markdown("---")
    full_report = f"""# AI Intelligence Report: {company_name}
Generated by AI Research Agent (LangGraph × Groq)

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
    st.download_button(
        "⬇️ Download Full Report (.md)",
        data=full_report,
        file_name=f"{company_name.replace(' ', '_')}_report.md",
        mime="text/markdown"
    )

    if st.button("🔄 New Report"):
        reset_state()
        st.rerun()


if not st.session_state.running and not st.session_state.done:
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;color:#9ca3af;">
        <div style="font-size:3rem;margin-bottom:1rem;">🔍</div>
        <div style="font-size:1.1rem;font-weight:500;color:#6b7280;">
            Enter a company name and your Groq API key to generate a report
        </div>
        <div style="font-size:0.9rem;margin-top:0.5rem;">
            Works with any company — real estate, tech, retail, manufacturing…
        </div>
    </div>
    """, unsafe_allow_html=True)
