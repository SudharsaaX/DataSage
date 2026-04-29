import streamlit as st
import requests
import pandas as pd
import time
from llm import explain_sql

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(
    page_title="DataSage",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

h1 {
    font-weight: 700;
    letter-spacing: -1px;
}

[data-testid="stSidebar"] {
    padding-top: 1rem;
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("DataSage")
st.caption("Ask your data. Get instant insights.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        if "sql" in msg:
            st.markdown("**SQL Query**")
            st.code(msg["sql"], language="sql")

        if "explanation" in msg:
            st.markdown("**Explanation**")
            st.write(msg["explanation"])

        if "result" in msg and isinstance(msg["result"], list):
            df = pd.DataFrame(msg["result"])
            st.markdown("**Data**")
            st.dataframe(df, use_container_width=True)

def type_text(text):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(output)
        time.sleep(0.008)

user_input = st.chat_input("Ask DataSage...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Processing..."):
        response = requests.post(API_URL, json={"question": user_input})
        data = response.json()

    if "response" in data:
        with st.chat_message("assistant"):
            type_text(data["response"])

        st.session_state.messages.append({
            "role": "assistant",
            "content": data["response"]
        })
        st.stop()

    sql_query = data.get("sql", "")
    result = data.get("result", "")

    with st.spinner("Analyzing query..."):
        explanation = explain_sql(sql_query)

    with st.chat_message("assistant"):
        type_text("Analysis complete.")

        st.markdown("### SQL Query")
        st.code(sql_query, language="sql")

        st.markdown("### Explanation")
        st.write(explanation)

        if isinstance(result, list) and len(result) > 0:
            df = pd.DataFrame(result)
            st.session_state.df = df

            st.markdown("### Data")
            st.dataframe(df, use_container_width=True)
        else:
            st.write(result)

    st.session_state.messages.append({
        "role": "assistant",
        "content": "Analysis complete.",
        "sql": sql_query,
        "explanation": explanation,
        "result": result
    })

st.sidebar.title("DataSage")

df = st.session_state.df

st.markdown("""
<style>
section[data-testid="stSidebar"] .block-container {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}
section[data-testid="stSidebar"] .stSlider,
section[data-testid="stSidebar"] .stMultiSelect {
    margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

if df is not None:

    if st.sidebar.button("Reset filters"):
        st.session_state.df = df
        st.experimental_rerun()

    filtered_df = df.copy()

    for col in df.columns:

        with st.sidebar.expander(col, expanded=False):

            if df[col].dtype == "object":
                options = sorted(df[col].dropna().unique().tolist())
                selected = st.multiselect(
                    "Values",
                    options,
                    default=options,
                    key=f"filter_{col}"
                )
                filtered_df = filtered_df[filtered_df[col].isin(selected)]

            elif pd.api.types.is_numeric_dtype(df[col]):
                min_val = float(df[col].min())
                max_val = float(df[col].max())

                selected_range = st.slider(
                    "Range",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                    key=f"slider_{col}"
                )

                filtered_df = filtered_df[
                    (filtered_df[col] >= selected_range[0]) &
                    (filtered_df[col] <= selected_range[1])
                ]

    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtered Data")
    st.sidebar.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="datasage_export.csv",
        mime="text/csv"
    )