import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

@st.cache_data
def load_data(sheet_url):
    df = pd.read_csv(sheet_url)
    return df

sheet_url = 'https://docs.google.com/spreadsheets/d/10K60YsROG3u0Lh_PNE0B3wrwUB0OLFgKjl2ChpRc0ec/export?format=csv'
df = load_data(sheet_url)

st.title("Which day of the week has the highest average total bill?")


if 'chart_selected' not in st.session_state:
    st.session_state.chart_selected = None

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if st.button("Show Chart"):
    st.session_state.chart_selected = np.random.choice(['bar', 'pie'])
    st.session_state.start_time = time.time()


avg_bills = df.groupby('day')['total_bill'].mean()

if st.session_state.chart_selected == 'bar':
    fig, ax = plt.subplots()
    ax.bar(avg_bills.index, avg_bills.values, color='skyblue')
    ax.set_title('Average Bill by Day (Bar Chart)')
    ax.set_xlabel('Day')
    ax.set_ylabel('Average Total Bill')
    st.pyplot(fig)
    st.session_state.chart_displayed = 'Bar Chart'

elif st.session_state.chart_selected == 'pie':
    fig, ax = plt.subplots()
    ax.pie(avg_bills.values, labels=avg_bills.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Average Bill by Day (Pie Chart)')
    st.pyplot(fig)
    st.session_state.chart_displayed = 'Pie Chart'


if st.session_state.chart_selected:
    if st.button("I answered your question"):
        response_time = time.time() - st.session_state.start_time
        st.write(f"You took {response_time:.2f} seconds using {st.session_state.chart_displayed}.")

        # Reset for the next round
        st.session_state.chart_selected = None