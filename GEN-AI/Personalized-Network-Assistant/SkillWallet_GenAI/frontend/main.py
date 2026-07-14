import streamlit as st
import requests
import pandas as pd
import json

# Setup page config
st.set_page_config(
    page_title="Personalized Networking Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API URL definition
API_URL = "http://127.0.0.1:8000"

# Inject Custom CSS for Premium Design aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Universal Font override */
    html, body, p, h1, h2, h3, h4, h5, h6, textarea, input, label, button {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Global Page Background styling */
    .stApp {
        background: linear-gradient(135deg, #0a071b 0%, #120e2e 50%, #05030c 100%) !important;
        color: #F3F3F3 !important;
    }
    
    /* Custom Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(8, 6, 21, 0.96) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Sidebar Navigation Menu overhaul (Radio buttons to Nav links) */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        padding: 5px 0 !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 12px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        cursor: pointer !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(108, 93, 211, 0.1) !important;
        border-color: rgba(108, 93, 211, 0.4) !important;
        transform: translateX(4px) !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(90deg, rgba(108, 93, 211, 0.22) 0%, rgba(0, 198, 255, 0.12) 100%) !important;
        border-color: #6C5DD3 !important;
        box-shadow: 0 4px 15px rgba(108, 93, 211, 0.2) !important;
    }
    /* Hide default radio elements */
    [data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stWidgetSecondaryContainer"] {
        display: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label > div:not(:has([data-testid="stMarkdownContainer"])) {
        display: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label > span:not(:has([data-testid="stMarkdownContainer"])) {
        display: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stMarkdownContainer"] p {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: #FFFFFF !important;
        margin: 0 !important;
    }
    
    /* Title widget label of Navigation in sidebar */
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] label {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #A180F4 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        margin-bottom: 12px !important;
    }
    
    /* Heading Styling */
    .app-title {
        background: linear-gradient(135deg, #b094ff 0%, #4D96FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.2rem;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
        filter: drop-shadow(0 2px 10px rgba(176, 148, 255, 0.15));
    }
    .app-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #A0A0B0;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: #4D96FF;
        margin-top: 15px;
        margin-bottom: 20px;
        letter-spacing: -0.2px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        padding-bottom: 8px;
    }
    
    /* Beautiful Glassmorphic card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        position: relative;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #A180F4, #00C6FF);
        opacity: 0.7;
        border-radius: 16px 16px 0 0;
    }
    .glass-card:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(161, 128, 244, 0.35) !important;
        box-shadow: 0 16px 36px 0 rgba(161, 128, 244, 0.15) !important;
    }
    
    /* Elegant tag styling */
    .theme-tag {
        background: linear-gradient(135deg, rgba(108, 93, 211, 0.3) 0%, rgba(0, 198, 255, 0.2) 100%);
        border: 1px solid rgba(108, 93, 211, 0.5);
        color: #FFFFFF;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
        margin-right: 10px;
        margin-bottom: 10px;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(108, 93, 211, 0.25);
        transition: all 0.2s ease;
    }
    .theme-tag:hover {
        transform: scale(1.05);
        border-color: #00C6FF;
    }
    
    /* Custom container padding */
    .starter-text {
        font-size: 1.15rem;
        font-style: italic;
        line-height: 1.7;
        color: #FFFFFF;
        border-left: 3px solid #A180F4;
        padding-left: 18px;
        margin: 12px 0px;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Styling input fields and wrappers */
    div[data-baseweb="textarea"], div[data-baseweb="input"] {
        border: none !important;
        background: transparent !important;
    }
    textarea, input[type="text"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        padding: 12px !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #A180F4 !important;
        box-shadow: 0 0 18px rgba(161, 128, 244, 0.3) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Input field label overriding */
    [data-testid="stWidgetLabel"] p {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #4D96FF !important;
        margin-bottom: 6px !important;
    }
    
    /* Button Custom styling */
    div.stButton > button {
        border-radius: 12px !important;
        padding: 10px 22px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    /* Primary buttons (Submit/Generate/Verify) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6C5DD3 0%, #00C6FF 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(108, 93, 211, 0.3) !important;
        width: 100%;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(108, 93, 211, 0.5), 0 0 15px rgba(0, 198, 255, 0.4) !important;
        color: #FFFFFF !important;
    }
    div.stButton > button[kind="primary"]:active {
        transform: translateY(1px) !important;
    }
    /* Secondary buttons (Unselected Feedback / default secondary) */
    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #A0A0B0 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        width: 100%;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Metric Card Grid Dashboard style */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-bottom: 35px;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 12px 30px rgba(0,0,0,0.35);
    }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0; height: 4px;
    }
    .metric-card.purple::after { background: #A180F4; }
    .metric-card.blue::after { background: #00C6FF; }
    .metric-card.green::after { background: #2ECC71; }
    .metric-card.yellow::after { background: #F1C40F; }
    
    .metric-title {
        font-size: 0.85rem;
        color: #A0A0B0;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
    }
    .metric-value.green-val {
        color: #2ECC71;
        text-shadow: 0 0 15px rgba(46,204,113,0.2);
    }
    .metric-value.yellow-val {
        color: #F1C40F;
        text-shadow: 0 0 15px rgba(241,196,15,0.2);
    }
    
    /* Scrollbars customization */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.01);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(161, 128, 244, 0.2);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(161, 128, 244, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Helper function to submit feedback to the backend API
def submit_feedback(record_id, api_val):
    try:
        response = requests.post(
            f"{API_URL}/api/history/{record_id}/feedback",
            json={"feedback": api_val}
        )
        if response.status_code == 200:
            return True
    except Exception as e:
        st.error(f"Error submitting feedback: {e}")
    return False

# Sidebar layout
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #4D96FF; margin-top: 10px; font-weight: 800;'>💡 AI Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 15px 0;' />", unsafe_allow_html=True)
    
    # Navigation
    menu = st.radio(
        "Navigation Menu",
        ["💬 Smart Starter Generator", "🔍 Wikipedia Fact Check", "📊 History & Analytics"],
        index=0
    )
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 20px 0;' />", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; font-weight: 700; color: #A180F4; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 12px;'>System Health</p>", unsafe_allow_html=True)
    
    # Simple ping to backend
    api_online = False
    try:
        res = requests.get(API_URL, timeout=3)
        if res.status_code == 200:
            api_online = True
    except requests.exceptions.RequestException:
        api_online = False

    if api_online:
        st.markdown("""
        <div style="display: flex; align-items: center; background: rgba(46, 204, 113, 0.1); border: 1px solid rgba(46, 204, 113, 0.25); padding: 10px 14px; border-radius: 12px; margin-bottom: 15px;">
            <span style="height: 8px; width: 8px; background-color: #2ECC71; border-radius: 50%; display: inline-block; margin-right: 12px; box-shadow: 0 0 10px #2ECC71;"></span>
            <span style="font-size: 0.9rem; font-weight: 600; color: #2ECC71; letter-spacing: 0.2px;">Backend: Online</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display: flex; align-items: center; background: rgba(231, 76, 60, 0.1); border: 1px solid rgba(231, 76, 60, 0.25); padding: 10px 14px; border-radius: 12px; margin-bottom: 15px;">
            <span style="height: 8px; width: 8px; background-color: #E74C3C; border-radius: 50%; display: inline-block; margin-right: 12px; box-shadow: 0 0 10px #E74C3C;"></span>
            <span style="font-size: 0.9rem; font-weight: 600; color: #E74C3C; letter-spacing: 0.2px;">Backend: Offline</span>
        </div>
        """, unsafe_allow_html=True)
        st.info("Start the FastAPI backend to use the application functionality.")

# Main app title display
st.markdown("<h1 class='app-title'>Personalized Networking Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='app-subtitle'>Generate smart conversation starters and verify background facts instantly</p>", unsafe_allow_html=True)

# ----------------- Tab 1: Generate Starters -----------------
if menu == "💬 Smart Starter Generator":
    st.markdown("<div class='section-header'>Generate Smart Starters</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("<p style='color: #B2B2B2; font-size: 1rem; margin-bottom: 20px;'>Enter the details of the networking event and your target goals or professional topics.</p>", unsafe_allow_html=True)
        
        event_desc = st.text_area(
            "Event Description", 
            placeholder="e.g. AI for Sustainable Cities conference focusing on climate resilience, smart transit, and urban layout optimization.",
            height=120,
            help="Describe the event topic, target audience, or theme."
        )
        
        interests = st.text_input(
            "Your Interests / Goals", 
            placeholder="e.g. climate change, urban planning, machine learning",
            help="Comma-separated topics you want to talk about or goals you want to achieve."
        )
        
        # Spacer
        st.write("")
        generate_btn = st.button("Generate Tailored Starters 🚀", use_container_width=True, type="primary")
        
    with col2:
        if generate_btn:
            if not event_desc.strip():
                st.error("Please enter a valid event description.")
            elif not interests.strip():
                st.error("Please enter at least one interest or goal.")
            elif not api_online:
                st.error("Cannot connect to backend server. Make sure the FastAPI app is running.")
            else:
                with st.spinner("Analyzing event themes and generating conversation starters..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/api/starters/generate",
                            json={
                                "event_description": event_desc,
                                "interests": interests
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            record_id = data["id"]
                            extracted_themes = data["extracted_themes"]
                            starters = data["starters"]
                            
                            st.success("Analysis Complete!")
                            
                            # Display extracted themes
                            st.markdown("<h3 style='font-size: 1.25rem; font-weight: 600; color: #4D96FF; margin-top: 15px; margin-bottom: 12px;'>Extracted Event Themes</h3>", unsafe_allow_html=True)
                            theme_html = "<div>"
                            for theme in extracted_themes:
                                theme_html += f"<span class='theme-tag'>{theme}</span>"
                            theme_html += "</div>"
                            st.markdown(theme_html, unsafe_allow_html=True)
                            
                            st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 20px 0;' />", unsafe_allow_html=True)
                            
                            # Display starters
                            st.markdown("<h3 style='font-size: 1.25rem; font-weight: 600; color: #4D96FF; margin-bottom: 15px;'>Generated Starters</h3>", unsafe_allow_html=True)
                            for idx, starter in enumerate(starters):
                                st.markdown(f"""
                                <div class='glass-card'>
                                    <div style='font-size: 0.85rem; color: #A180F4; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;'>PROMPT #{idx+1}</div>
                                    <div class='starter-text'>"{starter}"</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            st.info("💡 Tip: Visit the **History** tab to rate these starters and see past strategies!")
                        else:
                            st.error(f"Backend API error: {response.text}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")
        else:
            st.markdown("""
            <div style='border: 1px dashed rgba(255,255,255,0.12); border-radius: 16px; padding: 50px 30px; text-align: center; color: #888; background: rgba(255,255,255,0.01);'>
                <div style="font-size: 3rem; margin-bottom: 15px;">✨</div>
                <h3 style='margin-bottom: 8px; color: #FFFFFF; font-weight: 600;'>Ready to Generate</h3>
                <p style="font-size: 0.95rem; max-width: 400px; margin: 0 auto;">Fill out the parameters on the left and click 'Generate Tailored Starters' to see AI suggestions.</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- Tab 2: Fact Checking -----------------
elif menu == "🔍 Wikipedia Fact Check":
    st.markdown("<div class='section-header'>Quick Fact Verification</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B2B2B2; font-size: 1rem; margin-bottom: 25px;'>Attend networking events with absolute confidence. Check names, technologies, or concepts instantly using the live Wikipedia verification utility.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3], gap="large")
    
    with col1:
        query = st.text_input(
            "Verify Topic / Fact", 
            placeholder="e.g. blockchain in healthcare, zero shot learning, IPCC climate reports"
        )
        st.write("")
        verify_btn = st.button("Check Reference 🔍", use_container_width=True, type="primary")
        
    with col2:
        if verify_btn:
            if not query.strip():
                st.error("Please enter a query to search.")
            elif not api_online:
                st.error("Backend server is offline.")
            else:
                with st.spinner("Searching and summarizing Wikipedia articles..."):
                    try:
                        response = requests.get(f"{API_URL}/api/facts/verify", params={"query": query})
                        if response.status_code == 200:
                            data = response.json()
                            if data.get("found"):
                                st.markdown(f"""
                                <div class='glass-card'>
                                    <h3 style='margin-top:0; color: #00C6FF; font-weight: 700; font-size: 1.4rem; margin-bottom: 12px;'>{data['title']}</h3>
                                    <p style='line-height: 1.7; font-size: 1rem; color: #E0E0E0; margin-bottom: 20px;'>{data['summary']}</p>
                                    <hr style='border-color: rgba(255,255,255,0.08); margin: 15px 0;' />
                                    <a href='{data['url']}' target='_blank' style='color: #4D96FF; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center;'>Read full article on Wikipedia <span style="margin-left: 5px;">↗</span></a>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.warning(data.get("message", "No matching topics found."))
                        else:
                            st.error(f"Backend API error: {response.text}")
                    except Exception as e:
                        st.error(f"Failed to query fact: {e}")
        else:
            st.markdown("""
            <div style='border: 1px dashed rgba(255,255,255,0.12); border-radius: 16px; padding: 50px 30px; text-align: center; color: #888; background: rgba(255,255,255,0.01);'>
                <div style="font-size: 3rem; margin-bottom: 15px;">🔍</div>
                <h3 style='margin-bottom: 8px; color: #FFFFFF; font-weight: 600;'>Wikipedia Verification Panel</h3>
                <p style="font-size: 0.95rem; max-width: 400px; margin: 0 auto;">Enter a term, technology, or theory to search and fetch summarizing paragraphs.</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------- Tab 3: History & Analytics -----------------
elif menu == "📊 History & Analytics":
    st.markdown("<div class='section-header'>Reviewing Past Strategies</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #B2B2B2; font-size: 1rem; margin-bottom: 30px;'>Examine previously generated networking conversation templates. Update thumbs up/down ratings to refine your networking strategies.</p>", unsafe_allow_html=True)
    
    if not api_online:
        st.error("Cannot retrieve history: Backend server is offline.")
    else:
        with st.spinner("Loading conversation history..."):
            try:
                response = requests.get(f"{API_URL}/api/history")
                if response.status_code == 200:
                    history = response.json().get("history", [])
                    
                    if not history:
                        st.info("No saved history found. Try generating some starters first!")
                    else:
                        # Analytics Summary
                        total_runs = len(history)
                        total_starters = sum(len(item["starters"]) for item in history)
                        
                        # Count thumbs up & down
                        upvotes = sum(1 for item in history if item["feedback"] == 1)
                        downvotes = sum(1 for item in history if item["feedback"] == -1)
                        unrated = sum(1 for item in history if item["feedback"] is None)
                        
                        useful_percentage = int((upvotes / (upvotes + downvotes) * 100)) if (upvotes + downvotes) > 0 else 0
                        
                        # Display custom HTML metrics cards
                        st.markdown(f"""
                        <div class="metric-grid">
                            <div class="metric-card purple">
                                <div class="metric-title">Total Events Logged</div>
                                <div class="metric-value">{total_runs}</div>
                            </div>
                            <div class="metric-card blue">
                                <div class="metric-title">Total Starters Created</div>
                                <div class="metric-value">{total_starters}</div>
                            </div>
                            <div class="metric-card green">
                                <div class="metric-title">Useful Starters (👍)</div>
                                <div class="metric-value green-val">{upvotes}</div>
                            </div>
                            <div class="metric-card yellow">
                                <div class="metric-title">Helper Match Rate</div>
                                <div class="metric-value yellow-val">{useful_percentage}%</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # History list
                        st.markdown("<h3 style='font-size: 1.4rem; font-weight: 700; color: #FFFFFF; margin-bottom: 25px;'>Saved Events & Prompts Log</h3>", unsafe_allow_html=True)
                        
                        for item in history:
                            record_id = item["id"]
                            
                            # Custom layout for each history item
                            with st.container():
                                st.markdown(f"""
                                <div style='border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 22px; margin-bottom: 15px; background: rgba(255,255,255,0.01); box-shadow: 0 4px 15px rgba(0,0,0,0.15);'>
                                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;'>
                                        <span style='font-size: 1.2rem; font-weight: 700; color: #4D96FF;'>Event: {item['event_description']}</span>
                                        <span style='font-size: 0.8rem; color: #888; background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 20px;'>Logged: {item['created_at'][:10]}</span>
                                    </div>
                                    <p style='font-size: 0.95rem; margin-bottom: 12px; color: #E0E0E0;'><strong style='color: #A0A0B0; font-weight: 600;'>Interests:</strong> {item['interests']}</p>
                                    <div style='margin-bottom: 5px;'>
                                        <strong style='color: #A0A0B0; font-weight: 600; margin-right: 12px;'>Themes:</strong> 
                                        {" ".join([f"<span class='theme-tag' style='font-size: 0.75rem; padding: 4px 10px; margin-bottom: 4px;'>{t}</span>" for t in item['extracted_themes']])}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Let's show the starters
                                st.markdown("<p style='font-weight: 600; font-size: 0.95rem; color: #B2B2B2; margin-left: 10px; margin-bottom: 10px;'>Starters generated:</p>", unsafe_allow_html=True)
                                for star_idx, starter in enumerate(item["starters"]):
                                    st.markdown(f"<div class='starter-text' style='margin-left: 20px; margin-bottom: 12px;'>\"{starter}\"</div>", unsafe_allow_html=True)
                                
                                # Dynamic interactive feedback row for this item
                                current_fb = item["feedback"]
                                
                                # Display two buttons side by side for voting
                                fb_col1, fb_col2, fb_col3 = st.columns([1, 1.2, 5])
                                with fb_col1:
                                    up_label = "👍 Useful" if current_fb == 1 else "👍 Rate Useful"
                                    # If clicked and current_fb was 1, we clear it (send 0), otherwise we send 1
                                    target_up = 0 if current_fb == 1 else 1
                                    if st.button(up_label, key=f"up_{record_id}", type="primary" if current_fb == 1 else "secondary"):
                                        if submit_feedback(record_id, target_up):
                                            st.rerun()
                                            
                                with fb_col2:
                                    down_label = "👎 Not Useful" if current_fb == -1 else "👎 Rate Unuseful"
                                    # If clicked and current_fb was -1, we clear it (send 0), otherwise we send -1
                                    target_down = 0 if current_fb == -1 else -1
                                    if st.button(down_label, key=f"down_{record_id}", type="primary" if current_fb == -1 else "secondary"):
                                        if submit_feedback(record_id, target_down):
                                            st.rerun()
                                
                                st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 25px 0 15px 0;' />", unsafe_allow_html=True)
                                
            except Exception as e:
                st.error(f"Error fetching history: {e}")
