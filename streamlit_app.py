
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Uber Pickups Explorer", layout="wide")

st.title("Uber Pickups Explorer")
st.write("Explore simulated Uber pickup locations in New York City.")

@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    return pd.DataFrame({
        "date": pd.date_range("2014-05-01", periods=n, freq="h"),
        "lat": np.random.uniform(40.60, 40.85, n),
        "lon": np.random.uniform(-74.05, -73.75, n),
        "hour": np.random.randint(0, 24, n)
    })

data = load_data()

st.sidebar.header("Filters")
hour_range = st.sidebar.slider(
    "Select an hour range",
    min_value=0,
    max_value=23,
    value=(8, 18)
)
show_map = st.sidebar.checkbox("Show pickup map", value=True)

filtered = data[data["hour"].between(hour_range[0], hour_range[1])]

st.metric("Pickups shown", len(filtered))

st.subheader("Pickups by hour")
histogram = filtered["hour"].value_counts().sort_index()
st.bar_chart(histogram)

if show_map:
    st.subheader("Pickup locations")
    map_data = filtered.rename(
        columns={"lat": "latitude", "lon": "longitude"}
    )
    st.map(map_data[["latitude", "longitude"]])

st.caption("Streamlit data exploration demo.")