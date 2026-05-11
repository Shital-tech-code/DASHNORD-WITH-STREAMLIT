import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# =========================
# 🔐 LOGIN SYSTEM
# =========================
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Hive Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
    st.stop()
       # =========================
# AUTO REFRESH DASHBOARD
# =========================
st_autorefresh(
    interval=1200000,   # 20 
    limit=None,
    key="dashboard_refresh"
)

# =========================
# PAGE SETTINGS
# =========================
st.set_page_config(layout="wide")
st_autorefresh(interval=1200000, key="refresh")  # 20 min refresh

# =========================
# LOCATION
# =========================
st.sidebar.header("📍 Select Location")

location = st.sidebar.selectbox(
    "Choose Location",
    ["Pandharkaoda", "Wardha (MGIRI)"]
)

if location == "Pandharkaoda":
    url = "https://docs.google.com/spreadsheets/d/1gjlu4F-iNqhjrT57mpU7vGQOgXtjMer6i2Z3dDRbrFo/export?format=csv&gid=0"
else:
    url = "https://docs.google.com/spreadsheets/d/1gjlu4F-iNqhjrT57mpU7vGQOgXtjMer6i2Z3dDRbrFo/export?format=csv&gid=1479038266"

# =========================
# # =========================
# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=60)
def load_data(url, location):

    # =========================
    # LOAD CSV
    # =========================
    if location == "Pandharkaoda":

        df = pd.read_csv(
            url,
            header=None,
            low_memory=False
        )

        df = df.dropna(axis=1, how='all')   # remove empty columns
        df = df.iloc[:, 0:10]               # keep correct columns

        df.columns = [
            "Timestamp",
            "Hive_ID",
            "Status",
            "Temperature",
            "Humidity",
            "Weight 1",
            "Weight 2",
            "Total Weight",
            "Latitude",
            "Longitude"
        ]

    else:

        df = pd.read_csv(
            url,
            low_memory=False
        )

        df.columns = df.columns.str.strip()

    # =========================
    # CLEANING
    # =========================
    df['Timestamp'] = pd.to_datetime(
        df['Timestamp'],
        dayfirst=True,
        errors='coerce'
    )

    for col in [
        "Temperature",
        "Humidity",
        "Weight 1",
        "Weight 2"
    ]:

        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors='coerce'
            )

    # Remove invalid rows
    df = df.dropna(
        subset=[
            'Timestamp',
            'Weight 1',
            'Weight 2'
        ]
    )

    # Sort by time
    df = df.sort_values('Timestamp')

    return df


# =========================
# LOAD DATA CALL
# =========================
df = load_data(url, location)

if df.empty:
    st.error("No data loaded")
    st.stop()
# =========================
# TITLE
# =========================
st.title("🐝 Hive Monitoring Dashboard")
st.markdown(f"### 📍 Location: {location}")

# =========================
# LIVE DATA
# =========================
latest = df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Temperature", float(latest.get('Temperature', 0)))
col2.metric("Humidity", float(latest.get('Humidity', 0)))
col3.metric("Weight 1", float(latest.get('Weight 1', 0)))
col4.metric("Weight 2", float(latest.get('Weight 2', 0)))

# ✅ Last updated time
st.markdown(f"🕒 Last Updated: {latest['Timestamp']}")

# =========================
# DATE FILTER
# =========================
st.sidebar.header("📅 Filter")

start_date = st.sidebar.date_input("Start Date", df['Timestamp'].min().date())
end_date = st.sidebar.date_input("End Date", df['Timestamp'].max().date())

filtered = df[
    (df['Timestamp'].dt.date >= start_date) &
    (df['Timestamp'].dt.date <= end_date)
].copy()

# =========================
# 📈 REAL-TIME GRAPH
# =========================
import matplotlib.dates as mdates

st.markdown("### 📈 Weight Over Time")

# =========================
# REALTIME GRAPH DATA ONLY
# =========================
realtime_df = filtered.iloc[-200:].copy()

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(
    realtime_df['Timestamp'],
    realtime_df['Weight 1'],
    label="Weight 1"
)

ax.plot(
    realtime_df['Timestamp'],
    realtime_df['Weight 2'],
    label="Weight 2"
)
# ✅ CLEAN TIME FORMAT
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# ✅ Reduce number of labels (VERY IMPORTANT)
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

ax.set_xlabel("Time")
ax.set_ylabel("Weight (kg)")
ax.legend()

ax.grid(True, linestyle='--', alpha=0.5)

plt.xticks(rotation=30)
plt.tight_layout()

st.pyplot(fig)

# =========================
# 📊 MODE SELECTOR
# =========================
mode = st.radio(
    "Select Trend Mode",
    ["Auto", "Daily", "Weekly", "Monthly"],
    horizontal=True
)
# =========================
# 📊 TIME GROUP FILTER
# =========================
time_mode = st.selectbox(
    "Select Time View",
    ["Day", "Week", "Month"]
)
# =========================
# =========================
# 📊 TREND BASED ON FILTER
# =========================
st.markdown("### 📊 Weight Trend")

plot_df = filtered.copy()

fig, ax = plt.subplots(figsize=(10, 4))

# =========================
# 🔹 DAILY VIEW
# =========================
if time_mode == "Day":
    st.info("📅 Daily View")

    ax.plot(plot_df['Timestamp'], plot_df['Weight 1'], label="Weight 1")
    ax.plot(plot_df['Timestamp'], plot_df['Weight 2'], label="Weight 2")

    import matplotlib.dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %H:%M'))

# =========================
# # =========================
# # =========================
# # =========================
# 🔹 WEEKLY VIEW
# =========================
elif time_mode == "Week":

    st.info("📅 Weekly View")

    # -------------------------
    # COPY DATA
    # -------------------------
    week_plot_df = plot_df.copy()

    # -------------------------
    # Convert datetime
    # -------------------------
    week_plot_df['Timestamp'] = pd.to_datetime(
        week_plot_df['Timestamp'],
        dayfirst=True,
        errors='coerce'
    )

    week_plot_df = week_plot_df.dropna(subset=['Timestamp'])

    # -------------------------
    # SHOW DATA FROM APRIL 2026
    # -------------------------
    week_plot_df = week_plot_df[
        week_plot_df['Timestamp'] >= pd.Timestamp("2026-04-01")
    ]

    # -------------------------
    # MONTH COLUMN
    # -------------------------
    week_plot_df['Month'] = week_plot_df['Timestamp'].dt.strftime('%B %Y')

    # -------------------------
    # MONTH SORT
    # -------------------------
    week_plot_df['Month Sort'] = week_plot_df['Timestamp'].dt.to_period('M')

    # -------------------------
    # WEEK PERIOD
    # -------------------------
    week_plot_df['Week Period'] = week_plot_df['Timestamp'].dt.to_period('W')

    # -------------------------
    # WEEK START / END
    # -------------------------
    week_plot_df['Week Start'] = week_plot_df['Week Period'].apply(
        lambda x: x.start_time.date()
    )

    week_plot_df['Week End'] = week_plot_df['Week Period'].apply(
        lambda x: x.end_time.date()
    )

    # -------------------------
    # WEEK LABEL
    # -------------------------
    week_plot_df['Week Label'] = week_plot_df.apply(
        lambda x:
        f"{x['Week Start'].strftime('%d %b')} → "
        f"{x['Week End'].strftime('%d %b')}",
        axis=1
    )

    # -------------------------
    # WEEKLY SUMMARY
    # -------------------------
    week_df = week_plot_df.groupby(
        [
            'Month',
            'Month Sort',
            'Week Period',
            'Week Label'
        ]
    )[
        ['Weight 1', 'Weight 2']
    ].mean().reset_index()

    # -------------------------
    # SORT WEEKS
    # -------------------------
    week_df = week_df.sort_values(
        by=['Month Sort', 'Week Period'],
        ascending=False
    )

    # -------------------------
    # MONTH ORDER
    # -------------------------
    month_order = (
        week_df['Month']
        .drop_duplicates()
        .tolist()
    )

    # -------------------------
    # MONTH SELECTOR
    # -------------------------
    selected_month = st.selectbox(
        "📅 Select Month",
        month_order
    )

    # -------------------------
    # FILTER MONTH
    # -------------------------
    month_weeks = week_df[
        week_df['Month'] == selected_month
    ]

    # -------------------------
    # SESSION STATE
    # -------------------------
    available_weeks = month_weeks['Week Period'].astype(str).tolist()

    if (
        "selected_week" not in st.session_state
        or st.session_state.selected_week not in available_weeks
    ):

        st.session_state.selected_week = available_weeks[0]

    # -------------------------
    # MONTH TITLE
    # -------------------------
    st.markdown(f"## 📆 Weeks in {selected_month}")

    # -------------------------
    # WEEK CARDS
    # -------------------------
    cols = st.columns(3)

    for i, row in month_weeks.iterrows():

        week_key = str(row['Week Period'])

        col = cols[i % 3]

        is_selected = (
            st.session_state.selected_week == week_key
        )

        border = (
            "3px solid #4CAF50"
            if is_selected
            else "1px solid #ddd"
        )

        bg = (
            "#e8f5e9"
            if is_selected
            else "#ffffff"
        )

        # -------------------------
        # BUTTON
        # -------------------------
        if col.button(
            f"📅 {row['Week Label']}",
            key=week_key,
            use_container_width=True
        ):
            st.session_state.selected_week = week_key

        # -------------------------
        # CARD
        # -------------------------
        col.markdown(
            f"""
            <div style="
                padding:12px;
                border-radius:12px;
                border:{border};
                background-color:{bg};
                margin-bottom:15px;
                text-align:center;
            ">

            <b>{row['Week Label']}</b>

            <hr>

            ⚖ Avg W1:
            <b>{row['Weight 1']:.2f}</b>

            <br><br>

            ⚖ Avg W2:
            <b>{row['Weight 2']:.2f}</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # FILTER SELECTED WEEK
    # =========================
    selected_week = st.session_state.selected_week

    selected_week_df = week_plot_df[
        week_plot_df['Week Period'].astype(str)
        == selected_week
    ]

    # =========================
    # DAILY BREAKDOWN
    # =========================
    daily = selected_week_df.groupby(
        selected_week_df['Timestamp'].dt.date
    )[
        ['Weight 1', 'Weight 2']
    ].mean().reset_index()

    # Rename column
    daily.columns = ['Date', 'Weight 1', 'Weight 2']

    # =========================
    # SELECTED WEEK LABEL
    # =========================
    selected_label = month_weeks[
        month_weeks['Week Period'].astype(str)
        == selected_week
    ]['Week Label'].values[0]

    st.markdown(f"## 📈 Trend for {selected_label}")

    # =========================
    # GRAPH
    # =========================
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        daily['Date'],
        daily['Weight 1'],
        marker='o',
        linewidth=2,
        label="Weight 1"
    )

    ax.plot(
        daily['Date'],
        daily['Weight 2'],
        marker='o',
        linewidth=2,
        label="Weight 2"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Weight")
    ax.legend()

    plt.xticks(rotation=45)

    st.pyplot(fig)
# =========================


# SLOT FUNCTION
# =========================
def get_slot(ts):
    h = ts.hour
    if 5 <= h < 9:
        return "5–9 AM"
    elif 9 <= h < 13:
        return "9–1 PM"
    elif 13 <= h < 16:
        return "1–4 PM"
    elif 16 <= h < 19:
        return "4–7 PM"
    return None

# =========================
# =========================
# =========================
# SLOT FUNCTION
# =========================
def get_slot(ts):

    h = ts.hour

    if 5 <= h < 9:
        return "5–9 AM"

    elif 9 <= h < 13:
        return "9–1 PM"

    elif 13 <= h < 16:
        return "1–4 PM"

    elif 16 <= h < 19:
        return "4–7 PM"

    return None


# =========================
# TREND FUNCTION
# =========================
def trend(previous_weight, current_weight):

    if current_weight > previous_weight:
        return "⬆ Increasing"

    elif current_weight < previous_weight:
        return "⬇ Decreasing"

    else:
        return "➡ Stable"


# =========================
# SLOT DATA
# =========================
temp_df = filtered.copy()

# Ensure datetime format
temp_df['Timestamp'] = pd.to_datetime(
    temp_df['Timestamp'],
    dayfirst=True
)

# Create Slot + Date
temp_df['Slot'] = temp_df['Timestamp'].apply(get_slot)
temp_df['Date'] = temp_df['Timestamp'].dt.date

# Remove empty slot rows
temp_df = temp_df.dropna(subset=['Slot'])

# Sort data
temp_df = temp_df.sort_values("Timestamp")

# Check empty
if temp_df.empty:
    st.warning("No slot data available")
    st.stop()


# =========================
# AVAILABLE DATES
# =========================
unique_dates = sorted(temp_df['Date'].unique())

min_date = min(unique_dates)
max_date = max(unique_dates)


# =========================
# CALENDAR DATE PICKER
# =========================
st.markdown("## 📅 Select Dates For Slot Analysis")

col1, col2 = st.columns(2)

date1 = col1.date_input(
    "📅 Select Previous Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

date2 = col2.date_input(
    "📅 Select Current Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# Convert to date
date1 = pd.to_datetime(date1).date()
date2 = pd.to_datetime(date2).date()


# =========================
# VALIDATION
# =========================
if date1 == date2:

    st.warning("⚠ Please select different dates")

elif date1 not in unique_dates:

    st.warning(f"⚠ No data available for {date1}")

elif date2 not in unique_dates:

    st.warning(f"⚠ No data available for {date2}")

else:

    # =========================
    # SLOT COMPARISON
    # =========================
    all_results = []

    slots = [
        "5–9 AM",
        "9–1 PM",
        "1–4 PM",
        "4–7 PM"
    ]

    for slot in slots:

        # Previous Day Data
        d1 = temp_df[
            (temp_df['Date'] == date1) &
            (temp_df['Slot'] == slot)
        ]

        # Current Day Data
        d2 = temp_df[
            (temp_df['Date'] == date2) &
            (temp_df['Slot'] == slot)
        ]

        # Skip missing slots
        if d1.empty or d2.empty:
            continue

        # -------------------------
        # Average Weights
        # -------------------------
        w1_d1 = round(d1['Weight 1'].mean(), 2)
        w1_d2 = round(d2['Weight 1'].mean(), 2)

        w2_d1 = round(d1['Weight 2'].mean(), 2)
        w2_d2 = round(d2['Weight 2'].mean(), 2)

        # -------------------------
        # Weight Changes
        # -------------------------
        w1_change = round(w1_d2 - w1_d1, 2)
        w2_change = round(w2_d2 - w2_d1, 2)

        # -------------------------
        # Store Results
        # -------------------------
        all_results.append([

            slot,

            w1_d1,
            w1_d2,
            w1_change,
            trend(w1_d1, w1_d2),

            w2_d1,
            w2_d2,
            w2_change,
            trend(w2_d1, w2_d2),

            len(d1),
            len(d2)
        ])


    # =========================
    # CREATE DATAFRAME
    # =========================
    all_df = pd.DataFrame(all_results, columns=[

        "Slot",

        "W1 Prev Day",
        "W1 Current Day",
        "W1 Change",
        "W1 Trend",

        "W2 Prev Day",
        "W2 Current Day",
        "W2 Change",
        "W2 Trend",

        "Records Prev",
        "Records Current"
    ])


    # =========================
    # DISPLAY TABLE
    # =========================
    st.markdown("## 📊 Slot Comparison Analysis")

    st.dataframe(
        all_df,
        width="stretch"
    )


    # =========================
    # SLOT TREND GRAPH
    # =========================
    st.markdown("## 📈 Slot Trend Graph")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        all_df['Slot'],
        all_df['W1 Prev Day'],
        marker='o',
        label=f"W1 {date1}"
    )

    ax.plot(
        all_df['Slot'],
        all_df['W1 Current Day'],
        marker='o',
        label=f"W1 {date2}"
    )

    ax.plot(
        all_df['Slot'],
        all_df['W2 Prev Day'],
        marker='o',
        linestyle='--',
        label=f"W2 {date1}"
    )

    ax.plot(
        all_df['Slot'],
        all_df['W2 Current Day'],
        marker='o',
        linestyle='--',
        label=f"W2 {date2}"
    )

    ax.set_xlabel("Time Slot")
    ax.set_ylabel("Weight")
    ax.legend()

    plt.xticks(rotation=15)

    st.pyplot(fig)