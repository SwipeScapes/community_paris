import streamlit as st
from pathlib import Path
from PIL import Image

# --- Page Setup ---
st.set_page_config(page_title="SwipeScapes - Paris", layout="wide")
st.title("🇫🇷 SwipeScapes - Discover Paris Attractions")

# --- Constants ---
PARIS = "Paris"
IMAGES_PATH = Path("images")  # Folder containing your image files

# --- Attraction Data ---
destinations = {
    PARIS: [
        {
            "name": "Eiffel Tower",
            "category": "Sightseeing",
            "rating": 4.7,
            "reviews": 250000,
            "hours": "9 AM – 11 PM",
            "summary": "Iconic Paris landmark with breathtaking city views.",
            "photos": [IMAGES_PATH / "ET.jpg", IMAGES_PATH / "et2.jpg"],
        },
        {
            "name": "Louvre Museum",
            "category": "Museum",
            "rating": 4.8,
            "reviews": 180000,
            "hours": "9 AM – 6 PM (Closed Tue)",
            "summary": "World's largest art museum, home to the Mona Lisa.",
            "photos": [IMAGES_PATH / "LM.jpg", IMAGES_PATH / "LM2.jpg"],
        },
        {
            "name": "Notre Dame",
            "category": "Religious",
            "rating": 4.6,
            "reviews": 150000,
            "hours": "8 AM – 6 PM",
            "summary": "Famous Gothic cathedral with stunning architecture.",
            "photos": [IMAGES_PATH / "ND.jpg", IMAGES_PATH / "ND2.jpg"],
        },
        {
            "name": "Champs-Élysées",
            "category": "Shopping",
            "rating": 4.5,
            "reviews": 100000,
            "hours": "Open 24 hours",
            "summary": "Luxury shopping street with cafés and boutiques.",
            "photos": [IMAGES_PATH / "CE.jpg", IMAGES_PATH / "CE2.jpg"],
        },
    ]
}

# --- Initialize Session State ---
if "liked" not in st.session_state:
    st.session_state.liked = []
if "indices" not in st.session_state:
    st.session_state.indices = {PARIS: 0}
if "photo_index" not in st.session_state:
    st.session_state.photo_index = {PARIS: 0}
if "finalized" not in st.session_state:
    st.session_state.finalized = False

# --- Helper Functions ---
def move_next(city, place_name=None):
    """Go to the next attraction."""
    st.session_state.indices[city] += 1
    st.session_state.photo_index[city] = 0
    if place_name:
        st.session_state.liked.append(place_name)

def change_photo(city, direction, max_index):
    """Switch to previous or next photo."""
    current_index = st.session_state.photo_index[city]
    if direction == "prev":
        st.session_state.photo_index[city] = max(0, current_index - 1)
    elif direction == "next":
        st.session_state.photo_index[city] = min(max_index, current_index + 1)

def finalize_selections():
    """Mark trip selections as finalized."""
    st.session_state.finalized = True

# --- Sidebar Filters ---
st.sidebar.header("Filter Attractions")
filter_choice = st.sidebar.multiselect(
    "Choose filters:",
    ["Museum", "Religious", "Shopping", "Sightseeing"],
    default=[],
)

# --- Main App Logic ---
city = PARIS
st.header(f"📍 {city}")
attractions = destinations[city]

# Apply filters
if filter_choice:
    filtered = [a for a in attractions if a["category"] in filter_choice]
else:
    filtered = attractions

if not filtered:
    st.warning("No attractions match your filter! Try removing some filters.")
else:
    if st.session_state.indices[city] >= len(filtered):
        st.success("🎉 You've swiped through all available attractions in Paris!")
    else:
        place = filtered[st.session_state.indices[city]]
        current_attraction_index = st.session_state.indices[city]
        current_photo_index = st.session_state.photo_index[city]
        max_photo_index = len(place["photos"]) - 1

        # --- Display Attraction Card ---
        with st.container(border=True):
            current_photo_path = place["photos"][current_photo_index]

            if current_photo_path.exists():
                try:
                    img = Image.open(current_photo_path)
                    # Resize image to larger display size
                    max_width = 1200
                    if img.width > max_width:
                        new_height = int((max_width / img.width) * img.height)
                        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                    st.image(
                        img,
                        width=450,
                        caption=f"📸 Photo {current_photo_index + 1} of {max_photo_index + 1}",
                    )
                except Exception as e:
                    st.error(f"⚠️ Error loading image: {e}")
            else:
                st.warning(f"⚠️ Image not found: {current_photo_path.name}")

            # --- Photo navigation buttons ---
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.button(
                    "⬅️ Prev Photo",
                    key=f"prev_{city}_{current_attraction_index}",
                    on_click=change_photo,
                    args=(city, "prev", max_photo_index),
                    disabled=(current_photo_index == 0),
                )
            with col3:
                st.button(
                    "Next Photo ➡️",
                    key=f"next_{city}_{current_attraction_index}",
                    on_click=change_photo,
                    args=(city, "next", max_photo_index),
                    disabled=(current_photo_index == max_photo_index),
                )

            # --- Attraction details ---
            st.subheader(place["name"])
            st.markdown(f"**Category:** *{place['category']}*")
            st.write(f"⭐ **{place['rating']}** ({place['reviews']} reviews)")
            st.write(f"🕐 **Hours:** {place['hours']}")
            st.write(f"📝 {place['summary']}")

            # --- Swipe Buttons ---
            col_skip, col_like = st.columns(2)
            with col_skip:
                st.button(
                    "❌ Skip",
                    key=f"skip_{city}_{current_attraction_index}",
                    use_container_width=True,
                    on_click=move_next,
                    args=(city,),
                )
            with col_like:
                st.button(
                    "❤️ Like",
                    key=f"like_{city}_{current_attraction_index}",
                    use_container_width=True,
                    on_click=move_next,
                    args=(city, place["name"]),
                )

# --- Selections Section ---
st.divider()
st.header("Your Paris Selections")

if st.session_state.liked:
    st.info(f"👍 You've liked **{len(st.session_state.liked)}** attraction(s) so far!")
    st.markdown(f"**Current Likes:** {', '.join(st.session_state.liked)}")
else:
    st.info("Start swiping to build your dream itinerary!")

# --- Finalize Button ---
st.button("✅ Finalize Selections", on_click=finalize_selections)

# --- Final Itinerary Section ---
if st.session_state.finalized:
    st.subheader("Your Final Itinerary:")
    if st.session_state.liked:
        st.balloons()
        st.success("Your liked attractions have been saved!")
        st.markdown(f"**{', '.join(st.session_state.liked)}**")
    else:
        st.warning("No attractions were selected for your itinerary.")
        st.markdown("**Empty Itinerary**")

    st.markdown(
        """
        ---
        **[⬅️ Return to Main Trip Planning Page](https://your-main-website.com)**
        """
    )
