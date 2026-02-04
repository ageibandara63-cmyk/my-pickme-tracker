import streamlit as st
import pandas as pd
import os
from datetime import datetime

# පිටුවේ සැකසුම්
st.set_page_config(page_title="PickMe Bike Profit Tracker", layout="wide")
st.title("🏍️ PickMe Bike Business Tracker")

FILE_NAME = 'bike_profit_data.csv'

# දත්ත Load කිරීම
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
else:
    df = pd.DataFrame(columns=['Date', 'Income', 'KM_Driven', 'Expenses', 'Profit'])

# Sidebar එකේ Inputs
with st.sidebar:
    st.header("අද දවසේ විස්තර")
    date_input = st.date_input("දිනය", datetime.now())
    income = st.number_input("මුළු ආදායම (LKR)", min_value=0.0, step=100.0)
    km_driven = st.number_input("දුවපු මුළු දුර (KM)", min_value=0.0, step=1.0)
    
    # උඹේ බයික් එකේ ගණනය කිරීම්
    fuel_per_km = 370 / 40  # රු. 9.25 (ලීටරේට 40km නම්)
    service_parts_per_km = 3.00 # සර්විස් සහ ටයර් වලට (උඹේ chart එකේ විදියට)
    fixed_cost_daily = 50.00 # ලයිසන්/ඉන්ෂුවරන්ස් වගේ ඒවට දවසකට
    
    if st.button("දත්ත ඇතුළත් කරන්න ✅"):
        commission = income * 0.15 # PickMe 15%
        # සම්පූර්ණ වියදම = (දුවපු KM x KM එකකට වියදම) + කොමිස් + ස්ථාවර වියදම්
        total_exp = (km_driven * (fuel_per_km + service_parts_per_km)) + commission + fixed_cost_daily
        profit = income - total_exp
        
        new_row = {
            'Date': pd.to_datetime(date_input),
            'Income': income,
            'KM_Driven': km_driven,
            'Expenses': round(total_exp, 2),
            'Profit': round(profit, 2)
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)
        st.success("දත්ත සේව් වුණා මචං!")

# Dashboard Display
if not df.empty:
    st.subheader("ව්‍යාපාරික සාරාංශය")
    c1, c2, c3 = st.columns(3)
    c1.metric("මුළු ආදායම", f"Rs. {df['Income'].sum():,.0f}")
    c2.metric("මුළු වියදම (Maintenance ඇතුළුව)", f"Rs. {df['Expenses'].sum():,.0f}")
    c3.metric("නියම ශුද්ධ ලාභය", f"Rs. {df['Profit'].sum():,.0f}")

    st.divider()
    
    # ප්‍රස්ථාරය
    st.subheader("දිනපතා ලාභය")
    st.line_chart(df.set_index('Date')['Profit'])
    
    # වගුව
    st.write("පසුගිය දත්ත:")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

    # Backup Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Excel/CSV විදියට Backup ගන්න", data=csv, file_name='my_bike_profit.csv', mime='text/csv')
else:
    st.info("මචං, අද හයර් දුවලා ඉවර වෙලා දුවපු KM ගාණයි, ලැබුණු සල්ලි ගාණයි sidebar එකට දාපන්.")
