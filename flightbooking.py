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
    highlight = "border:3px solid #00aaff; background-color:#e6f7ff;" if flight["recommended"] else "border:1px solid #ccc; background-color:#f9f9f9;"
    
    st.markdown(f"""
    <div style="border-radius:12px; padding:15px; margin-bottom:15px; {highlight}">
        <h3 style="color:#0066cc;">{flight['carrier']}</h3>
        <p style="color:#0066cc;">
            <b>Departure:</b> {flight['departure']} &nbsp;&nbsp;
            <b>Arrival:</b> {flight['arrival']} &nbsp;&nbsp;
            <b>Duration:</b> {flight['duration']}
        </p>
        <p style="color:#0066cc;">
            <b>Return Departure:</b> {flight['return_dep']} &nbsp;&nbsp;
            <b>Return Arrival:</b> {flight['return_arr']}
        </p>
        <p style="color:#0066cc;"><b>Cost:</b> ₹{flight['cost']}</p>
        <p style="color:#0066cc;">
            <b>Cancellation Rate:</b> {flight['cancellation']} &nbsp;&nbsp;
            <b>Delay Risk:</b> {flight['delays']}
        </p>
        <p style="color:#0066cc;">
            <b>Audience:</b> {flight['audience']} &nbsp;&nbsp;
            <b>Family Rating:</b> {flight['rating']}%
        </p>
        {"<p style='color:#ff0000;'><b>Recommended:</b> ⭐ This flight is suggested for you</p>" if flight["recommended"] else ""}
        {"<p style='color:#0000cc;'><b>Rationale:</b> "+flight['reason']+"</p>" if flight["recommended"] else ""}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("⚠️ Note: Timings, costs, cancellation rates, and ratings are simulated for demo purposes.")