import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import io

# Set page config for better performance
st.set_page_config(
    page_title="SwipeScapes - Bangkok Itinerary",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .day-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px; margin: 10px 0; }
    .attraction-card { background-color: white; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .meal-warning { background-color: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 8px; color: #856404; }
    .restaurant-option { background-color: #e7f3ff; padding: 12px; border-radius: 6px; margin: 8px 0; border-left: 4px solid #0066cc; }
    [data-testid="stDataFrame"] { font-size: 24px !important; }
    [data-testid="stDataFrame"] td { font-size: 24px !important; }
    [data-testid="stDataFrame"] th { font-size: 24px !important; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'lunch_added_day3' not in st.session_state:
    st.session_state.lunch_added_day3 = None
if 'selected_restaurant' not in st.session_state:
    st.session_state.selected_restaurant = None

# Bangkok attractions data
ATTRACTIONS = {
    "Grand Palace": {"lat": 13.6515, "lon": 100.4904, "duration": 90, "category": "Iconic"},
    "Wat Arun": {"lat": 13.6435, "lon": 100.4864, "duration": 75, "category": "Temple"},
    "Wat Pho": {"lat": 13.6469, "lon": 100.4909, "duration": 90, "category": "Temple"},
    "Chatuchak Weekend Market": {"lat": 13.8116, "lon": 100.5527, "duration": 120, "category": "Shopping"},
    "Jim Thompson House": {"lat": 13.7367, "lon": 100.5108, "duration": 60, "category": "Historic"},
    "Lumphini Park": {"lat": 13.7307, "lon": 100.5542, "duration": 75, "category": "Nature"},
    "Chao Phraya River Cruise": {"lat": 13.7280, "lon": 100.5008, "duration": 90, "category": "Experience"}
}

RESTAURANTS = {
    "Gaggan": {"lat": 13.7163, "lon": 100.5542, "cuisine": "Thai", "price": "€€€", "stars": 3},
    "Pad Thai Restaurant": {"lat": 13.7280, "lon": 100.5008, "cuisine": "Thai", "price": "€", "stars": 4},
    "Issaya Siamese Club": {"lat": 13.7437, "lon": 100.5234, "cuisine": "Thai", "price": "€€€", "stars": 5},
    "Khao San Road Eatery": {"lat": 13.7618, "lon": 100.5003, "cuisine": "Thai Street", "price": "€", "stars": 4},
    "Som Tam Nua": {"lat": 13.7307, "lon": 100.5542, "cuisine": "Thai", "price": "€", "stars": 4},
    "Blue Elephant": {"lat": 13.6878, "lon": 100.5234, "cuisine": "Thai", "price": "€€€", "stars": 5}
}

ITINERARY = {
    "Day 1": {
        "date": "May 10, 2025",
        "theme": "🏯 Royal Bangkok",
        "color": "#FF6B6B",
        "stops": [
            {"name": "Grand Palace", "time": "08:30", "type": "attraction"},
            {"name": "Wat Arun", "time": "11:00", "type": "attraction"},
            {"name": "Pad Thai Restaurant", "time": "13:00", "type": "restaurant"},
            {"name": "Chao Phraya River Cruise", "time": "15:00", "type": "attraction"}
        ]
    },
    "Day 2": {
        "date": "May 11, 2025",
        "theme": "🏮 Temples & Culture",
        "color": "#4ECDC4",
        "stops": [
            {"name": "Wat Pho", "time": "09:00", "type": "attraction"},
            {"name": "Jim Thompson House", "time": "11:00", "type": "attraction"},
            {"name": "Issaya Siamese Club", "time": "13:00", "type": "restaurant"},
            {"name": "Lumphini Park", "time": "15:30", "type": "attraction"}
        ]
    },
    "Day 3": {
        "date": "May 12, 2025",
        "theme": "🛍️ Markets & Shopping",
        "color": "#FFE66D",
        "stops": [
            {"name": "Chatuchak Weekend Market", "time": "09:00", "type": "attraction"},
            {"name": "Khao San Road Eatery", "time": "12:30", "type": "restaurant"}
        ]
    }
}

def calculate_end_time(start_time, duration_minutes):
    """Calculate end time."""
    start = datetime.strptime(start_time, "%H:%M")
    end = start + timedelta(minutes=duration_minutes)
    return end.strftime("%H:%M")

def get_duration(item_name):
    """Get duration for attraction or restaurant."""
    if item_name in ATTRACTIONS:
        return ATTRACTIONS[item_name]["duration"]
    elif item_name in RESTAURANTS:
        return 60  # Default meal time
    return 60

def display_day_itinerary(day_name, day_data):
    """Display itinerary for a single day."""
    with st.container():
        st.markdown(f"<div class='day-header'><h2>{day_data['theme']}</h2><p>{day_data['date']}</p></div>", unsafe_allow_html=True)
        
        # Create dataframe
        data = []
        for stop in day_data['stops']:
            name = stop['name']
            start_time = stop['time']
            duration = get_duration(name)
            end_time = calculate_end_time(start_time, duration)
            
            if stop['type'] == 'restaurant':
                category = "🍽️ Restaurant"
            else:
                category = f"📍 {ATTRACTIONS[name]['category']}"
            
            data.append({
                "⏰ Time": f"{start_time} - {end_time}",
                "📍 Location": name,
                "⏳ Duration": f"{duration} min",
                "🏷️ Type": category
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        return df

def create_map_with_routes():
    """Create interactive map with all routes."""
    center_lat, center_lon = 13.7563, 100.5018
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )
    
    # Day 1 route
    day1_coords = [
        (13.6515, 100.4904),  # Grand Palace
        (13.6435, 100.4864),  # Wat Arun
        (13.7280, 100.5008),  # Pad Thai Restaurant
        (13.7280, 100.5008)   # Chao Phraya River Cruise
    ]
    
    # Day 2 route
    day2_coords = [
        (13.6469, 100.4909),  # Wat Pho
        (13.7367, 100.5108),  # Jim Thompson House
        (13.7437, 100.5234),  # Issaya Siamese Club
        (13.7307, 100.5542)   # Lumphini Park
    ]
    
    # Day 3 route
    day3_coords = [
        (13.8116, 100.5527),  # Chatuchak Weekend Market
        (13.7618, 100.5003)   # Khao San Road Eatery
    ]
    
    # Draw routes
    folium.PolyLine(day1_coords, color="#FF6B6B", weight=4, opacity=0.8, popup="Day 1").add_to(m)
    folium.PolyLine(day2_coords, color="#4ECDC4", weight=4, opacity=0.8, popup="Day 2").add_to(m)
    folium.PolyLine(day3_coords, color="#FFE66D", weight=4, opacity=0.8, popup="Day 3").add_to(m)
    
    # Add markers
    for idx, (lat, lon) in enumerate(day1_coords, 1):
        folium.CircleMarker([lat, lon], radius=8, color="#FF6B6B", fill=True, fillColor="#FF6B6B", fillOpacity=0.8, popup=f"Day 1 - Stop {idx}").add_to(m)
    
    for idx, (lat, lon) in enumerate(day2_coords, 1):
        folium.CircleMarker([lat, lon], radius=8, color="#4ECDC4", fill=True, fillColor="#4ECDC4", fillOpacity=0.8, popup=f"Day 2 - Stop {idx}").add_to(m)
    
    for idx, (lat, lon) in enumerate(day3_coords, 1):
        folium.CircleMarker([lat, lon], radius=8, color="#FFE66D", fill=True, fillColor="#FFE66D", fillOpacity=0.8, popup=f"Day 3 - Stop {idx}").add_to(m)
    
    return m

def export_to_excel(all_data):
    """Export itineraries to Excel."""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for day_name, df in all_data.items():
            df.to_excel(writer, sheet_name=day_name, index=False)
    
    output.seek(0)
    return output.getvalue()

# Main app
st.title("✈️ SwipeScapes - Bangkok 3-Day Itinerary")
st.markdown("---")

# Back button
col_back = st.columns([5, 1])
with col_back[1]:
    if st.button("← Back to Website", use_container_width=True):
        st.info("Redirecting to SwipeScapes website...")
        st.markdown("<meta http-equiv='refresh' content='1;url=https://swipescapes.com'>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["📋 Itinerary", "🗺️ Map", "💾 Export"])

with tab1:
    st.header("Your Personalized Bangkok Trip")
    
    all_dataframes = {}
    
    # Display all days
    for day_name, day_data in ITINERARY.items():
        df = display_day_itinerary(day_name, day_data)
        all_dataframes[day_name] = df
    
    # Day 3 lunch alert
    st.markdown("---")
    st.markdown("<div class='meal-warning'><h3>⚠️ Missing Dinner on Day 3</h3><p>Your Day 3 itinerary is missing dinner. Would you like to add a restaurant?</p></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h4>Recommended Restaurants:</h4>", unsafe_allow_html=True)
        
        restaurant_options = []
        for rest_name, details in RESTAURANTS.items():
            rest_col1, rest_col2, rest_col3, rest_col4 = st.columns([2, 1, 1, 1])
            with rest_col1:
                if st.checkbox(rest_name, key=f"rest_{rest_name}"):
                    st.session_state.selected_restaurant = rest_name
                    st.session_state.lunch_added_day3 = True
            with rest_col2:
                st.write(f"🍽️ {details['cuisine']}")
            with rest_col3:
                st.write(f"💰 {details['price']}")
            with rest_col4:
                st.write(f"⭐ {details['stars']}")
    
    if st.session_state.lunch_added_day3 and st.session_state.selected_restaurant:
        st.success(f"✅ Added {st.session_state.selected_restaurant} to Day 3 dinner at 18:00!")

with tab2:
    st.header("Bangkok Itinerary Routes")
    st.markdown("**Route Colors:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='background-color: #FF6B6B; padding: 10px; border-radius: 5px; color: white; text-align: center;'><b>Day 1: Royal Bangkok</b></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='background-color: #4ECDC4; padding: 10px; border-radius: 5px; color: white; text-align: center;'><b>Day 2: Temples & Culture</b></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='background-color: #FFE66D; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>Day 3: Markets & Shopping</b></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    m = create_map_with_routes()
    st_folium(m, width=1400, height=600)

with tab3:
    st.header("Export Your Itinerary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download as Excel", use_container_width=True):
            excel_data = export_to_excel(all_dataframes)
            st.download_button(
                label="Download Excel File",
                data=excel_data,
                file_name="Bangkok_3Day_Itinerary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    with col2:
        if st.button("📊 View Summary", use_container_width=True):
            st.write("### Trip Summary")
            
            total_attractions = sum(len([s for s in day["stops"] if s["type"] == "attraction"]) for day in ITINERARY.values())
            total_meals = sum(len([s for s in day["stops"] if s["type"] == "restaurant"]) for day in ITINERARY.values())
            if st.session_state.lunch_added_day3:
                total_meals += 1
            
            total_duration = sum(get_duration(s["name"]) for day in ITINERARY.values() for s in day["stops"])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📍 Total Days", "3")
            col2.metric("🏛️ Attractions", total_attractions)
            col3.metric("🍽️ Meals", total_meals)
            col4.metric("⏱️ Total Hours", f"{total_duration // 60}h {total_duration % 60}m")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 20px;'>
    <p>Made with ❤️ by SwipeScapes</p>
    <p style='font-size: 12px;'>Your personalized travel companion powered by AI & Geospatial Tech</p>
</div>
""", unsafe_allow_html=True)
