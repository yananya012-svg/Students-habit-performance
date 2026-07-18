import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 AI-Based Student Routine & Productivity Analyzer")

df = pd.read_csv("student_habits_performance.csv")

st.subheader("Dataset")
st.dataframe(df.head())

st.subheader("Project Summary")

st.write("Total Students:", len(df))
st.write("Average Study Hours:", round(df["study_hours_per_day"].mean(),2))
st.write("Average Attendance:", round(df["attendance_percentage"].mean(),2))
st.write("Average Sleep Hours:", round(df["sleep_hours"].mean(),2))

st.subheader("Study Hours Distribution")

fig, ax = plt.subplots()

ax.hist(df["study_hours_per_day"], bins=10)

st.pyplot(fig)

st.subheader("Sleep Categories")

sleep = df["Sleep Category"].value_counts()

fig, ax = plt.subplots()

ax.bar(sleep.index, sleep.values)

st.pyplot(fig)

st.subheader("Attendance Distribution")

attendance = df["attendance_percentage"]

labels=["Below Average","Average","Excellent"]

sizes=[
len(attendance[attendance<70]),
len(attendance[(attendance>=70)&(attendance<90)]),
len(attendance[attendance>=90])
]

fig, ax = plt.subplots()

ax.pie(sizes,labels=labels,autopct="%1.1f%%")

st.pyplot(fig)

st.subheader("Study Hours vs Attendance")

fig, ax = plt.subplots()

ax.scatter(df["study_hours_per_day"],df["attendance_percentage"])

ax.set_xlabel("Study Hours")
ax.set_ylabel("Attendance")

st.pyplot(fig)
