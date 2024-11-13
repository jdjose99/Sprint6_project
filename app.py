import pandas as pd
import plotly_express as px
import streamlit as st

df = pd.read_csv("vehicles_us.csv")
df["manufacturer"] = df["model"].apply(lambda x: x.split()[0])

columns_to_fill = ["model_year", "cylinders", "odometer", "is_4wd"]

for column in columns_to_fill:
    median_value = df[column].median()
    df[column].fillna(median_value, inplace=True)

removed_outliers = df[
    (df["price"] >= 500)
    & (df["price"] <= 150000)
    & (df["odometer"] >= 0)
    & (df["odometer"] <= 300000)
]

df = removed_outliers

st.header("Data viewer")
st.dataframe(df)

st.header("Vehicle Types by Manufacturer")
fig = px.histogram(df, x="manufacturer", color="type")
st.write(fig)

st.header("Price vs Condition")
fig = px.histogram(df, x="price", color="condition")
st.write(fig)

st.header("Transmission Type by Manufacturer")
fig = px.histogram(df, x="manufacturer", color="transmission")
st.write(fig)

st.header("Price vs Year of Manufacture")

vehicle_types = df["type"].unique()
selected_type = st.selectbox("Select a Vehicle Type:", options=vehicle_types)

filtered_df = df[df["type"] == selected_type]

fig = px.scatter(filtered_df, x="model_year", y="price", color="manufacturer")
st.write(fig)

st.header("Relationship between Odometer & Year of Manufacture")

remove_high_odometer = st.checkbox("Remove vehicles with odometer over 500,000")

if remove_high_odometer:
    filtered_df = df[df["odometer"] <= 500000]
else:
    filtered_df = df

fig = px.scatter(filtered_df, x="model_year", y="odometer", color="manufacturer")
st.write(fig)
