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
st.set_page_config(layout="wide", page_title="FinRobot Agent")

st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #ffffff;
        color: #000000;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #FFDE00; /* Bright Yellow */
        color: #000000;
        border: 4px solid #000000;
        border-radius: 0px;
        box-shadow: 6px 6px 0px 0px #000000;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.1s;
        text-transform: uppercase;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 8px 8px 0px 0px #000000;
        border-color: #000000;
        background-color: #FFDE00;
        color: #000000;
    }
    .stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px 0px #000000;
        background-color: #00FFFF; /* Cyan on click */
    }

    /* Inputs */
    .stTextInput > div > div > input {
        border: 3px solid #000000;
        border-radius: 0px;
        box-shadow: 4px 4px 0px 0px #000000;
        background-color: #ffffff;
        color: #000000;
        font-weight: bold;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FF00FF; /* Magenta */
        box-shadow: 6px 6px 0px 0px #000000;
    }

    /* Headers */
    h1, h2, h3 {
        color: #000000;
        text-transform: uppercase;
        font-weight: 900;
        text-shadow: 3px 3px 0px #FF00FF; /* Magenta Shadow */
    }
    
    /* Expanders/Containers */
    .streamlit-expanderHeader {
        border: 3px solid #000000;
        border-radius: 0px;
        background-color: #00FFFF; /* Cyan */
        color: #000000;
        font-weight: bold;
        box-shadow: 4px 4px 0px 0px #000000;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border: 3px solid #000000;
        border-radius: 0px;
        box-shadow: 4px 4px 0px 0px #000000;
        font-weight: bold;
        color: #000000;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FF00FF; /* Magenta */
        color: #ffffff;
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px 0px #000000;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f0f0;
        border-right: 4px solid #000000;
    }

</style>
""", unsafe_allow_html=True)

# --- App Logic ---
st.title("FINROBOT /// AGENTIC ANALYST")
st.caption("INDIAN STOCK MARKET FOCUS // NSE & BSE")

# Sidebar Configuration
with st.sidebar:
    st.header("SYSTEM CONFIG")
    st.markdown("---")
    
    google_api_key = st.text_input("GOOGLE API KEY", value=os.environ.get("GOOGLE_API_KEY", ""), type="password", help="For Gemini 1.5 Pro")
    fmp_api_key = st.text_input("FMP API KEY", value=os.environ.get("FMP_API_KEY", ""), type="password", help="Financial Modeling Prep")
    finnhub_api_key = st.text_input("FINNHUB API KEY", value=os.environ.get("FINNHUB_API_KEY", ""), type="password", help="Finnhub Stock Data")
    
    st.markdown("---")
    st.info("Ensure all keys are set for agents to function correctly.")

# Environment Setup
if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key
if fmp_api_key:
    os.environ["FMP_API_KEY"] = fmp_api_key
if finnhub_api_key:
    os.environ["FINNHUB_API_KEY"] = finnhub_api_key

# Check for keys
missing_keys = []
if not google_api_key: missing_keys.append("Google")
if not fmp_api_key: missing_keys.append("FMP")
if not finnhub_api_key: missing_keys.append("Finnhub")

if missing_keys:
    st.warning(f"MISSING API KEYS: {', '.join(missing_keys)}")

# --- Helper Functions ---
def get_llm_config():
    # Configuring for Gemini via AutoGen
    # Use gemini-1.5-pro as requested (fallback) or preview if available.
    # Note: As of late 2024/2025, AutoGen supports gemini via api_type="google" or "genai" depending on version.
    # We will use the standard config list format.
    config_list = [
        {
            "model": "gemini-1.5-pro",
            "api_key": os.environ.get("GOOGLE_API_KEY"),
            "api_type": "google" 
        }
    ]
    return {
        "config_list": config_list,
        "timeout": 120,
        "temperature": 0.5,
    }

# Tabs
tab1, tab2 = st.tabs(["MARKET FORECASTER", "ANNUAL REPORT ANALYZER"])

with tab1:
    st.subheader("/// MARKET MOMENTUM PREDICTOR")
    # Content placeholder
    col1, col2 = st.columns([1, 2])
    with col1:
        ticker_1 = st.text_input("TICKER SYMBOL", value="RELIANCE.NS", help="E.g., RELIANCE.NS, TCS.NS, INFY.NS")
        run_btn_1 = st.button("RUN FORECAST", key="btn1")
    
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
                    st.markdown(f"### FORECAST REPORT // {company}")
                    st.markdown(f"""
                    <div style="border: 3px solid black; padding: 20px; box-shadow: 5px 5px 0px 0px #000000;">
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
    st.subheader("/// 10-K / ANNUAL REPORT DEEP DIVE")
    # Content placeholder
    col1_2, col2_2 = st.columns([1, 2])
    with col1_2:
        ticker_2 = st.text_input("COMPANY TICKER", value="TCS.NS", help="E.g., TCS.NS, INFY.NS")
        run_btn_2 = st.button("ANALYZE REPORT", key="btn2")
        
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
                    
                    st.markdown(f"### ANNUAL PERFORMANCE REPORT // {company_2}")
                    st.markdown(f"""
                    <div style="border: 3px solid black; padding: 20px; box-shadow: 5px 5px 0px 0px #000000; background-color: #f9f9f9;">
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

