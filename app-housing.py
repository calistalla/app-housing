from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

plt.style.use("seaborn-v0_8")

st.title("California Housing Data (1990) by Yifei Li")

# Read the CSV next to this script, locally or on Streamlit Cloud.
df = pd.read_csv(Path(__file__).with_name("housing.csv"))

minimum_value = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000,
    step=1,
)

st.subheader("See more filters in the sidebar:")

location_types = df["ocean_proximity"].unique().tolist()
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types,
)
income_level = st.sidebar.radio(
    "Choose income level", ["Low", "Medium", "High"]
)

# Apply all three filters to the same dataframe.
filtered = df[df["median_house_value"] >= minimum_value]
filtered = filtered[filtered["ocean_proximity"].isin(selected_locations)]

if income_level == "Low":
    filtered = filtered[filtered["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered = filtered[
        (filtered["median_income"] > 2.5) & (filtered["median_income"] < 4.5)
    ]
else:
    filtered = filtered[filtered["median_income"] >= 4.5]

if filtered.empty:
    st.info("No districts match these filters. Please adjust your selections.")
else:
    st.map(filtered[["latitude", "longitude"]])

    fig, ax = plt.subplots()
    ax.hist(filtered["median_house_value"], bins=30)
    ax.set_xlabel("Median house value (USD)")
    ax.set_ylabel("Number of districts")
    st.pyplot(fig)
    plt.close(fig)
