import streamlit as st

# --- Page config ---
st.set_page_config(page_title="Flight Booking - BLR to Paris", layout="wide")

# --- Title ---
st.title("✈️ Flights: Bangalore → Paris")
st.markdown("Travel Dates: **April 3 → April 16**")
st.markdown("Traveler Type: **Family**")

# --- Sample Flight Data (Multiple Carriers) ---
flight_itineraries = [
    {
        "carrier": "Air India",
        "departure": "2025-04-03 03:30",
        "arrival": "2025-04-03 10:45",
        "return_dep": "2025-04-16 13:00",
        "return_arr": "2025-04-16 22:30",
        "duration": "7h 15m",
        "cost": 72000,
        "cancellation": "2%",
        "delays": "Low",
        "audience": "Family Friendly",
        "rating": 78,
        "recommended": True,
        "reason": "Full carrier with vegetarian meals, in-flight entertainment, and good legroom. Highly preferred by family travelers."
    },
    {
        "carrier": "Emirates",
        "departure": "2025-04-03 06:00",
        "arrival": "2025-04-03 14:15",
        "return_dep": "2025-04-16 15:00",
        "return_arr": "2025-04-17 00:30",
        "duration": "8h 15m",
        "cost": 85000,
        "cancellation": "1%",
        "delays": "Medium",
        "audience": "Luxury / Family",
        "rating": 82,
        "recommended": True,
        "reason": "Premium experience with comfortable seats and great service. Popular among family travelers."
    },
    {
        "carrier": "Air France",
        "departure": "2025-04-03 09:00",
        "arrival": "2025-04-03 16:30",
        "return_dep": "2025-04-16 11:00",
        "return_arr": "2025-04-16 19:30",
        "duration": "7h 30m",
        "cost": 78000,
        "cancellation": "3%",
        "delays": "Low",
        "audience": "Budget-Conscious Families",
        "rating": 75,
        "recommended": False,
        "reason": "Reliable carrier with decent meals and comfortable seating. Preferred by budget-conscious family travelers."
    },
    {
        "carrier": "Lufthansa",
        "departure": "2025-04-03 05:00",
        "arrival": "2025-04-03 13:00",
        "return_dep": "2025-04-16 12:00",
        "return_arr": "2025-04-16 21:00",
        "duration": "8h 0m",
        "cost": 80000,
        "cancellation": "4%",
        "delays": "Medium",
        "audience": "Business / Family",
        "rating": 70,
        "recommended": False,
        "reason": "Good option for those who prefer European carriers; slightly higher delay risk."
    },
]

# --- Display Flight Cards ---
st.subheader("Available Flights")
st.markdown("Recommended options are highlighted for your convenience.")

for idx, flight in enumerate(flight_itineraries):
    # Use Streamlit columns and markdown instead of HTML
    col1, col2 = st.columns([1, 10])
    
    with col1:
        if flight["recommended"]:
            st.write("⭐")
    
    with col2:
        if flight["recommended"]:
            st.info(f"**{flight['carrier']}** (Recommended)")
        else:
            st.write(f"**{flight['carrier']}**")
    
    # Outbound flight details
    st.write(f"**Outbound:** {flight['departure']} → {flight['arrival']} ({flight['duration']})")
    
    # Return flight details
    st.write(f"**Return:** {flight['return_dep']} → {flight['return_arr']}")
    
    # Cost and stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cost", f"₹{flight['cost']}")
    with col2:
        st.metric("Cancellation", flight['cancellation'])
    with col3:
        st.metric("Delay Risk", flight['delays'])
    with col4:
        st.metric("Family Rating", f"{flight['rating']}%")
    
    # Additional info
    st.write(f"👥 **For:** {flight['audience']}")
    
    if flight["recommended"]:
        st.success(f"✅ {flight['reason']}")
    
    st.divider()

st.caption("⚠️ Note: Timings, costs, cancellation rates, and ratings are simulated for demo purposes.")
