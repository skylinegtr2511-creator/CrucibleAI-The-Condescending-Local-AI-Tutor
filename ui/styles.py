"""
ui/styles.py
All custom CSS lives here — Claude-inspired warm dark palette, fonts,
and the animations (message fade-in, typing dots, gradient title,
button/slider hover states, custom scrollbar).
"""

import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:ital,opsz,wght@0,9..144,500;1,9..144,500&display=swap');

:root {
    --bg:        #191818;
    --bg-panel:  #1F1E1D;
    --bg-card:   #262624;
    --bg-hover:  #2E2C2A;
    --accent:    #D97757;
    --accent-2:  #E8A87C;
    --accent-soft: rgba(217, 119, 87, 0.15);
    --text:      #F5F4EF;
    --text-muted:#A9A79F;
    --border:    #33312E;
    --success:   #7FB88A;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── App background ─────────────────────────────────────────────── */
.stApp {
    background: radial-gradient(circle at 15% 0%, #1D1B1A 0%, #191818 45%, #151413 100%);
}

/* ── Hide default chrome ────────────────────────────────────────── */
#MainMenu, footer, header {visibility: hidden;}

/* ── Animated gradient hero title ───────────────────────────────── */
.crucible-hero {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.25rem 0 0.75rem 0;
    animation: fadeInDown 0.6s ease-out;
}
.crucible-hero .flame {
    font-size: 2.1rem;
    animation: flicker 2.4s ease-in-out infinite;
    filter: drop-shadow(0 0 10px rgba(217, 119, 87, 0.45));
}
.crucible-hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 2rem;
    margin: 0;
    background: linear-gradient(100deg, #F5F4EF 20%, var(--accent-2) 45%, var(--accent) 65%, #F5F4EF 85%);
    background-size: 300% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shimmer 6s linear infinite;
}
.crucible-hero .tagline {
    color: var(--text-muted);
    font-size: 0.92rem;
    margin-top: -2px;
    letter-spacing: 0.2px;
}

@keyframes shimmer {
    to { background-position: 300% center; }
}
@keyframes flicker {
    0%, 100% { transform: scale(1) rotate(0deg); }
    25%      { transform: scale(1.05) rotate(-3deg); }
    50%      { transform: scale(0.97) rotate(2deg); }
    75%      { transform: scale(1.03) rotate(-1deg); }
}
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Chat messages ───────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 4px 6px;
    margin-bottom: 12px;
    animation: fadeInUp 0.35s ease-out;
    transition: border-color 0.25s ease, transform 0.15s ease;
}
[data-testid="stChatMessage"]:hover {
    border-color: rgba(217, 119, 87, 0.35);
}
[data-testid="stChatMessageAvatarUser"] {
    background: var(--accent) !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, var(--accent), #B85C3E) !important;
}

/* ── Typing indicator ───────────────────────────────────────────── */
.typing-indicator {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 6px 2px;
}
.typing-indicator span {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent);
    animation: bounce 1.2s infinite ease-in-out;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.15s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.30s; }

@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
    30%           { transform: translateY(-6px); opacity: 1; }
}

/* ── Chat input ──────────────────────────────────────────────────── */
[data-testid="stChatInput"] {
    border-radius: 14px;
    border: 1px solid var(--border);
    background: var(--bg-panel);
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-soft);
}

/* ── Sidebar ─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-panel);
    border-right: 1px solid var(--border);
}
.sidebar-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 14px;
    animation: fadeInUp 0.4s ease-out;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.sidebar-card:hover {
    border-color: rgba(217, 119, 87, 0.3);
    transform: translateY(-1px);
}
.sidebar-card h4 {
    margin: 0 0 8px 0;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--text-muted);
    font-weight: 600;
}
.sarcasm-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent-2);
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    animation: fadeInUp 0.3s ease-out;
}

/* ── Buttons ─────────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    background: var(--bg-card) !important;
    color: var(--text) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    background: var(--accent-soft) !important;
    color: var(--accent-2) !important;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0px) scale(0.98);
}

/* Primary "New Chat" style button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), #C1613F) !important;
    border: none !important;
    color: #FFF !important;
}

/* ── Slider ──────────────────────────────────────────────────────── */
[data-testid="stSlider"] [role="slider"] {
    background-color: var(--accent) !important;
    box-shadow: 0 0 0 6px var(--accent-soft) !important;
}
[data-testid="stSlider"] .st-emotion-cache-1dx1gwv,
[data-testid="stTickBar"] {
    background: var(--accent) !important;
}

/* ── File uploader ───────────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {
    background: var(--bg-card) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
    transition: border-color 0.25s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--accent) !important;
}

/* ── Session list rows ───────────────────────────────────────────── */
.session-row {
    padding: 8px 10px;
    border-radius: 10px;
    font-size: 0.85rem;
    color: var(--text-muted);
    border: 1px solid transparent;
    transition: all 0.2s ease;
    cursor: pointer;
}
.session-row:hover {
    background: var(--bg-hover);
    border-color: var(--border);
    color: var(--text);
}

/* ── Scrollbar ───────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 8px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ── Divider ─────────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── Success / toast tweaks ─────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px;
    animation: fadeInUp 0.3s ease-out;
}
</style>
"""


def inject_custom_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown(
        """
        <div class="crucible-hero">
            <div class="flame">🔥</div>
            <div>
                <h1>CrucibleAI</h1>
                <div class="tagline">The Condescending Tutor — forging knowledge, one roast at a time.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def typing_indicator_html() -> str:
    return (
        '<div class="typing-indicator"><span></span><span></span><span></span></div>'
    )
