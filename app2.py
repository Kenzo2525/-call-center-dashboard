import streamlit as st
import numpy as np
import pandas as pd 
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib.pyplot as plt
import statistics as sts

df = pd.read_excel("call-center-Dataset.xlsx")
df['Date'] = pd.to_datetime(df['Date'])

df

st.sidebar.header("Filters")

# Date Range
date_min = df['Date'].min().date()
date_max = df['Date'].max().date()
date_range = st.sidebar.date_input("Date Range", [date_min, date_max])

# Department
selected_dept = st.sidebar.multiselect("Department", df['Department'].unique(), default=df['Department'].unique())

# Agent Filter
agent_list = df['Agent'].unique().tolist()
selected_agents = st.sidebar.multiselect("Select Agent", options=agent_list, default=agent_list)

# Answered
selected_answered = st.sidebar.multiselect("Answered (Y/N)", df['Answered (Y/N)'].unique(), default=df['Answered (Y/N)'].unique())

# Resolved
selected_resolved = st.sidebar.multiselect("Resolved", df['Resolved'].unique(), default=df['Resolved'].unique())

st.subheader("1. Agent with most calls")
agent_calls = df['Agent'].value_counts()
st.bar_chart(agent_calls)
st.write(f"**Top agent:** {agent_calls.index[0]} with {agent_calls.iloc[0]} calls")

st.subheader("2. Agent with highest satisfaction")
agent_sat = df.groupby('Agent')['Satisfaction rating'].mean().sort_values(ascending=False)
st.bar_chart(agent_sat)
st.write(f"**Top rated:** {agent_sat.index[0]} - {agent_sat.iloc[0]:.2f} / 5 avg rating")
st.dataframe(agent_sat.reset_index().rename(columns={'Satisfaction rating':'Avg Rating'}))

st.subheader("3. Department with most calls")
dept_calls = df['Department'].value_counts()
st.bar_chart(dept_calls)
st.write(f"**Busiest dept:** {dept_calls.index[0]} with {dept_calls.iloc[0]} calls")

st.subheader("4. % Calls Answered")
answered_pct = (df['Answered (Y/N)'] == 'Y').mean() * 100
st.metric("Answered Rate", f"{answered_pct:.1f}%")
st.write(f"Total: {(df['Answered (Y/N)'] == 'Y').sum()} answered out of {len(df)} calls")

st.subheader("5. % Calls Resolved")
resolved_pct = (df['Resolved'] == 'Y').mean() * 100
st.metric("Resolution Rate", f"{resolved_pct:.1f}%")
st.write(f"Total: {(df['Resolved'] == 'Y').sum()} resolved out of {len(df)} calls")

import numpy as np
st.subheader("6. Average Speed of Answer")
df['Speed of Answer'] = pd.to_numeric(df['Speed of Answer'], errors='coerce')
avg_speed = df['Speed of Answer'].mean()
st.metric("Avg Speed", f"{avg_speed:.0f} seconds")

st.subheader("7. Average Talk Duration")
df['AvgTalkDuration'] = pd.to_numeric(df['AvgTalkDuration'], errors='coerce')
avg_talk = df['AvgTalkDuration'].mean()
st.metric("Avg Talk Time", f"{avg_talk:.0f} seconds")

# Bonus: Talk time by agent
talk_by_agent = df.groupby('Agent')['AvgTalkDuration'].mean().sort_values(ascending=False)
st.write("**Talk time by agent:**")
st.bar_chart(talk_by_agent)

import plotly.express as px
st.subheader("8. Hour with most calls")
df['Date'] = pd.to_datetime(df['Date'])
df['Hour'] = df['Date'].dt.hour
hour_calls = df['Hour'].value_counts().sort_index()
fig = px.bar(x=hour_calls.index, y=hour_calls.values, labels={'x':'Hour of Day', 'y':'# Calls'})
st.plotly_chart(fig)
st.write(f"**Busiest hour:** {hour_calls.idxmax()}:00 with {hour_calls.max()} calls")

st.subheader("9. Day with most calls")
df['Day'] = df['Date'].dt.day_name()
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_calls = df['Day'].value_counts().reindex(day_order)
st.bar_chart(day_calls)
st.write(f"**Busiest day:** {day_calls.idxmax()} with {day_calls.max()} calls")

st.subheader("10. Speed of Answer vs Satisfaction")
df['Speed of Answer'] = pd.to_numeric(df['Speed of Answer'], errors='coerce')

fig = px.scatter(df, x='Speed of Answer', y='Satisfaction rating',
                 color='Agent', trendline='ols',
                 labels={'Speed of Answer':'Wait Time (seconds)', 'Satisfaction rating':'rating /5'})
st.plotly_chart(fig)

corr = df[['Speed of Answer', 'Satisfaction rating']].corr().iloc[0,1]
st.metric("Correlation", f"{corr:.2f}")

if corr < -0.3:
    st.success("Faster answers = higher satisfaction")
elif corr > 0.3:
    st.warning("Slower answers = higher satisfaction")
else:
    st.info("Weak/no relationship between speed and satisfaction")