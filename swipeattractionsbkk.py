import streamlit as st
import time
from pathlib import Path

st.set_page_config(page_title="SwipeScapes - Bangkok", layout="wide")
st.title("🇹🇭 SwipeScapes - Discover Bangkok Attractions")

BANGKOK = "Bangkok"

# --- Path to local images folder ---
# Update this path to match your local folder structure
IMAGES_PATH = Path("images")  # e.g., "images/bangkok" or "/Users/yourname/Desktop/bangkok_images"

# --- Attraction Data with local image paths ---
destinations = {
    BANGKOK: [
        {
            "name": "Grand Palace",
            "category": "Sightseeing",
            "rating": 4.6,
            "reviews": 180000,
            "hours": "8:30 AM – 3:30 PM",
            "summary": "Stunning royal complex with intricate Thai architecture.",
            "photos": [
                IMAGES_PATH / "GP.jpg",
                IMAGES_PATH / "GP2.jpg"
            ]
        },
        {
            "name": "Wat Arun",
            "category": "Temple",
            "rating": 4.7,
            "reviews": 150000,
            "hours": "8 AM – 6 PM",
            "summary": "Temple of Dawn with iconic riverside spires.",
            "photos": [
                IMAGES_PATH / "WA.jpg",
                IMAGES_PATH / "WA2.jpg"
            ]
        },
        {
            "name": "Chatuchak Weekend Market",
            "category": "Shopping",
            "rating": 4.5,
            "reviews": 120000,
            "hours": "9 AM – 6 PM (Sat-Sun)",
            "summary": "Massive market with thousands of stalls selling everything.",
            "photos": [
                IMAGES_PATH / "CM.jpg",
                IMAGES_PATH / "CM2.jpg"
            ]
        },
        {
            "name": "Wat Pho",
            "category": "Temple",
            "rating": 4.8,
            "reviews": 140000,
            "hours": "8 AM – 6:30 PM",
            "summary": "Home to the famous reclining Buddha statue.",
            "photos": [
                IMAGES_PATH / "WP.jpg",
                IMAGES_PATH / "WP2.jpg"
            ]
        },
    ]
}

# --- Initialize session state ---
if "liked" not in st.session_state:
    st.session_state.liked = []
if "indices" not in st.session_state:
    st.session_state.indices = {BANGKOK: 0}
if "photo_index" not in st.session_state:
    st.session_state.photo_index = {BANGKOK: 0}
if "finalized" not in st.session_state:
    st.session_state.finalized = False


# --- Callbacks for state updates ---
def move_next(city, place_name=None):
    """Increments the attraction index and resets the photo index."""
    st.session_state.indices[city] += 1
    st.session_state.photo_index[city] = 0 
    if place_name:
        st.session_state.liked.append(place_name)

def change_photo(city, direction, max_index):
    """Changes the current photo index for the displayed attraction."""
    current_index = st.session_state.photo_index[city]
    if direction == "prev":
        st.session_state.photo_index[city] = max(0, current_index - 1)
    elif direction == "next":
        st.session_state.photo_index[city] = min(max_index, current_index + 1)
        
def finalize_selections():
    """Sets the finalized state to True."""
    st.session_state.finalized = True

# --- Filters ---
st.sidebar.header("Filter Attractions")
filter_choice = st.sidebar.multiselect(
    "Choose filters:", 
    ["Museum", "Temple", "Shopping", "Nightlife", "Sightseeing"],
    default=[]
)

# --- Main App Logic ---
city = BANGKOK
st.header(f"📍 {city}")
attractions = destinations[city]

# Apply filter
if filter_choice:
     filtered = [a for a in attractions if a["category"] in filter_choice]
else:
    filtered = attractions

if not filtered:
    st.warning("No attractions match your filter! Try removing some filters.")
else:
    # Check if all attractions viewed
    if st.session_state.indices[city] >= len(filtered):
        st.success("🎉 You've swiped through all available attractions in Bangkok!")
    else:
        place = filtered[st.session_state.indices[city]]
        current_attraction_index = st.session_state.indices[city]
        current_photo_index = st.session_state.photo_index[city]
        max_photo_index = len(place["photos"]) - 1

        # Display attraction card and photo
        with st.container(border=True):
            
            # Image with cache buster
            image_placeholder = st.empty()
            current_photo_path = place["photos"][current_photo_index]
            
            # Check if image file exists
            if current_photo_path.exists():
                with image_placeholder:
                    st.image(
                        str(current_photo_path),
                        use_container_width=True,
                        caption=f"Photo {current_photo_index + 1} of {max_photo_index + 1}"
                    )
            else:
                st.error(f"⚠️ Image not found: {current_photo_path.name}")
                st.info("Please ensure images are in the correct folder with matching filenames.")
            
            # Photo navigation buttons
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                st.button("⬅️ Prev Photo", 
                          key=f"prev_{city}_{current_attraction_index}",
                          on_click=change_photo, 
                          args=(city, "prev", max_photo_index),
                          disabled=(current_photo_index == 0))
            with col3:
                st.button("Next Photo ➡️", 
                          key=f"next_{city}_{current_attraction_index}",
                          on_click=change_photo, 
                          args=(city, "next", max_photo_index),
                          disabled=(current_photo_index == max_photo_index))
            
            st.subheader(place["name"])
            st.markdown(f"**Category:** *{place['category']}*")
            st.write(f"⭐ **{place['rating']}** ({place['reviews']} reviews)")
            st.write(f"🕐 **Hours:** {place['hours']}")
            st.write(f"📝 {place['summary']}")

            # Tinder-style Like / Skip buttons
            col_skip, col_like = st.columns(2)
            with col_skip:
                st.button("❌ Skip", 
                          key=f"skip_{city}_{current_attraction_index}",
                          use_container_width=True,
                          on_click=move_next, 
                          args=(city,))
            with col_like:
                st.button("❤️ Like", 
                          key=f"like_{city}_{current_attraction_index}",
                          use_container_width=True,
                          on_click=move_next, 
                          args=(city, place["name"]))

st.divider()

## Your Trip Selections
st.header("Your Bangkok Selections")

if st.session_state.liked:
    st.info(f"👍 You've liked **{len(st.session_state.liked)}** attraction(s) so far!")
    st.markdown(f"**Current Likes:** {', '.join(st.session_state.liked)}")
else:
    st.info("Start swiping to build your dream itinerary!")

# Finalize Selections button
st.button("✅ Finalize Selections", on_click=finalize_selections)

# --- Finalization Message and Return Link ---
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
        ***
        **[⬅️ Click here to return to your main trip planning page](https://your-main-website.com)**
        """
    )
