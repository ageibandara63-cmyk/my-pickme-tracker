import streamlit as st
import pandas as pd
import os

# Software එකේ නම
st.set_page_config(page_title="PickMe Profit Tracker")
st.title("🚖 PickMe Profit Tracker")

FILE_NAME = 'pickme_data.csv'

# දත්ත Load කරගැනීම
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=['Date', 'Income', 'Fuel', 'Profit'])

# දත්ත ඇතුළත් කරන තීරුව
with st.sidebar:
    st.header("නව දත්ත ඇතුළත් කරන්න")
    date = st.date_input("දිනය")
    income = st.number_input("ආදායම (LKR)", min_value=0)
    fuel = st.number_input("තෙල් වියදම (LKR)", min_value=0)
    
    if st.button("Save කරන්න"):
        profit = income - (fuel + (income * 0.15)) # 15% commission එක අඩු කරා
        new_data = pd.DataFrame([[date, income, fuel, profit]], columns=['Date', 'Income', 'Fuel', 'Profit'])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)
        st.success("දත්ත ඇතුළත් කළා!")

# ප්‍රස්ථාර පෙන්වීම
st.subheader("ලාභය පෙන්වන ප්‍රස්ථාරය")
if not df.empty:
    st.line_chart(df.set_index('Date')['Profit'])
    st.write("පසුගිය දත්ත:")
    st.dataframe(df)
else:
    st.info("තවම දත්ත ඇතුළත් කර නැත.")
