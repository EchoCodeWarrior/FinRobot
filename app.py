import streamlit as st
import os
from dotenv import load_dotenv
import autogen
from finrobot.utils import get_current_date, register_keys_from_json
from finrobot.data_source import FinnHubUtils, YFinanceUtils, FMPUtils
from finrobot.toolkits import register_toolkits
from finrobot.functional import ReportChartUtils, ReportAnalysisUtils, ReportLabUtils, TextUtils

# Load environment variables
load_dotenv()

# --- Neo-Brutalism Design System ---
st.set_page_config(layout="wide", page_title="FinRobot Agent", page_icon="📊")

st.markdown("""
<style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Space+Grotesk:wght@500;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
        color: #ffffff;
        font-family: 'Space Mono', monospace;
    }
    
    /* Main Container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Custom Title */
    .neo-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #00FF88;
        text-shadow: 6px 6px 0px #FF00FF, -2px -2px 0px #00FFFF;
        letter-spacing: -2px;
        margin-bottom: 0;
        line-height: 1.1;
    }
    
    .neo-subtitle {
        font-family: 'Space Mono', monospace;
        font-size: 1rem;
        color: #FFD700;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-top: 0.5rem;
        padding: 8px 16px;
        background: rgba(255, 215, 0, 0.1);
        border: 2px solid #FFD700;
        display: inline-block;
    }
    
    /* Buttons - Neo Brutalism */
    .stButton > button {
        background-color: #00FF88 !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        border-radius: 0px !important;
        box-shadow: 8px 8px 0px 0px #000000 !important;
        font-family: 'Space Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        transition: all 0.15s ease !important;
        text-transform: uppercase !important;
        padding: 12px 24px !important;
        letter-spacing: 2px !important;
    }
    .stButton > button:hover {
        transform: translate(-4px, -4px) !important;
        box-shadow: 12px 12px 0px 0px #000000 !important;
        background-color: #00FFFF !important;
    }
    .stButton > button:active {
        transform: translate(4px, 4px) !important;
        box-shadow: 4px 4px 0px 0px #000000 !important;
        background-color: #FF00FF !important;
        color: #ffffff !important;
    }

    /* Text Inputs - Neo Brutalism */
    .stTextInput > div > div > input {
        border: 3px solid #00FF88 !important;
        border-radius: 0px !important;
        box-shadow: 5px 5px 0px 0px #00FF88 !important;
        background-color: rgba(0, 255, 136, 0.05) !important;
        color: #ffffff !important;
        font-family: 'Space Mono', monospace !important;
        font-weight: 700 !important;
        padding: 12px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF00FF !important;
        box-shadow: 8px 8px 0px 0px #FF00FF !important;
        background-color: rgba(255, 0, 255, 0.05) !important;
    }
    
    .stTextInput label {
        color: #00FF88 !important;
        font-family: 'Space Mono', monospace !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
    }
    
    h2 {
        color: #00FFFF !important;
        text-shadow: 3px 3px 0px #FF00FF !important;
    }
    
    h3 {
        color: #FFD700 !important;
        border-left: 6px solid #FFD700;
        padding-left: 16px;
    }
    
    /* Expanders - Neo Style */
    .streamlit-expanderHeader {
        border: 3px solid #00FFFF !important;
        border-radius: 0px !important;
        background-color: rgba(0, 255, 255, 0.1) !important;
        color: #00FFFF !important;
        font-family: 'Space Mono', monospace !important;
        font-weight: 700 !important;
        box-shadow: 4px 4px 0px 0px #00FFFF !important;
    }
    
    /* Tabs - Neo Brutalism */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: rgba(255, 255, 255, 0.05);
        border: 3px solid #ffffff;
        border-radius: 0px;
        box-shadow: 5px 5px 0px 0px rgba(255,255,255,0.3);
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-right: 10px;
        transition: all 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 255, 136, 0.2);
        border-color: #00FF88;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FF00FF !important;
        color: #ffffff !important;
        border-color: #000000 !important;
        transform: translate(-3px, -3px);
        box-shadow: 8px 8px 0px 0px #000000 !important;
    }
    
    /* Sidebar - Neo Style */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d1a 0%, #1a1a2e 100%);
        border-right: 4px solid #00FF88;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #00FF88 !important;
        text-shadow: none !important;
        border-bottom: 3px solid #00FF88;
        padding-bottom: 10px;
    }
    
    /* Info/Warning boxes */
    .stAlert {
        border-radius: 0px !important;
        border: 3px solid !important;
        box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5) !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #00FF88 !important;
    }
    
    /* Success message */
    .stSuccess {
        background-color: rgba(0, 255, 136, 0.2) !important;
        border: 3px solid #00FF88 !important;
        border-radius: 0px !important;
        box-shadow: 5px 5px 0px 0px #00FF88 !important;
    }
    
    /* Error message */
    .stError {
        background-color: rgba(255, 0, 100, 0.2) !important;
        border: 3px solid #FF0064 !important;
        border-radius: 0px !important;
        box-shadow: 5px 5px 0px 0px #FF0064 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, #00FF88, #00FFFF, #FF00FF);
        margin: 2rem 0;
    }
    
    /* IMPORTANT: Text visibility fixes */
    p, span, li, div {
        color: #ffffff !important;
    }
    
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #e0e0e0 !important;
    }
    
    /* Placeholder text */
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
        font-style: italic;
    }
    
    /* Labels and help text */
    .stTextInput label p {
        color: #00FF88 !important;
    }
    
    small, .stHelp {
        color: #888888 !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] li {
        color: #ffffff !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 2px solid #00FFFF !important;
        border-top: none !important;
    }
    
    .streamlit-expanderContent p {
        color: #e0e0e0 !important;
    }
    
    /* Card Style */
    .neo-card {
        background: rgba(255, 255, 255, 0.03);
        border: 4px solid #00FF88;
        padding: 24px;
        box-shadow: 10px 10px 0px 0px #000000;
        margin: 20px 0;
    }
    
    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 255, 255, 0.05) 100%);
        border: 4px solid #00FF88;
        padding: 24px;
        box-shadow: 10px 10px 0px 0px rgba(0, 255, 136, 0.5);
        font-family: 'Space Mono', monospace;
        color: #ffffff;
        line-height: 1.8;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 class="neo-title">FINROBOT<br/>AGENTIC ANALYST</h1>
    <div class="neo-subtitle">🇮🇳 INDIAN STOCK MARKET // NSE & BSE</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ SYSTEM CONFIG")
    st.markdown("---")
    
    groq_api_key = st.text_input("� GROQ API KEY", value=os.environ.get("GROQ_API_KEY", ""), type="password", help="Get free key at console.groq.com")
    fmp_api_key = st.text_input("📊 FMP API KEY", value=os.environ.get("FMP_API_KEY", ""), type="password", help="Financial Modeling Prep")
    finnhub_api_key = st.text_input("📈 FINNHUB API KEY", value=os.environ.get("FINNHUB_API_KEY", ""), type="password", help="Finnhub Stock Data")
    
    st.markdown("---")
    
    # Status indicators
    st.markdown("### 🔌 CONNECTION STATUS")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if groq_api_key:
            st.markdown("🟢 **GROQ**")
        else:
            st.markdown("🔴 **GROQ**")
    with col_s2:
        if fmp_api_key:
            st.markdown("🟢 **FMP**")
        else:
            st.markdown("🔴 **FMP**")
    
    if finnhub_api_key:
        st.markdown("🟢 **FINNHUB**")
    else:
        st.markdown("🔴 **FINNHUB**")

# Environment Setup
if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key
if fmp_api_key:
    os.environ["FMP_API_KEY"] = fmp_api_key
if finnhub_api_key:
    os.environ["FINNHUB_API_KEY"] = finnhub_api_key

# Check for keys
missing_keys = []
if not groq_api_key: missing_keys.append("Groq")
if not fmp_api_key: missing_keys.append("FMP")
if not finnhub_api_key: missing_keys.append("Finnhub")

if missing_keys:
    st.warning(f"⚠️ MISSING API KEYS: {', '.join(missing_keys)}")

# --- Helper Functions ---
def get_llm_config():
    # Using Groq with Llama 3.1 8B Instant (14.4K requests/day free!)
    config_list = [
        {
            "model": "llama-3.1-8b-instant",
            "api_key": os.environ.get("GROQ_API_KEY"),
            "base_url": "https://api.groq.com/openai/v1"
        }
    ]
    return {
        "config_list": config_list,
        "timeout": 120,
        "temperature": 0.5,
    }

# Tabs
tab1, tab2 = st.tabs(["📈 MARKET FORECASTER", "📋 ANNUAL REPORT"])

with tab1:
    st.markdown("### 🚀 MARKET MOMENTUM PREDICTOR")
    st.markdown("*AI-powered stock analysis using real-time market data*")
    st.markdown("---")
    
    # Content layout
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### CONFIGURATION")
        ticker_1 = st.text_input("TICKER SYMBOL", value="", placeholder="Enter ticker (e.g., RELIANCE.NS)", help="E.g., RELIANCE.NS, TCS.NS, INFY.NS", key="ticker1")
        st.markdown("")
        run_btn_1 = st.button("⚡ RUN FORECAST", key="btn1", use_container_width=True)
        
        st.markdown("---")
        st.markdown("##### 💡 TIPS")
        st.markdown("""
        - Use `.NS` suffix for NSE stocks
        - Use `.BO` suffix for BSE stocks
        - Example: `TCS.NS`, `INFY.NS`
        """)
    
    with col2:
        output_1 = st.empty()

        
    if run_btn_1 and not missing_keys:
        with st.spinner("AGENTS DEPLOYED. ANALYZING MARKET DATA..."):
            try:
                # Agent Configuration
                llm_config = get_llm_config()
                
                # 1. Market Analyst Agent
                analyst = autogen.AssistantAgent(
                    name="Market_Analyst",
                    system_message="As a Market Analyst for the Indian Stock Market (NSE/BSE), you possess strong analytical abilities. "
                    "Collect financial info and news using provided tools. "
                    "Focus on Indian market context, regulatory updates (SEBI), and local economic factors. "
                    "Reply TERMINATE when the task is done.",
                    llm_config=llm_config,
                )

                # 2. User Proxy Agent
                user_proxy = autogen.UserProxyAgent(
                    name="User_Proxy",
                    human_input_mode="NEVER",
                    max_consecutive_auto_reply=10,
                    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").strip().endswith("TERMINATE"),
                    code_execution_config={
                        "work_dir": "coding",
                        "use_docker": False,
                    }, 
                )
                
                # Register Tools
                tools = [
                    {"function": FinnHubUtils.get_company_profile, "name": "get_company_profile", "description": "get company profile"},
                    {"function": FinnHubUtils.get_company_news, "name": "get_company_news", "description": "get company news"},
                    {"function": FinnHubUtils.get_basic_financials, "name": "get_financial_basics", "description": "get financial basics"},
                    {"function": YFinanceUtils.get_stock_data, "name": "get_stock_data", "description": "get stock data"}
                ]
                register_toolkits(tools, analyst, user_proxy)
                
                # Prompt Construction
                today = get_current_date()
                company = ticker_1
                prompt = (
                    f"Use all tools to retrieve info for {company} (Indian Stock) as of {today}. "
                    f"Analyze positive developments and concerns (focus on Indian market impact). "
                    f"Make a prediction (up/down %) for next week. Provide a summary."
                )
                
                # Run Chat
                chat_res = user_proxy.initiate_chat(
                    analyst,
                    message=prompt,
                    summary_method="reflection_with_llm",
                )
                
                # Display Output
                with output_1.container():
                    st.success("ANALYSIS COMPLETE")
                    
                    # Extract the summary or last message
                    summary = chat_res.summary
                    st.markdown(f"### 📊 FORECAST REPORT // {company}")
                    st.markdown(f"""
                    <div class="result-card">
                        {summary}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("VIEW FULL CONVERSATION LOG"):
                        for msg in chat_res.chat_history:
                            role = msg['role'].upper()
                            content = msg['content']
                            if content:
                                st.markdown(f"**{role}:** {content}")
                                st.divider()
                                
            except Exception as e:
                st.error(f"EXECUTION FAILED: {str(e)}")
    elif run_btn_1:
         st.error("CONFIGURE API KEYS IN SIDEBAR FIRST.")

with tab2:
    st.markdown("### 📋 ANNUAL REPORT DEEP DIVE")
    st.markdown("*Comprehensive financial analysis using AI-powered document parsing*")
    st.markdown("---")
    
    col1_2, col2_2 = st.columns([1, 2])
    with col1_2:
        st.markdown("#### CONFIGURATION")
        ticker_2 = st.text_input("COMPANY TICKER", value="", placeholder="Enter ticker (e.g., TCS.NS)", help="E.g., TCS.NS, INFY.NS", key="ticker2")
        st.markdown("")
        run_btn_2 = st.button("📄 ANALYZE REPORT", key="btn2", use_container_width=True)
        
        st.markdown("---")
        st.markdown("##### 📊 ANALYSIS INCLUDES")
        st.markdown("""
        - Balance Sheet Analysis
        - Income Statement Review
        - Cash Flow Assessment
        - Investment Recommendation
        """)
        
    with col2_2:
        output_2 = st.empty()
        
    if run_btn_2 and not missing_keys:
        with st.spinner("FETCHING AND ANALYZING ANNUAL REPORT..."):
            try:
                # Agent Configuration
                llm_config = get_llm_config()
                
                # Agents
                expert = autogen.AssistantAgent(
                    name="Expert_Investor",
                    system_message="Role: Expert Investor for Indian Markets. "
                    "Responsibility: Generate Customized Financial Analysis Reports. "
                    "Use tools to fetch financial statements (Balance Sheet, Income Stmt, Cash Flow). "
                    "If SEC 10-K is not available (common for Indian stocks), use FMP financial statements directly. "
                    "Reply TERMINATE when detailed analysis is done.",
                    llm_config=llm_config,
                )
                
                user_proxy_rep = autogen.UserProxyAgent(
                    name="User_Proxy_Report",
                    human_input_mode="NEVER",
                    max_consecutive_auto_reply=10,
                    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").strip().endswith("TERMINATE"),
                    code_execution_config={
                        "work_dir": "report_coding",
                        "use_docker": False,
                    },
                )
                        
                # Register Tools
                # We register basic financial tools + report tools
                # Note: FMPUtils.get_sec_report might fail for NS tickers, so we emphasize financial statement analysis
                tools_rep = [
                    {"function": FMPUtils.get_sec_report, "name": "get_sec_report", "description": "get SEC report"},
                    {"function": ReportAnalysisUtils.analyze_balance_sheet, "name": "analyze_balance_sheet", "description": "analyze balance sheet"},
                    {"function": ReportAnalysisUtils.analyze_income_stmt, "name": "analyze_income_stmt", "description": "analyze income statement"},
                    {"function": ReportAnalysisUtils.analyze_cash_flow, "name": "analyze_cash_flow", "description": "analyze cash flow"},
                    {"function": ReportAnalysisUtils.analyze_business_highlights, "name": "analyze_business_highlights", "description": "analyze business highlights"},
                    {"function": TextUtils.check_text_length, "name": "check_text_length", "description": "check text length"},
                ]
                register_toolkits(tools_rep, expert, user_proxy_rep)
                
                # Prompt
                company_2 = ticker_2
                year = "2024" # Default to recent
                prompt_rep = (
                    f"Analyze the financial health of {company_2} (Indian Stock) for the year {year}. "
                    f"1. Retrieve/Analyze Balance Sheet, Income Statement, and Cash Flow. "
                    f"2. Summarize key financial metrics (Profitability, Liquidity, Solvency). "
                    f"3. Provide an investment recommendation based on these metrics. "
                    f"Format the output as a structured Annual Performance Report."
                )
                
                # Run Chat
                chat_res_rep = user_proxy_rep.initiate_chat(
                    expert,
                    message=prompt_rep,
                    summary_method="reflection_with_llm",
                )
                
                # Output
                with output_2.container():
                    st.success("REPORT GENERATION COMPLETE")
                    summary_rep = chat_res_rep.summary
                    
                    st.markdown(f"### 📈 ANNUAL PERFORMANCE REPORT // {company_2}")
                    st.markdown(f"""
                    <div class="result-card">
                        {summary_rep}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("VIEW ANALYSIS STEPS"):
                        for msg in chat_res_rep.chat_history:
                            role = msg['role'].upper()
                            content = msg['content']
                            if content:
                                st.markdown(f"**{role}:** {content}")
                                st.divider()

            except Exception as e:
                st.error(f"EXECUTION FAILED: {str(e)}")
    elif run_btn_2:
        st.error("CONFIGURE API KEYS IN SIDEBAR FIRST.")

