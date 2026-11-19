# @language  Python
# @updated   2026-11-19
# @changed   Added a minimal interactive Streamlit starter app.

import streamlit as st

st.set_page_config(page_title="ISOM Project", page_icon="👋", layout="centered")

st.title("👋 ISOM Project")
st.write("Welcome! Your Streamlit app is ready to use.")

# Personalize the welcome message using the visitor's name.
name = st.text_input("What's your name?", placeholder="Enter your name")
if name.strip():
    st.success(f"Hello, {name.strip()}! Welcome to the ISOM project.")

# Preview a quadratic sequence with an adjustable number of data points.
st.subheader("Try an interactive chart")
points = st.slider("Number of data points", min_value=5, max_value=50, value=15)
st.line_chart({"Value": [number**2 for number in range(points)]})

st.caption("Built with Streamlit · ISOM Project")
