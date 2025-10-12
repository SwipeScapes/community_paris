#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 22:25:47 2025

@author: pavan
"""

import streamlit as st

# --- Page config ---
st.set_page_config(page_title="Flight Booking BLR → BKK", layout="wide")
st.title("✈️ Bangalore → Bangkok Flight Booking")

# --- Traveler Info ---
traveler_type = "Family"
travel_start = "2025-04-03"
travel_end = "2025-04-16"

st.subheader(f"Traveler Type: {traveler_type}")
st.subheader(f"Travel Dates: {travel_start} → {travel_end}")

# --- Flight Data ---
flight_data = [
    {
        "carrier": "Thai Airways",
        "departure": "2025-04-03 05:00",
        "arrival": "2025-04-03 11:15",
        "return_dep": "2025-04-16 12:00",
        "return_arr": "2025-04-16 18:15",
        "duration": "6h 15m",
        "cost": 45000,
        "cancellation": "1%",
        "delays": "Low",
        "audience": "Family Friendly",
        "rating": 80,
        "recommended": True,
        "reason": "Full-service carrier with vegetarian meals, in-flight entertainment, and great legroom."
    },
    {
        "carrier": "Singapore Airlines",
        "departure": "2025-04-03 07:30",
        "arrival": "2025-04-03 13:45",
        "return_dep": "2025-04-16 14:30",
        "return_arr": "2025-04-16 20:45",
        "duration": "6h 15m",
        "cost": 52000,
        "cancellation": "2%",
        "delays": "Medium",
        "audience": "Luxury / Family",
        "rating": 85,
        "recommended": True,
        "reason": "Premium airline with excellent service, popular among families."
    },
    {
        "carrier": "IndiGo",
        "departure": "2025-04-03 06:00",
        "arrival": "2025-04-03 12:15",
        "return_dep": "2025-04-16 13:00",
        "return_arr": "2025-04-16 19:15",
        "duration": "6h 15m",
        "cost": 40000,
        "cancellation": "3%",
        "delays": "Low",
        "audience": "Budget Families",
        "rating": 70,
        "recommended": False,
        "reason": "Budget-friendly option with basic amenities; suitable for families on a budget."
    }
]

# --- Display Flights ---
for flight in flight_data:
    highlight_style = "border: 2px solid green; padding: 15px; margin-bottom: 15px; background-color: #f0fff0;" if flight["recommended"] else "border: 1px solid #ccc; padding: 15px; margin-bottom: 15px; background-color: #f9f9f9;"
    
    st.markdown(f"""
    <div style="{highlight_style} font-family: 'Segoe UI', sans-serif; color: #003366;">
        <h3>{flight['carrier']} {"✅ Recommended" if flight['recommended'] else ""}</h3>
        <p><b>Departure:</b> {flight['departure']} → <b>Arrival:</b> {flight['arrival']}</p>
        <p><b>Return:</b> {flight['return_dep']} → {flight['return_arr']}</p>
        <p><b>Duration:</b> {flight['duration']}</p>
        <p><b>Cost:</b> ₹{flight['cost']}</p>
        <p><b>Cancellation Rate:</b> {flight['cancellation']}</p>
        <p><b>Delay Info:</b> {flight['delays']}</p>
        <p><b>Audience:</b> {flight['audience']} | <b>Rating:</b> {flight['rating']}%</p>
        {"<p><b>Reason for Recommendation:</b> " + flight['reason'] + "</p>" if flight['recommended'] else ""}
    </div>
    """, unsafe_allow_html=True)