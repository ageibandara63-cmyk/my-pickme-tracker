import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="PickMe Bike Pro (No Meter)", layout="wide")
st.title("🏍️ PickMe Bike Profit Tracker (Income Based)")

FILE_NAME = 'bike_income_tracker.csv'

# දත්ත Load කිරීම
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
else:
    df = pd.DataFrame(columns=['Date', 'Total_Income', 'Calculated_KM', 'Expenses', 'Net_Profit'])

with st.sidebar:
    st.header("Daily Entry 📝")
    date_input = st.date_input("දිනය", datetime.now())
    income = st.number_input("අද ලැබුණු මුළු මුදල (LKR)", min_value=0.0, step=100.0)
    
    # උඹේ ගණනය කිරීම් (Settings)
    avg_pay_per_km = 40.00  # පික්මී එකෙන් $1km$ කට දෙන සාමාන්‍ය ගාණ
    fuel_cost_per_km = 370 / 40 # ලීටරේට $40km$ කරන නිසා $1km$ කට තෙල් වියදම
    maintenance_per_km = 3.00 # සර්විස් සහ ටයර්
    
    if st.button("Save Data ✅"):
        if income > 0:
            # ලැබුණු මුදලෙන් දුවපු දුර අනුමාන කිරීම
            est_km = income / avg_pay_per_km
            
            commission = income * 0.15 # PickMe 15%
            # වියදම = (අනුමාන KM x KM එකකට වියදම) + කොමිස්
            running_cost = est_km * (fuel_cost_per_km + maintenance_per_km)
            total_exp = running_cost + commission
            profit = income - total_exp
            
            new_row = {
                'Date': pd.to_datetime(date_input),
                'Total_Income': income,
                'Calculated_KM': round(est_km, 2),
                'Expenses': round(total_exp, 2),
                'Net_Profit': round(profit, 2)
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success(f"දත්ත සේව් කරා! අද දුවපු දුර (දළ වශයෙන්): {est_km:.2f} KM")
        else:
            st.warning("කරුණාකර ආදායම ඇතුළත් කරන්න.")

# Dashboard
if not df.empty:
    st.subheader("ව්‍යාපාරික වාර්තාව")
    c1, c2, c3 = st.columns(3)
    c1.metric("මුළු ආදායම", f"Rs. {df['Total_Income'].sum():,.0f}")
    c2.metric("මුළු වියදම", f"Rs. {df['Expenses'].sum():,.0f}")
    c3.metric("නියම ශුද්ධ ලාභය", f"Rs. {df['Net_Profit'].sum():,.0f}")

    st.divider()
    
    # ප්‍රස්ථාර
    st.subheader("දිනපතා ලාභය (Daily Profit)")
    st.line_chart(df.set_index('Date')['Net_Profit'])
    
    # වගුව
    st.write("පසුගිය වාර්තා:")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

    # Backup
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Excel Backup ගන්න", data=csv, file_name='bike_profit_backup.csv', mime='text/csv')
else:
    st.info("මචං, අද හම්බ කරපු මුළු ගාණ Sidebar එකේ දාලා ලාභය බලපන්.")
