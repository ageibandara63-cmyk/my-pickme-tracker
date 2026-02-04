import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="PickMe Bike Expense Tracker", layout="wide")
st.title("🏍️ PickMe Bike: ලාභ සහ වියදම් විස්තරය")

FILE_NAME = 'bike_detailed_tracker.csv'

# දත්ත Load කිරීම
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
else:
    df = pd.DataFrame(columns=['Date', 'Income', 'Fuel_Exp', 'Service_Exp', 'Commission', 'Total_Exp', 'Net_Profit'])

with st.sidebar:
    st.header("Daily Entry 📝")
    date_input = st.date_input("දිනය", datetime.now())
    income = st.number_input("අද ලැබුණු මුළු මුදල (LKR)", min_value=0.0, step=100.0)
    
    # උඹේ Settings (අර පරණ logic එකමයි)
    avg_pay_per_km = 40.0
    fuel_per_km = 370 / 40
    service_per_km = 3.0
    
    if st.button("දත්ත ඇතුළත් කරන්න ✅"):
        if income > 0:
            est_km = income / avg_pay_per_km
            
            # වියදම් වෙන් කිරීම
            fuel_exp = est_km * fuel_per_km
            service_exp = est_km * service_per_km
            commission = income * 0.15
            
            total_exp = fuel_exp + service_exp + commission
            profit = income - total_exp
            
            new_row = {
                'Date': pd.to_datetime(date_input),
                'Income': income,
                'Fuel_Exp': round(fuel_exp, 2),
                'Service_Exp': round(service_exp, 2),
                'Commission': round(commission, 2),
                'Total_Exp': round(total_exp, 2),
                'Net_Profit': round(profit, 2)
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success("විස්තර ඇතුළත් කළා!")

# Dashboard
if not df.empty:
    st.subheader("අද දවසේ සාරාංශය")
    last_entry = df.iloc[-1]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("මුළු ආදායම", f"Rs. {last_entry['Income']:,.0f}")
    c2.metric("තෙල් වියදම", f"Rs. {last_entry['Fuel_Exp']:,.0f}")
    c3.metric("සර්විස්/ටයර්", f"Rs. {last_entry['Service_Exp']:,.0f}")
    c4.metric("ශුද්ධ ලාභය", f"Rs. {last_entry['Net_Profit']:,.0f}", delta_color="normal")

    st.divider()

    # වියදම් විශ්ලේෂණය (Pie Chart)
    st.subheader("වියදම් බෙදී යන ආකාරය (මුළු කාලයම)")
    exp_summary = pd.DataFrame({
        'වර්ගය': ['තෙල් (Fuel)', 'නඩත්තු (Service)', 'කොමිස් (Commission)', 'ලාභය (Net Profit)'],
        'ගාණ': [df['Fuel_Exp'].sum(), df['Service_Exp'].sum(), df['Commission'].sum(), df['Net_Profit'].sum()]
    })
    
    # ලස්සනට පේන්න Bar Chart එකක්
    st.bar_chart(data=exp_summary.set_index('වර්ගය'))

    # සම්පූර්ණ දත්ත වගුව
    st.subheader("සවිස්තරාත්මක වාර්තාව (Detailed History)")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)

    # Backup
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Excel විදියට වාර්තාව ගන්න", data=csv, file_name='bike_detailed_report.csv', mime='text/csv')
else:
    st.info("මචං, අද හම්බ කරපු ගාණ දාලා වියදම් විස්තරය බලපන්.")
