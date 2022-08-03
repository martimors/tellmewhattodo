from tellmewhattodo.job.storage import client
import streamlit as st
import pandas as pd


storage_client = client()


st.title("Tasks")

with st.sidebar:
    read = st.button("READ")
    write = st.button("WRITE")
    if read:
        df = storage_client.read()
        st.session_state["alerts"] = df
    elif write:
        storage_client.write(df)

df.set_index("id", inplace=True)
df["datetime"] = pd.to_datetime(df["datetime"])
df["active"] = df["active"].astype(bool)

df.sort_values(by=["active", "datetime"], axis=0, ascending=False, inplace=True)
col_desc, col_ack = st.columns([10, 1])


def strikethrough(text: str) -> str:
    return f"~~{text}~~"


for idx, row in df.iterrows():
    row = row.to_dict()
    current_status = row["active"]
    text = f"{row['datetime']}: {row['description']}"
    if current_status:
        text = strikethrough(text)
    with col_desc:
        st.markdown(text)
    with col_ack:
        c = st.checkbox("ack", key=idx, value=not current_status)
