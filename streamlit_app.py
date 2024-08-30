import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import date


url = "https://docs.google.com/spreadsheets/d/105d9elDqCFDsucC8ZGefz22tn1MuX0X4mcutyxloRfM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, worksheet="tracking", usecols=list(range(5)), ttl = 5)
data = data.dropna(how="all")
exercises = data["Name"].unique()
data = data.sort_values(by="Date", ascending=False)

with st.form(key="Exercise form"):
    col1, col2 = st.columns(2)
    with col1:
        exercise_type = st.selectbox("Exercise", options=exercises, index=None)
        amount_effort = st.text_input(label="Effort")
    with col2:
        amount_rep = st.text_input(label="Rep")
        amount_set = st.number_input(label="Set", min_value=1, max_value=5, step=1)
        comment = st.text_input(label="Comment")

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:

        if not exercise_type or not amount_set or not amount_rep:
            st.warning("You are missing something important here.")
            st.stop()
        else:
            new_exer = pd.DataFrame(
                [
                    {
                        "Name": exercise_type,
                        "Effort": amount_effort,
                        "Rep": amount_rep,
                        "Set": amount_set,
                        "Date": date.today().strftime("%d.%m.%Y"),
                        "Comment": comment,
                    }
                ]
            )

        update_df = pd.concat([data, new_exer], ignore_index=True)
        conn.update(worksheet="tracking", data=update_df)

        st.success("Your submission completed! ")

        st.dataframe(data)


