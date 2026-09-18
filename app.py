import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Internship Tracker Pro",
    page_icon="💼",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #fbcfe8 0%, transparent 25%),
        radial-gradient(circle at top right, #c4b5fd 0%, transparent 25%),
        radial-gradient(circle at bottom left, #bfdbfe 0%, transparent 25%),
        linear-gradient(
            135deg,
            #faf5ff,
            #f3e8ff,
            #eef2ff
        );

    color: #1f2937;
}

h1, h2, h3 {
    color: #2d1b69 !important;
    font-weight: 700;
}

p, label, div, span {
    color: #1f2937 !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #ffffff,
        #f8f4ff
    );
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #e9d5ff;
    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
    text-align: center;
}

[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    font-weight: 600 !important;
}

.stButton button {
    background: linear-gradient(
        135deg,
        #a78bfa,
        #c4b5fd
    );
    color: white !important;
    border-radius: 14px;
    border: none;
    font-weight: 700;
    transition: 0.3s;
    box-shadow: 0px 4px 12px rgba(167,139,250,0.35);
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 8px 20px rgba(167,139,250,0.45);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #e9d5ff,
        #ddd6fe
    );
}

.stTextInput input,
.stNumberInput input {
    background-color: white;
    border: 2px solid #ddd6fe;
    border-radius: 14px;
    padding: 10px;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #a78bfa;
}

div[data-baseweb="select"] {
    background-color: white;
    border-radius: 14px;
}
[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
}
.stTextInput input,
.stNumberInput input {
    background-color: white;
    border: 2px solid #ddd6fe;
    border-radius: 14px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("🌸 Navigation")
st.sidebar.success("Smart Internship Tracker Pro")

st.markdown("""
<div style="
padding:20px;
border-radius:20px;
background:linear-gradient(135deg,#fdf4ff,#ede9fe);
border:1px solid #ddd6fe;
margin-bottom:20px;
">
<h1 style="margin:0;">
💼 Smart Internship Tracker Pro
</h1>
<p style="font-size:18px;">
Welcome back, Saranya 🌸<br>
Track and manage all your internship applications in one place.
</p>
</div>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("internships.db")
cursor = conn.cursor()

# ---------------- ADD APPLICATION ----------------

st.subheader("➕ Add Internship")

with st.form("add_application_form"):

    company = st.text_input("Company Name")

    role = st.text_input("Role")

    status = st.selectbox(
        "Status",
        ["Applied", "Interview", "Rejected", "Selected"]
    )

    submitted = st.form_submit_button("Add Application")

    if submitted:

        if company.strip() == "" or role.strip() == "":
            st.error("Please enter Company and Role.")

        else:

            cursor.execute(
                """
                INSERT INTO applications(company, role, status)
                VALUES (?, ?, ?)
                """,
                (company, role, status.lower())
            )

            conn.commit()

            st.success("Application Added Successfully!")

# ---------------- VIEW APPLICATIONS ----------------

st.subheader("📋 All Applications")

cursor.execute("SELECT * FROM applications")

applications = cursor.fetchall()

df = pd.DataFrame(
    applications,
    columns=[
        "ID",
        "Company",
        "Role",
        "Status"
    ]
)

st.dataframe(
    df,
    use_container_width=True
)

# ---------------- STATISTICS ----------------

st.subheader("📊 Statistics")

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

col1.metric("📄 Total", total)
col2.metric("📨 Applied", applied)
col3.metric("🎤 Interview", interview)
col4.metric("❌ Rejected", rejected)
col5.metric("🏆 Selected", selected)

# ---------------- DONUT CHART ----------------

st.subheader("🍩 Application Status Overview")

labels = ["Applied", "Interview", "Rejected", "Selected"]

sizes = [
    applied,
    interview,
    rejected,
    selected
]

if sum(sizes) > 0:

    colors = [
        "#A5B4FC",
        "#F9A8D4",
        "#FCA5A5",
        "#86EFAC"
    ]

    fig, ax = plt.subplots(
        figsize=(6, 6),
        facecolor="#f8f4ff"
    )

    ax.set_facecolor("#f8f4ff")

    ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={
            "width": 0.45,
            "edgecolor": "white"
        }
    )

    ax.axis("equal")

    st.pyplot(fig)

else:
    st.info("Add applications to view analytics.")

# ---------------- SEARCH ----------------

# ---------------- SEARCH ----------------

st.subheader("🔍 Search Applications")

search_company = st.text_input(
    "Enter Company Name to Search"
)

if search_company:

    cursor.execute(
        "SELECT * FROM applications WHERE company LIKE ?",
        ("%" + search_company + "%",)
    )

    results = cursor.fetchall()

    if results:

        search_df = pd.DataFrame(
            results,
            columns=[
                "ID",
                "Company",
                "Role",
                "Status"
            ]
        )

        st.dataframe(
            search_df,
            use_container_width=True
        )

    else:
        st.warning("No applications found.")

# ---------------- UPDATE ----------------

st.subheader("✏️ Update Status")

application_id = st.number_input(
    "Application ID",
    min_value=1,
    step=1
)

new_status = st.selectbox(
    "New Status",
    ["Applied", "Interview", "Rejected", "Selected"]
)

if st.button("Update Status"):

    cursor.execute(
        """
        UPDATE applications
        SET status = ?
        WHERE id = ?
        """,
        (new_status.lower(), int(application_id))
    )

    conn.commit()

    st.success("Status Updated Successfully!")

    st.rerun()

# ---------------- DELETE ----------------

# ---------------- DELETE ----------------

st.subheader("🗑️ Delete Application")

delete_id = st.number_input(
    "Enter Application ID to Delete",
    min_value=1,
    step=1,
    key="delete_id"
)

if st.button("Delete Application"):

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (int(delete_id),)
    )

    conn.commit()

    st.success("Application Deleted Successfully!")

    st.rerun()
# ---------------- EXPORT CSV ----------------

st.subheader("📥 Export Applications")

cursor.execute("SELECT * FROM applications")

data = cursor.fetchall()

df_export = pd.DataFrame(
    data,
    columns=[
        "ID",
        "Company",
        "Role",
        "Status"
    ]
)

csv = df_export.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="applications.csv",
    mime="text/csv"
)


# ---------------- CLOSE DB ----------------

conn.close()