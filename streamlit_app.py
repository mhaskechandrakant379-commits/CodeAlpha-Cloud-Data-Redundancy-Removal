
import sqlite3
from pathlib import Path

import streamlit as st

# ---------------- Page configuration ----------------
st.set_page_config(
    page_title="Cloud Data Redundancy Removal",
    page_icon="☁️",
    layout="wide",
)

DB_PATH = Path(__file__).parent / "streamlit_data.db"


# ---------------- Database ----------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE
            )
            """
        )


def add_user(name, email):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name.strip(), email.strip().lower()),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_users():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, name, email FROM users ORDER BY id DESC"
        ).fetchall()


def delete_user(user_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))


init_db()

# ---------------- Header ----------------
st.title("☁️ Cloud Data Redundancy Removal System")
st.markdown(
    "A cloud-oriented demo for detecting duplicate records "
    "and maintaining unique user data."
)

st.caption("Demo interface | Python • Streamlit • SQLite")

st.divider()

# ---------------- Metrics ----------------
users = get_users()
total_records = len(users)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Unique Records", total_records)

with col2:
    st.metric("Duplicate Prevention", "Enabled")

with col3:
    st.metric("Storage", "SQLite Demo DB")

st.divider()

# ---------------- Add record ----------------
left, right = st.columns([1, 1.5], gap="large")

with left:
    st.subheader("➕ Add a Record")
    st.write("Enter a name and email to test duplicate detection.")

    with st.form("add_user_form", clear_on_submit=True):
        name = st.text_input("Full Name", placeholder="e.g. Rahul Patil")
        email = st.text_input("Email Address", placeholder="e.g. rahul@example.com")
        submitted = st.form_submit_button(
            "Add Record",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            clean_name = name.strip()
            clean_email = email.strip().lower()

            if not clean_name or not clean_email:
                st.error("Please enter both name and email.")
            elif "@" not in clean_email or "." not in clean_email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            elif add_user(clean_name, clean_email):
                st.success("Unique record added successfully!")
                st.rerun()
            else:
                st.error(
                    "Duplicate Data Detected! "
                    "A record with this email already exists."
                )

with right:
    st.subheader("📋 Stored Records")

    if users:
        for user in users:
            with st.container(border=True):
                details, action = st.columns([4, 1])

                with details:
                    st.write(f"**{user['name']}**")
                    st.caption(user["email"])
                    st.caption(f"Record ID: {user['id']}")

                with action:
                    if st.button(
                        "Delete",
                        key=f"delete_{user['id']}",
                        use_container_width=True,
                    ):
                        st.session_state["confirm_delete"] = user["id"]

                if st.session_state.get("confirm_delete") == user["id"]:
                    st.warning(f"Delete record for {user['name']}?")
                    confirm_col, cancel_col = st.columns(2)

                    with confirm_col:
                        if st.button(
                            "Confirm",
                            key=f"confirm_{user['id']}",
                            type="primary",
                        ):
                            delete_user(user["id"])
                            st.session_state.pop("confirm_delete", None)
                            st.rerun()

                    with cancel_col:
                        if st.button("Cancel", key=f"cancel_{user['id']}"):
                            st.session_state.pop("confirm_delete", None)
                            st.rerun()
    else:
        st.info("No records yet. Add a record to get started.")

st.divider()

# ---------------- Explanation ----------------
with st.expander("ℹ️ How this demo works"):
    st.markdown(
        """
        1. **Input:** Enter a name and email address.
        2. **Normalization:** Email addresses are converted to lowercase.
        3. **Duplicate detection:** A unique database constraint prevents
           the same email from being stored more than once.
        4. **Record management:** View stored records and delete them when needed.

        This is a demonstration interface. It uses a separate SQLite database
        and does not connect to the existing AWS Flask application's database.
        """
    )

st.caption(
    "Portfolio demo — do not enter real personal or confidential information. "
    "Streamlit Cloud's local filesystem is not guaranteed to be persistent."
)