import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Productivity Dashboard",
    page_icon="📚",
    layout="wide"
)

# ---------- TITLE ----------
st.title("📚 Student Productivity Dashboard")
st.markdown("### AI-Based Student Routine & Performance Analysis")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("student_habits_performance.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ---------- CLEAN DATA ----------
df.fillna(df.mean(numeric_only=True), inplace=True)
df.drop_duplicates(inplace=True)

# ---------- FEATURE ENGINEERING ----------
df["Productivity Score"] = (
    df["study_hours_per_day"] * 5
    + df["attendance_percentage"] * 0.3
    - df["social_media_hours"] * 2
)

df["Study Efficiency"] = (
    df["study_hours_per_day"] /
    df["social_media_hours"].replace(0, np.nan)
)

df["Sleep Category"] = pd.cut(
    df["sleep_hours"],
    bins=[0,6,8,12],
    labels=["Poor","Good","Excellent"],
    include_lowest=True
)
st.sidebar.title("🎛 Dashboard Filters")

gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + list(df["gender"].unique())
)

diet = st.sidebar.selectbox(
    "Diet Quality",
    ["All"] + list(df["diet_quality"].unique())
)

if gender != "All":
    df = df[df["gender"] == gender]

if diet != "All":
    df = df[df["diet_quality"] == diet]
    st.markdown("---")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "👨‍🎓 Students",
    len(df)
)

col2.metric(
    "📚 Avg Study Hours",
    round(df["study_hours_per_day"].mean(),2)
)

col3.metric(
    "✅ Avg Attendance",
    round(df["attendance_percentage"].mean(),2)
)

col4.metric(
    "🎯 Avg Exam Score",
    round(df["exam_score"].mean(),2)
)

st.markdown("---")
st.header("📄 Dataset Preview")

show = st.checkbox("Show Complete Dataset")

if show:
    st.dataframe(df)
else:
    st.dataframe(df.head(10))
    st.header("📊 Study Hours Distribution")

fig, ax = plt.subplots(figsize=(7,4))

ax.hist(
    df["study_hours_per_day"],
    bins=10
)

ax.set_title("Study Hours Distribution")
ax.set_xlabel("Study Hours")
ax.set_ylabel("Students")

st.pyplot(fig)
st.header("😴 Sleep Categories")

sleep = df["Sleep Category"].value_counts()

fig, ax = plt.subplots(figsize=(7,4))

ax.bar(
    sleep.index.astype(str),
    sleep.values
)

ax.set_xlabel("Category")
ax.set_ylabel("Students")
ax.set_title("Sleep Categories")

st.pyplot(fig)
st.header("🎯 Attendance Distribution")

attendance = df["attendance_percentage"]

labels = [
    "Below Average",
    "Average",
    "Excellent"
]

sizes = [
    len(attendance[attendance < 70]),
    len(attendance[(attendance >=70) & (attendance <90)]),
    len(attendance[attendance >=90])
]

fig, ax = plt.subplots(figsize=(6,6))

ax.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

ax.set_title("Attendance Distribution")
st.pyplot(fig)

st.header("📈 Study Hours vs Exam Score")

fig, ax = plt.subplots(figsize=(7,4))

ax.scatter(
    df["study_hours_per_day"],
    df["exam_score"]
)

ax.set_xlabel("Study Hours")
ax.set_ylabel("Exam Score")
ax.set_title("Study Hours vs Exam Score")

st.pyplot(fig)
st.header("📉 Productivity Score")

fig, ax = plt.subplots(figsize=(9,4))

ax.plot(
    df["Productivity Score"]
)

ax.set_xlabel("Student")
ax.set_ylabel("Productivity Score")
ax.set_title("Student Productivity")

st.pyplot(fig)
st.header("🏆 Top 10 Students")

top = df.sort_values(
    "exam_score",
    ascending=False
).head(10)

st.dataframe(top)
st.sidebar.header("🧮 Productivity Calculator")

study = st.sidebar.slider(
    "Study Hours",
    0.0,
    12.0,
    5.0
)

attendance = st.sidebar.slider(
    "Attendance %",
    0.0,
    100.0,
    80.0
)

social = st.sidebar.slider(
    "Social Media Hours",
    0.0,
    10.0,
    2.0
)

score = study*5 + attendance*0.3 - social*2

st.sidebar.success(
    f"Predicted Productivity Score : {score:.2f}"
)
st.header("😴 Students Sleeping Less Than 6 Hours")

poor = df[df["sleep_hours"] < 6]

st.dataframe(poor)
st.header("📚 High Study Hour Students")

good = df[df["study_hours_per_day"] > 6]

st.dataframe(good)
st.header("📥 Download Processed Dataset")

csv = df.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    "Processed_Student_Productivity.csv",
    "text/csv"
)
st.markdown("---")

st.markdown(
    """
### 👩‍💻 Developed by Ananya Yadav

**Project:** AI-Based Student Routine & Productivity Dashboard

**Skills Used**

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit

⭐ Thank you for visiting this dashboard!
"""
)
