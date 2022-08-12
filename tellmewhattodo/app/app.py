from tellmewhattodo.job.storage import client
import streamlit as st
import pandas as pd

st.title("New releases")
st.write("Toggle to dismiss. Updated daily.")

storage_client = client()

df = storage_client.read()
df["active"] = df["active"].map({"True": True, "False": False})
df = df.sort_values(by=["active", "datetime"], ascending=(0, 0))


def highlight_active(s):
    if s["active"]:
        return ["background-color: red"] * len(s)
    else:
        return ["background-color: green"] * len(s)


# Interactive
col1, col2 = st.columns([10, 1])
df = df.sort_values(by=["active", "datetime"], ascending=(0, 0))
description = df["id"] + ": " + df["description"]
with col1:
    option = st.selectbox("Alert", description)
with col2:
    button = st.button("Toggle")

if button:
    temp = df.copy()
    temp["temp"] = description
    ids = temp.loc[temp["temp"] == option]
    current_active = df.loc[df["id"].isin(ids["id"]), "active"].iloc[0]
    df.loc[df["id"].isin(ids["id"]), "active"] = not current_active


# Make sure df is sorted
df = df.sort_values(by=["active", "datetime"], ascending=(0, 1))
st.dataframe(df.style.apply(highlight_active, axis=1), 1000, 2000)

storage_client.write(df)
