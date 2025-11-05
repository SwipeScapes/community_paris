#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 15:16:50 2025

@author: pavan
"""

import streamlit as st
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium

# ----------------------
# Page config
# ----------------------
st.set_page_config(page_title="SwipeScapes - Bangalore to Destinations", layout="wide")

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    h1 {
        color: white;
        text-align: center;
        font-weight: 700;
        font-size: 3.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .subtitle {
        color: #f0f0f0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .map-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 2rem auto;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .map-container * {
        color: #333 !important;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .legend-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem auto;
        max-width: 600px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .legend-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        color: #333;
    }
    
    .legend-color {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-right: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ SwipeScapes")
st.markdown('<p class="subtitle"> Your Perfect Destinations from Bangalore for travel dates along with attractiveness score</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🌍 Explore-Click on each destination to understand each destination offering better</p>', unsafe_allow_html=True)

# ----------------------
# Locations
# ----------------------
locations = [
    {"Destination":"Rome (Italy)","Lat":41.89193,"Lon":12.51133,"Visa":"Yes",
     "Visa_time":"~10-15 working days","Funds":"€130/day/person",
     "Known_for":"Ancient history, Vatican, Roman ruins","Cost":"INR 15000","Safety":70,"Icon":"university","Country":"Italy","Where_to_go":70},
    {"Destination":"Paris (France)","Lat":48.85661,"Lon":2.35222,"Visa":"Yes",
     "Visa_time":"~10-15 working days","Funds":"€130/day/person",
     "Known_for":"Museums, food, fashion, Eiffel Tower","Cost":"INR 20000","Safety":75,"Icon":"flag","Country":"France","Where_to_go":75},
    {"Destination":"Bangkok (Thailand)","Lat":13.75633,"Lon":100.50176,"Visa":"No",
     "Visa_time":"-","Funds":"10000 THB","Known_for":"Street life, temples, markets","Cost":"INR 6000","Safety":65,"Icon":"cutlery","Country":"Thailand","Where_to_go":70},
    {"Destination":"Siem Reap (Cambodia)","Lat":13.3671,"Lon":103.852,"Visa":"E-visa/VoA",
     "Visa_time":"~1-2 business days","Funds":"$100/day","Known_for":"Angkor Wat temples, heritage","Cost":"INR 4500","Safety":62,"Icon":"certificate","Country":"Cambodia","Where_to_go":65},
    {"Destination":"Cairo (Egypt)","Lat":30.0444,"Lon":31.2357,"Visa":"Yes",
     "Visa_time":"~7-10 working days","Funds":"$100/day","Known_for":"Pyramids, Sphinx, Egyptian Museum","Cost":"INR 8000","Safety":20,"Icon":"star","Country":"Egypt","Where_to_go":20}
]

bangalore = {"Lat":12.9716,"Lon":77.5946,"City":"Bangalore (India)"}

# ----------------------
# Function for gradient color based on index
# ----------------------
def get_index_color(index, min_index=20, max_index=75):
    norm = (index - min_index)/(max_index - min_index)
    r = int((1-norm)*255 + norm*76)
    g = int((1-norm)*76 + norm*175)
    b = int((1-norm)*76 + norm*80)
    return f'rgb({r},{g},{b})'

# ----------------------
# Create Map with beautiful tile
# ----------------------
st.markdown('<div class="map-container">', unsafe_allow_html=True)

# Use a more beautiful map tile
m = folium.Map(
    location=[20,50], 
    zoom_start=3, 
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
    attr='Esri'
)

# Bangalore Marker with enhanced styling
folium.Marker(
    location=[bangalore["Lat"], bangalore["Lon"]],
    popup=folium.Popup(f"""
        <div style="font-family: 'Poppins', sans-serif; padding: 10px; text-align: center;">
            <h3 style="color: #667eea; margin: 0;">🏠 {bangalore['City']}</h3>
            <p style="margin: 5px 0; color: #666;">Your Journey Starts Here</p>
        </div>
    """, max_width=200),
    icon=folium.Icon(color="green", icon="home", prefix="fa")
).add_to(m)

# Add destinations
flight_color = "#FF6B6B"  # Beautiful coral red
midpoint_marker_color = "#FFD93D"  # Golden yellow

for loc in locations:
    # Safety color
    safety_color = "#4ECDC4" if loc["Safety"] > 30 else "#FF6B6B"
    
    popup_html = f"""
    <div style="
        width: 300px; 
        padding: 15px; 
        border-radius: 15px; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3); 
        font-family: 'Poppins', sans-serif; 
        color: white;">
        <h3 style="margin:0 0 10px 0; color: white; border-bottom: 2px solid rgba(255,255,255,0.3); padding-bottom: 8px;">
            ✈️ {loc['Destination']}
        </h3>
        <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 8px;">
            <b>🛂 Visa:</b> {loc['Visa']}<br>
            <b>⏱️ Processing:</b> {loc['Visa_time']}<br>
            <b>💰 Funds:</b> {loc['Funds']}<br>
            <b>💵 Cost/day:</b> {loc['Cost']}
        </div>
        <b>🌟 Known for:</b> {loc['Known_for']}<br>
        <div style="margin-top: 10px;">
            <b>🛡️ Safety Index: {loc['Safety']}%</b>
            <div style='width:100%; background-color:rgba(255,255,255,0.3); border-radius:5px; height:12px; margin-top:5px;'>
                <div style='width:{loc['Safety']}%; background-color:{safety_color}; height:12px; border-radius:5px; transition: width 0.3s;'></div>
            </div>
        </div>
    </div>
    """
    
    # Destination marker
    folium.Marker(
        location=[loc['Lat'], loc['Lon']],
        popup=folium.Popup(popup_html, max_width=320),
        icon=folium.Icon(color="darkpurple", icon=loc["Icon"], prefix="fa")
    ).add_to(m)
    
    # Where to Go Index badge with improved styling
    badge_color = get_index_color(loc["Where_to_go"])
    folium.map.Marker(
        [loc['Lat']+0.5, loc['Lon']],
        icon=folium.DivIcon(
            html=f"""
                <div style="
                    background: linear-gradient(135deg, {badge_color}, {get_index_color(loc['Where_to_go']-5)});
                    color:white;
                    font-weight:bold;
                    border-radius:50%;
                    width:35px;
                    height:35px;
                    text-align:center;
                    line-height:35px;
                    border:3px solid white;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                    font-family: 'Poppins', sans-serif;">
                    {loc['Where_to_go']}
                </div>
            """
        )
    ).add_to(m)
    
    # Flight line with animated path
    AntPath(
        locations=[[bangalore["Lat"], bangalore["Lon"]],[loc['Lat'], loc['Lon']]],
        color=flight_color,
        weight=3,
        opacity=0.7,
        dash_array=[10,20],
        delay=800,
        pulse_color='#FFD93D'
    ).add_to(m)
    
    # Midpoint with glow effect
    mid_lat = (bangalore["Lat"] + loc['Lat'])/2
    mid_lon = (bangalore["Lon"] + loc['Lon'])/2
    folium.CircleMarker(
        location=[mid_lat, mid_lon],
        radius=6,
        color=midpoint_marker_color,
        fill=True,
        fill_color=midpoint_marker_color,
        fill_opacity=0.9,
        weight=2
    ).add_to(m)
    
    # Catchment area with gradient effect
    radius_dict = {"Italy":300000, "France":300000, "Thailand":200000, "Cambodia":150000, "Egypt":200000}
    folium.Circle(
        location=[loc['Lat'], loc['Lon']],
        radius=radius_dict[loc['Country']],
        color='#667eea',
        fill=True,
        fill_color='#764ba2',
        fill_opacity=0.15,
        weight=2,
        opacity=0.5
    ).add_to(m)

# ----------------------
# Show map in Streamlit
# ----------------------
st_data = st_folium(m, width=1200, height=650)

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# Legend
# ----------------------
st.markdown("""
    <div class="legend-container">
        <div class="legend-title">🗺️ Map Legend</div>
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(135deg, rgb(76, 175, 80), rgb(139, 195, 74));"></div>
            <span><b>Green Badge (70-75):</b> Highly Recommended</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(135deg, rgb(165, 125, 78), rgb(200, 160, 113));"></div>
            <span><b>Orange Badge (60-69):</b> Good Choice</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(135deg, rgb(255, 76, 76), rgb(255, 107, 107));"></div>
            <span><b>Red Badge (<60):</b> Consider Carefully</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #FF6B6B;"></div>
            <span><b>Red Lines:</b> Flight Routes</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: rgba(118, 75, 162, 0.3); border: 2px solid #667eea;"></div>
            <span><b>Purple Circles:</b> Destination Regions</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------------
# Get Back Button
# ----------------------
st.markdown(
    """
    <div style="text-align:center; margin-top:30px; margin-bottom: 20px;">
        <a href=" https://swipescapes.com/#page-3" target="_blank">
            <button style="
                background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
                color:white;
                padding:15px 40px;
                border:none;
                border-radius:30px;
                font-size:18px;
                font-weight:600;
                cursor:pointer;
                box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
                transition: all 0.3s ease;
                font-family: 'Poppins', sans-serif;">
                ⬅ Back to Home
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
