import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Smart Internship Tracker Pro",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Smart Internship Tracker Pro")

st.markdown("Track your internship applications easily.")

st.sidebar.title("Navigation")

st.sidebar.success("Project 2 - Streamlit Version")

st.header("Dashboard")

conn = sqlite3.connect("internships.db")
cursor = conn.cursor()

st.subheader("Add Internship")

company = st.text_input("Company Name")

role = st.text_input("Role")

status = st.selectbox(
    "Status",
    ["Applied", "Interview", "Rejected", "Selected"]
)

if st.button("Add Application"):

    cursor.execute(
        """
        INSERT INTO applications(company, role, status)
        VALUES (?, ?, ?)
        """,
        (company, role, status.lower())
    )

    conn.commit()

    st.success("Application Added Successfully!")


st.subheader("All Applications")

cursor.execute("SELECT * FROM applications")

applications = cursor.fetchall()

st.table(applications)
st.subheader("Statistics")

cursor.execute("SELECT COUNT(*) FROM applications")
total = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM applications WHERE status='applied'"
)
applied = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM applications WHERE status='interview'"
)
interview = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM applications WHERE status='rejected'"
)
rejected = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM applications WHERE status='selected'"
)
selected = cursor.fetchone()[0]

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total", total)
col2.metric("Applied", applied)
col3.metric("Interview", interview)
col4.metric("Rejected", rejected)
col5.metric("Selected", selected)
st.subheader("Search Applications")

search_company = st.text_input("Enter Company Name to Search")

if search_company:

    cursor.execute(
        "SELECT * FROM applications WHERE company LIKE ?",
        ("%" + search_company + "%",)
    )

    results = cursor.fetchall()

    if results:
        st.table(results)
    else:
        st.warning("No applications found.")