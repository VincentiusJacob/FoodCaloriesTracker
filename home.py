import streamlit as st

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        margin-top:2rem;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        text-shadow: 0 4px 12px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.95);
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        height: 100%;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(102, 126, 234, 0.2);
    }
    
    .card:hover::before {
        transform: scaleX(1);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        transition: transform 0.4s ease;
    }
    
    .card:hover .card-icon {
        transform: scale(1.1) rotate(5deg);
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: #2d3748;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-clip: text;
    }
    
    .card-desc {
        font-size: 1rem;
        color: #4a5568;
        line-height: 1.6;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
        padding: 1rem 3rem;
        border-radius: 50px;
        border: none;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 2rem auto;
        display: block;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-container">
        <h1 class="hero-title">🍽️ Food-Calorie Tracker</h1>
        <p class="hero-subtitle">Detect food, count calories, and track your daily intake with AI-powered precision</p>
    </div>
    """,
    unsafe_allow_html=True,
)

cols = st.columns(4)
features = [
    ("📸", "Upload Detection", "Drop an image and get instant calorie estimation powered by AI."),
    ("📹", "Real-Time Camera", "Point your webcam and see live food detection in action."),
    ("📊", "Weekly Reports", "Review your daily and weekly calorie history with beautiful charts."),
    ("📄", "Export PDF", "Download a clean, professional report for sharing or archiving."),
]

for col, (icon, ttl, desc) in zip(cols, features):
    with col:
        st.markdown(
            f'''
            <div class="card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{ttl}</div>
                <div class="card-desc">{desc}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Get Started Now", type="primary"):
        st.switch_page("track_calories.py")