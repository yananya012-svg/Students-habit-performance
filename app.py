import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Habits Performance", layout="wide")

st.title("📊 Student Habits Performance Analysis")

# Load dataset
df = pd.read_csv("student_habits_performance.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Missing Values
df.fillna(df.mean(numeric_only=True), inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Feature Engineering
df["Productivity Score"] = (
    df["study_hours_per_day"] * 5
    + df["attendance_percentage"] * 0.3
    - df["social_media_hours"] * 2
)

# Avoid division by zero
df["Study Efficiency"] = (
    df["study_hours_per_day"] /
    df["social_media_hours"].replace(0, np.nan)
)

# Sleep Category
df["Sleep Category"] = pd.cut(
    df["sleep_hours"],
    bins=[0, 6, 8, 12],
    labels=["Poor", "Good", "Excellent"],
    include_lowest=True
)

# Statistics
st.subheader("Summary Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Students", len(df))
col2.metric("Average Study Hours", round(df["study_hours_per_day"].mean(), 2))
col3.metric("Average Attendance", round(df["attendance_percentage"].mean(), 2))

st.write(df.describe())

# Histogram
st.subheader("Study Hours Distribution")

fig, ax = plt.subplots(figsize=(6,4))
ax.hist(df["study_hours_per_day"], bins=10)
ax.set_xlabel("Study Hours")
ax.set_ylabel("Students")
ax.set_title("Study Hours Distribution")
st.pyplot(fig)

# Sleep Categories
st.subheader("Sleep Categories")

sleep = df["Sleep Category"].value_counts()

fig, ax = plt.subplots(figsize=(6,4))
ax.bar(sleep.index.astype(str), sleep.values)
ax.set_xlabel("Category")
ax.set_ylabel("Students")
ax.set_title("Sleep Categories")
st.pyplot(fig)

# Attendance Pie Chart
st.subheader("Attendance Distribution")

attendance = df["attendance_percentage"]

labels = ["Below Average", "Average", "Excellent"]

sizes = [
    len(attendance[attendance < 70]),
    len(attendance[(attendance >= 70) & (attendance < 90)]),
    len(attendance[attendance >= 90])
]

fig, ax = plt.subplots(figsize=(6,6))
ax.pie(sizes, labels=labels, autopct="%1.1f%%")
ax.set_title("Attendance Distribution")
st.pyplot(fig)

# Scatter Plot
st.subheader("Study Hours vs Attendance")

fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(
    df["study_hours_per_day"],
    df["attendance_percentage"]
)
ax.set_xlabel("Study Hours")
ax.set_ylabel("Attendance")
ax.set_title("Study Hours vs Attendance")
st.pyplot(fig)

# Line Plot
st.subheader("Study Hours Line Plot")

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(df["study_hours_per_day"])
ax.set_xlabel("Student Index")
ax.set_ylabel("Study Hours")
ax.set_title("Study Hours")
st.pyplot(fig)

# Top Students
st.subheader("Top 10 Students by Productivity Score")

top_students = df.sort_values(
    "Productivity Score",
    ascending=False
).head(10)

st.dataframe(top_students)

# Poor Sleep Students
st.subheader("Students Sleeping Less Than 6 Hours")

st.dataframe(df[df["sleep_hours"] < 6])

# High Study Hour Students
st.subheader("Students Studying More Than 6 Hours")

st.dataframe(df[df["study_hours_per_day"] > 6])

# Download Processed Dataset
csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Processed Dataset",
    csv,
    file_name="Processed_Student_Productivity.csv",
    mime="text/csv"
)
