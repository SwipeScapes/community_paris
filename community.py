import streamlit as st
from datetime import datetime
import random

# --- Page config ---
st.set_page_config(page_title="Travel Community", layout="wide")

# --- Dummy profile images (emojis for demo) ---
profile_pics = {
    "Alice": "👩‍🦱",
    "Bob": "👨‍🦰",
    "Clara": "👩‍🦳",
    "David": "👨",
    "Eva": "👩",
    "Frank": "🧔",
}

# --- Fake timestamps ---
def random_timestamp():
    hours_ago = random.choice([2, 5, 12, 24, 48])
    return f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"

# --- Initialize posts and banner state ---
if "paris_posts" not in st.session_state:
    st.session_state.paris_posts = [
        {"user": "Alice", "content": "Loved the hidden café near Montmartre! Their croissants are amazing. ☕🥐",
         "type": "gem", "likes": 12, "useful": 8, "not_useful": 1,
         "comments": ["So true! Must visit."], "time": random_timestamp()},
        {"user": "Bob", "content": "Beware of pickpockets near the Eiffel Tower and Trocadéro 😬. Keep your bag close!",
         "type": "scam", "likes": 34, "useful": 25, "not_useful": 3,
         "comments": ["Thanks for the warning!"], "time": random_timestamp()},
        {"user": "Clara", "content": "The Seine boat tour at sunset is magical ✨. Book tickets online to avoid long queues.",
         "type": "experience", "likes": 20, "useful": 15, "not_useful": 2,
         "comments": ["Absolutely loved it!"], "time": random_timestamp()},
    ]

if "bkk_posts" not in st.session_state:
    st.session_state.bkk_posts = [
        {"user": "David", "content": "Chatuchak Market is huge! Go early to avoid crowds and heat 🛍️🌞",
         "type": "experience", "likes": 18, "useful": 12, "not_useful": 1,
         "comments": ["Great tip!"], "time": random_timestamp()},
        {"user": "Eva", "content": "Tuk-tuks near Asoke and Sukhumvit are expensive 💸. Grab or metered taxis are better.",
         "type": "scam", "likes": 40, "useful": 30, "not_useful": 2,
         "comments": ["Good to know, thanks!"], "time": random_timestamp()},
        {"user": "Frank", "content": "Hidden rooftop bar in Sukhumvit is amazing 🍹. Great view at sunset!",
         "type": "gem", "likes": 25, "useful": 20, "not_useful": 1,
         "comments": ["Adding this to my list!"], "time": random_timestamp()},
    ]

# Initialize state for the banner visibility - track per destination
if "banner_closed_paris" not in st.session_state:
    st.session_state.banner_closed_paris = False
if "banner_closed_bangkok" not in st.session_state:
    st.session_state.banner_closed_bangkok = False

# --- Sidebar with countdown ---
st.sidebar.title("🧳 Travel Countdown")
days_left = 13
destination = st.sidebar.radio("Select your destination", ["Paris", "Bangkok"])

# --- POP-UP AD BANNER FUNCTION ---
def travel_reminder(destination, days_left):
    # Check if banner was closed for this destination
    banner_closed = st.session_state.banner_closed_paris if destination == "Paris" else st.session_state.banner_closed_bangkok
    
    if not banner_closed:
        if destination == "Paris":
            temp_range = "10°C to 18°C"
            packing = "light jacket, sweater, comfortable shoes, umbrella, and sunglasses"
        else:  # Bangkok
            temp_range = "28°C to 35°C"
            packing = "light cotton clothes, sandals, sunhat, sunscreen, and umbrella for showers"
        
        st.markdown(f"""
        <style>
        .popup-banner {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 550px;
            max-width: 90%;
            z-index: 9999;
            border-radius: 12px;
            background: linear-gradient(90deg, #FFDEE9 0%, #B5FFFC 100%);
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            padding: 30px;
            padding-right: 30px;
            font-family: 'Segoe UI', sans-serif;
            color: black;
            animation: fadeIn 0.5s ease-in, fadeOut 0.5s ease-out 4.5s forwards;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translate(-50%, -50%) scale(0.9); }}
            to {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
        }}
        @keyframes fadeOut {{
            from {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
            to {{ opacity: 0; transform: translate(-50%, -50%) scale(0.9); }}
        }}
        .banner-content h3 {{
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 20px;
        }}
        .banner-content p {{
            margin: 10px 0;
            font-size: 16px;
        }}
        </style>
        
        <div class="popup-banner" id="travelBanner">
            <div class="banner-content">
                <h3>⏰ {days_left} days left for your trip to {destination}!</h3>
                <p>🌤️ Expected Temperatures: <b>{temp_range}</b></p>
                <p>🧳 Suggested Packing: {packing}</p>
            </div>
        </div>
        
        <script>
        setTimeout(function() {{
            var banner = document.getElementById('travelBanner');
            if (banner) {{
                banner.style.display = 'none';
            }}
        }}, 5000);
        </script>
        """, unsafe_allow_html=True)
        
        # Auto-close banner after showing it once
        import time
        time.sleep(5)
        if destination == "Paris":
            st.session_state.banner_closed_paris = True
        else:
            st.session_state.banner_closed_bangkok = True
        st.rerun()

# Call the reminder function
travel_reminder(destination, days_left)

# --- Post card function ---
def display_posts(posts, destination):
    for idx, post in enumerate(posts):
        bg = "#fefefe" if post["type"]=="gem" else "#fff0f0" if post["type"]=="scam" else "#f0f8ff" 
        text_color = "#003366" if post["type"] != "scam" else "#004d00"

        st.markdown(
            f"""
            <div style="
                border:1px solid #e0e0e0;
                border-radius:15px;
                padding:15px;
                margin-bottom:20px;
                background-color:{bg};
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            ">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:30px;">{profile_pics.get(post['user'], '👤')}</span>
                    <div>
                        <b style="color: {text_color};">{post['user']}</b><br>
                        <span style="font-size:12px; color:#999999;">{post['time']}</span>
                    </div>
                </div>
                <p style="
                    margin-top:10px;
                    font-size:16px; 
                    line-height:1.5; 
                    color:{text_color}; 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                ">{post['content']}</p>
            </div>
            """, unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns([1,1,1,5])
        post_key_prefix = 'paris_posts' if destination=='Paris' else 'bkk_posts'

        def update_post_count(count_key, index):
            st.session_state.get(post_key_prefix)[index][count_key] += 1
            st.rerun()

        with col1:
            st.button(f"❤️ {post['likes']}", key=f"like_{idx}_{destination}",
                      on_click=update_post_count, args=("likes", idx))
        with col2:
            st.button(f"👍 {post['useful']}", key=f"useful_{idx}_{destination}",
                      on_click=update_post_count, args=("useful", idx))
        with col3:
            st.button(f"👎 {post['not_useful']}", key=f"notuseful_{idx}_{destination}",
                      on_click=update_post_count, args=("not_useful", idx))
        with col4:
            st.write(f"💬 {len(post['comments'])} comments")

        new_comment = st.text_input("Add a comment:", key=f"comment_{idx}_{destination}")
        if new_comment:
            posts[idx]["comments"].append(new_comment)
            st.session_state[f"comment_{idx}_{destination}"] = ""
            st.rerun()

        if post["comments"]:
            for c in post["comments"]:
                st.markdown(f"<div style='margin-left:25px; color:#555;'>💬 {c}</div>", unsafe_allow_html=True)

        st.markdown("---")

# --- Tabs ---
tab1, tab2 = st.tabs(["Paris 🇫🇷", "Bangkok 🇹🇭"])
with tab1:
    st.header("Paris Community Feed")
    display_posts(st.session_state.paris_posts, "Paris")
with tab2:
    st.header("Bangkok Community Feed")
    display_posts(st.session_state.bkk_posts, "Bangkok")

# --- Footer ---
st.markdown("---")
st.caption("✨ Travel safe, explore more, and share your stories with the community!")