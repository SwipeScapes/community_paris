import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import io

# Set page config for better performance
st.set_page_config(
    page_title="SwipeScapes - Paris Itinerary",
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

# Paris attractions data
ATTRACTIONS = {
    "Eiffel Tower": {"lat": 48.8584, "lon": 2.2945, "duration": 90, "category": "Iconic"},
    "Louvre Museum": {"lat": 48.8606, "lon": 2.3352, "duration": 180, "category": "Museum"},
    "Arc de Triomphe": {"lat": 48.8738, "lon": 2.2950, "duration": 60, "category": "Iconic"},
    "Notre-Dame Cathedral": {"lat": 48.8530, "lon": 2.3499, "duration": 75, "category": "Historic"},
    "Sacré-Cœur Basilica": {"lat": 48.8867, "lon": 2.3431, "duration": 60, "category": "Historic"},
    "Champs-Élysées": {"lat": 48.8698, "lon": 2.3076, "duration": 120, "category": "Shopping"},
    "Versailles Palace": {"lat": 48.8047, "lon": 2.1204, "duration": 240, "category": "Historic"}
}

RESTAURANTS = {
    "L'Astrance": {"lat": 48.8550, "lon": 2.2950, "cuisine": "French", "price": "€€€", "stars": 3},
    "Café de Flore": {"lat": 48.8540, "lon": 2.3300, "cuisine": "French", "price": "€€", "stars": 4},
    "Joe's Pizza": {"lat": 48.8600, "lon": 2.3400, "cuisine": "Italian", "price": "€", "stars": 4},
    "Le Jules Verne": {"lat": 48.8584, "lon": 2.2945, "cuisine": "French", "price": "€€€", "stars": 5},
    "Marais Falafel": {"lat": 48.8620, "lon": 2.3650, "cuisine": "Middle Eastern", "price": "€", "stars": 4},
    "Le Comptoir du Relais": {"lat": 48.8510, "lon": 2.3360, "cuisine": "French", "price": "€€", "stars": 5}
}

ITINERARY = {
    "Day 1": {
        "date": "April 4, 2025",
        "theme": "🗼 Iconic Paris",
        "color": "#FF6B6B",
        "stops": [
            {"name": "Eiffel Tower", "time": "09:00", "type": "attraction"},
            {"name": "Champs-Élysées", "time": "11:00", "type": "attraction"},
            {"name": "Café de Flore", "time": "13:30", "type": "restaurant"},
            {"name": "Arc de Triomphe", "time": "15:00", "type": "attraction"}
        ]
    },
    "Day 2": {
        "date": "April 5, 2025",
        "theme": "🖼️ Museums & Culture",
        "color": "#4ECDC4",
        "stops": [
            {"name": "Louvre Museum", "time": "09:00", "type": "attraction"},
            {"name": "Le Comptoir du Relais", "time": "13:00", "type": "restaurant"},
            {"name": "Notre-Dame Cathedral", "time": "14:30", "type": "attraction"}
        ]
    },
    "Day 3": {
        "date": "April 6, 2025",
        "theme": "⛪ Historic & Spiritual",
        "color": "#FFE66D",
        "stops": [
            {"name": "Sacré-Cœur Basilica", "time": "09:30", "type": "attraction"},
            {"name": "Versailles Palace", "time": "14:00", "type": "attraction"}
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
    center_lat, center_lon = 48.8566, 2.3522
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )
    
    # Day 1 route
    day1_coords = [
        (48.8584, 2.2945),  # Eiffel Tower
        (48.8698, 2.3076),  # Champs-Élysées
        (48.8540, 2.3300),  # Café de Flore
        (48.8738, 2.2950)   # Arc de Triomphe
    ]
    
    # Day 2 route
    day2_coords = [
        (48.8606, 2.3352),  # Louvre
        (48.8510, 2.3360),  # Le Comptoir du Relais
        (48.8530, 2.3499)   # Notre-Dame
    ]
    
    # Day 3 route
    day3_coords = [
        (48.8867, 2.3431),  # Sacré-Cœur
        (48.8047, 2.1204)   # Versailles
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
st.title("✈️ SwipeScapes - Paris 3-Day Itinerary")
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
    st.header("Your Personalized Paris Trip")
    
    all_dataframes = {}
    
    # Display all days
    for day_name, day_data in ITINERARY.items():
        df = display_day_itinerary(day_name, day_data)
        all_dataframes[day_name] = df
    
    # Day 3 lunch alert
    st.markdown("---")
    st.markdown("<div class='meal-warning'><h3>⚠️ Missing Lunch on Day 3</h3><p>Your Day 3 itinerary is missing lunch. Would you like to add a restaurant?</p></div>", unsafe_allow_html=True)
    
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
        st.success(f"✅ Added {st.session_state.selected_restaurant} to Day 3 lunch at 13:00!")

with tab2:
    st.header("Paris Itinerary Routes")
    st.markdown("**Route Colors:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='background-color: #FF6B6B; padding: 10px; border-radius: 5px; color: white; text-align: center;'><b>Day 1: Iconic Paris</b></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='background-color: #4ECDC4; padding: 10px; border-radius: 5px; color: white; text-align: center;'><b>Day 2: Museums</b></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='background-color: #FFE66D; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>Day 3: Historic</b></div>", unsafe_allow_html=True)
    
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
                file_name="Paris_3Day_Itinerary.xlsx",
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