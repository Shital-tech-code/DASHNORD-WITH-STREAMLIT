import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go

# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="🐝 Hive Monitoring Dashboard",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Hive Dashboard",
    layout="wide"
)

# =====================================================
# MAIN HEADER
# =====================================================
st.markdown("""
<div style="
background:linear-gradient(135deg,#111827,#1f2937);
padding:25px;
border-radius:20px;
margin-bottom:20px;
">

<h1 style="
color:white;
text-align:center;
">
Smart Hive Monitoring System
</h1>

<p style="
color:#cbd5e1;
text-align:center;
font-size:18px;
">
Real-Time IoT Based Bee Hive  Dashboard
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background: #f8fafc;
    color:black;
}

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#111827;
    margin-bottom:5px;
}

.sub-title{
    text-align:center;
    color:#374151;
    margin-bottom:30px;
}

section[data-testid="stSidebar"]{
    background:#ffffff;
    border-right:1px solid #d1d5db;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:18px;
    padding:18px;
    border:1px solid #d1d5db;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
}

div[data-testid="metric-container"]:hover{
    transform:scale(1.02);
    transition:0.3s;
}

.stButton > button{
    background:#22c55e;
    color:white;
    border-radius:12px;
    border:none;
    height:45px;
    font-weight:bold;
}

.stDownloadButton > button{
    background:#2563eb;
    color:white;
    border-radius:12px;
    border:none;
}

</style>
""", unsafe_allow_html=True)

# LOGIN SYSTEM
# =====================================================

users = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },

    "user1": {
        "password": "user123",
        "role": "user1"
    }
}

# SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# =====================================================
# LOGIN PAGE
# =====================================================
def login():

    st.markdown("""
    <style>

    .login-box{
        background:white;
        padding:40px;
        border-radius:20px;
        box-shadow:0px 4px 20px rgba(0,0,0,0.1);
        margin-top:60px;
    }

    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1.2,1])

    with col2:

        st.markdown("""
        <div class="login-box">

        <h1 style='text-align:center;color:#111827;'>
        🐝 Hive Dashboard
        </h1>

        <p style='text-align:center;color:gray;'>
        Smart Beehive Monitoring System
        </p>

        </div>
        """, unsafe_allow_html=True)

        username = st.text_input(
            "👤 Username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if (
                username in users and
                users[username]["password"] == password
            ):

                st.session_state.logged_in = True

                st.session_state.role = users[username]["role"]

                st.session_state.username = username

                st.success("✅ Login Successful")

                st.rerun()

            else:

                st.error(
                    "❌ Invalid Username or Password"
                )

# =====================================================
# SHOW LOGIN
# =====================================================
if not st.session_state.logged_in:

    login()

    st.stop()

# =====================================================
# LOGOUT BUTTON
# =====================================================
if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.session_state.role = ""

    st.session_state.username = ""

    st.rerun()
# =====================================================
# AUTO REFRESH
# =====================================================
st_autorefresh(
    interval=1200000,
    key="refresh"
)

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("⚙ Dashboard Controls")

location = st.sidebar.selectbox(
    "📍 Choose Location",
    ["Pandharkaoda", "Wardha (MGIRI)"]
)

# =====================================================
# GOOGLE SHEET URL
# =====================================================
if location == "Pandharkaoda":

    url = "https://docs.google.com/spreadsheets/d/1gjlu4F-iNqhjrT57mpU7vGQOgXtjMer6i2Z3dDRbrFo/export?format=csv&gid=0"

else:

    url = "https://docs.google.com/spreadsheets/d/1gjlu4F-iNqhjrT57mpU7vGQOgXtjMer6i2Z3dDRbrFo/export?format=csv&gid=1479038266"

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data(ttl=60)

def load_data(url, location):

    if location == "Pandharkaoda":

        df = pd.read_csv(
            url,
            header=None,
            low_memory=False
        )

        df = df.dropna(axis=1, how='all')
        df = df.iloc[:,0:10]

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

        df = pd.read_csv(url)

        df.columns = df.columns.str.strip()

    df['Timestamp'] = pd.to_datetime(
    df['Timestamp'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)
    
    for col in [
    "Temperature",
    "Humidity",
    "Weight 1",
    "Weight 2",
    "Latitude",
    "Longitude"
]:

     df[col] = pd.to_numeric(
        df[col],
        errors='coerce'
    )

    df = df.dropna(
        subset=[
            'Timestamp',
            'Weight 1',
            'Weight 2'
        ]
    )

    return df.sort_values('Timestamp')

# =====================================================
# LOAD DATA
# =====================================================
df = load_data(url, location)

if df.empty:
    st.error("❌ No Data Loaded")
    st.stop()

# =====================================================
# HEADER
# =====================================================
st.markdown(
    '<div class="main-title">🐝 Hive Monitoring Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="sub-title">📍 Smart Beehive Monitoring System | {location}</div>',
    unsafe_allow_html=True
)

# =====================================================
# LIVE DATA
# =====================================================
latest = df.iloc[-1]

w1 = float(latest['Weight 1'])
w2 = float(latest['Weight 2'])

total = w1 + w2

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "🌡 Temperature",
    f"{latest['Temperature']:.1f} °C"
)

c2.metric(
    "💧 Humidity",
    f"{latest['Humidity']:.1f} %"
)

c3.metric(
    "⚖ Weight 1",
    f"{w1:.2f} kg"
)

c4.metric(
    "🍯 Weight 2",
    f"{w2:.2f} kg"
)

c5.metric(
    "🐝 Total Weight",
    f"{total:.2f} kg"
)

# =====================================================
# HIVE STATUS
# =====================================================
if total > 5:
    st.success("✅ Hive Status : Healthy & Active")

elif total > 1:
    st.warning("⚠ Hive Status : Moderate Activity")

else:
    st.error("❌ Hive Status : Low Activity")

st.info(f"🕒 Last Sensor Update : {latest['Timestamp']}")
# =====================================================
# DOWNLOAD BUTTON
# =====================================================
csv = df.to_csv(index=False).encode('utf-8')

if st.session_state.role == "admin":

    st.download_button(
        "⬇ Download CSV Data",
        csv,
        "hive_data.csv",
        "text/csv"
    )

# =====================================================
# DATE FILTER
# =====================================================
st.sidebar.header("📅 Date Filter")

start_date = st.sidebar.date_input(
    "Start Date",
    df['Timestamp'].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df['Timestamp'].max().date()
)

filtered = df[
    (df['Timestamp'].dt.date >= start_date) &
    (df['Timestamp'].dt.date <= end_date)
].copy()
## =====================================================
# TABS BASED ON ROLE
# =====================================================

if st.session_state.role == "admin":

    tab1, tab2, tab3 = st.tabs([
        "📊 Live Dashboard",
        "📈 Trends",
        "📅 Weekly Analytics"
    ])

else:

    tab1, tab2 = st.tabs([
        "📊 Live Dashboard",
        "📈 Trends"
    ])

with tab1:

    from datetime import datetime, time

    st.subheader("📈 Real Time Hive Weight Monitoring")

    now = datetime.now()
    today = now.date()
    start_time = time(5, 0)

    realtime_df = filtered[
        (filtered['Timestamp'].dt.date == today) &
        (filtered['Timestamp'].dt.time >= start_time) &
        (filtered['Timestamp'].dt.time <= now.time())
    ]

    # =========================
    # EMPTY CHECK (FIXED)
    # =========================
    if realtime_df.empty:

        st.error("🔴 MGIRI Hive Device Offline")

        if not filtered.empty:
            last_record = filtered.iloc[-1]

            st.info(f"🕒 Last Update: {last_record['Timestamp']}")

            st.metric(
                "🐝 Last Weight",
                f"{last_record['Weight 2']:.2f} kg"
            )

        st.warning("📡 Waiting for internet connection...")
        st.stop()   # ⭐ IMPORTANT FIX

    # =========================
    # SAFE DATA ACCESS
    # =========================
    plot_df = realtime_df

    latest_w1 = realtime_df['Weight 1'].iloc[-1]
    latest_w2 = realtime_df['Weight 2'].iloc[-1]
    start_weight = realtime_df['Weight 2'].iloc[0]

    change = latest_w2 - start_weight

    # =========================
    # METRICS
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.metric("🐝 Current Weight 1", f"{latest_w1:.2f} kg")
    col2.metric("🍯 Current Weight 2", f"{latest_w2:.2f} kg")
    col3.metric("📈 Daily Change", f"{change:.2f} kg")

    # =========================
    # STATUS (SAFE NOW)
    # =========================
    status1, status2, status3 = st.columns(3)

    status1.success("🟢 Device Online")

    status2.info(
        f"🕒 Updated: {realtime_df['Timestamp'].iloc[-1].strftime('%I:%M %p')}"
    )

    status3.warning("📡 Live Monitoring Active")

# =========================
# LIVE INFO BOX
# =========================
st.markdown("""
    <div style="
    background:linear-gradient(135deg,#2563eb,#1d4ed8);
    padding:15px;
    border-radius:15px;
    color:white;
    font-size:18px;
    font-weight:600;
    margin-bottom:20px;
    ">
    📡 Real-Time Hive Monitoring Dashboard
    </div>
    """, unsafe_allow_html=True)

# =========================
# MODERN SPLINE AREA GRAPH
# =========================
fig = go.Figure()

# WEIGHT 1
fig.add_trace(go.Scatter(
    x=plot_df['Timestamp'],
    y=plot_df['Weight 1'],
    mode='lines',
    name='Weight 1',

    line=dict(
        color='#00FFB3',
        width=5,
        shape='spline'
    ),

    fill='tozeroy',

    fillcolor='rgba(0,255,179,0.25)'
))

# WEIGHT 2
fig.add_trace(go.Scatter(
    x=plot_df['Timestamp'],
    y=plot_df['Weight 2'],
    mode='lines',
    name='Weight 2',

    line=dict(
        color='#FF6B3D',
        width=5,
        shape='spline'
    ),

    fill='tozeroy',

    fillcolor='rgba(255,107,61,0.25)'
))

# =========================
# GRAPH DESIGN
# =========================
fig.update_layout(

    title={
        'text': "📈 Real-Time Hive Weight Analysis",
        'x': 0.5,
        'xanchor': 'center',

        'font': dict(
            size=24,
            color='white'
        )
    },

    template="plotly_dark",

    height=520,

    hovermode='x unified',

    paper_bgcolor='#0f172a',

    plot_bgcolor='#0f172a',

    font=dict(
        color='white',
        size=16
    ),

    margin=dict(
        l=20,
        r=20,
        t=70,
        b=20
    ),

    legend=dict(
        orientation="h",

        yanchor="bottom",
        y=1.02,

        xanchor="right",
        x=1,

        font=dict(
            size=15,
            color='white'
        ),

        bgcolor='rgba(0,0,0,0)'
    ),

    xaxis=dict(

        title="Time",

        showgrid=False,

        title_font=dict(
            size=18,
            color='white'
        ),

        tickfont=dict(
            size=13,
            color='white'
        )
    ),

    yaxis=dict(

        title="Weight (kg)",

        gridcolor='rgba(255,255,255,0.1)',

        title_font=dict(
            size=18,
            color='white'
        ),

        tickfont=dict(
            size=13,
            color='white'
        )
    )
)

# =========================
# AUTO ZOOM
# =========================
fig.update_yaxes(
    autorange=True,
    fixedrange=False
)

# =========================
# SHOW GRAPH
# =========================
st.plotly_chart(
    fig,
    width='stretch'
)
        # =========================
# WEIGHT SUMMARY
# =========================
st.markdown("### 📊 Weight Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "📉 Minimum",
    f"{realtime_df['Weight 2'].min():.2f} kg"
)

c2.metric(
    "📈 Maximum",
    f"{realtime_df['Weight 2'].max():.2f} kg"
)

c3.metric(
    "📊 Average",
    f"{realtime_df['Weight 2'].mean():.2f} kg"
)

# =========================
# SMART ALERTS
# =========================
st.markdown("### 🚨 Smart Alerts")

if latest['Temperature'] > 40:

    st.error("🔥 High Temperature Detected")

if change < -1:

    st.warning("⚠ Possible Swarming Activity")

elif change > 1:

    st.success("🍯 Strong Honey Collection Activity")

else:

    st.info("✅ Hive Weight Stable")
            
# =========================
        
# =====================================================
# # =====================================================
# =====================================================
# TAB 2 : TREND DASHBOARD
# =====================================================
with tab2:

    st.subheader("📊 Trend Dashboard")

    time_mode = st.radio(
        "Select View",
        ["Day", "Week", "Month"],
        horizontal=True
    )

    plot_df = filtered.copy()

    # =================================================
    # DAY VIEW
    # =================================================
    if time_mode == "Day":

        st.markdown("### 📈 Daily Weight Trend")

        fig = go.Figure()

        # WEIGHT 1
        fig.add_trace(go.Scatter(
            x=plot_df['Timestamp'],
            y=plot_df['Weight 1'],
            mode='lines',
            name='🐝 Weight 1',

            line=dict(
                color='#00FFB3',
                width=6,
                shape='spline'
            ),

            fill='tozeroy',

            fillcolor='rgba(0,255,179,0.30)'
        ))

        # WEIGHT 2
        fig.add_trace(go.Scatter(
            x=plot_df['Timestamp'],
            y=plot_df['Weight 2'],
            mode='lines',
            name='🍯 Weight 2',

            line=dict(
                color='#FF8C42',
                width=6,
                shape='spline'
            ),

            fill='tozeroy',

            fillcolor='rgba(255,140,66,0.30)'
        ))

        fig.update_layout(

            template="plotly_dark",

            height=520,

            hovermode='x unified',

            paper_bgcolor='#0f172a',

            plot_bgcolor='#0f172a',

            title={
                'text': "📈 Daily Hive Trend",
                'x': 0.5,
                'font': dict(
                    size=24,
                    color='white'
                )
            },

            font=dict(
                color='white',
                size=16
            ),

            legend=dict(
                orientation="h",

                yanchor="bottom",
                y=1.02,

                xanchor="center",
                x=0.5,

                font=dict(
                    size=18,
                    color='white'
                ),

                bgcolor='rgba(0,0,0,0)'
            ),

            xaxis=dict(

                title="Time",

                showgrid=False,

                title_font=dict(
                    size=20,
                    color='white'
                ),

                tickfont=dict(
                    size=15,
                    color='white'
                )
            ),

            yaxis=dict(

                title="Weight (kg)",

                gridcolor='rgba(255,255,255,0.1)',

                title_font=dict(
                    size=20,
                    color='white'
                ),

                tickfont=dict(
                    size=15,
                    color='white'
                )
            )
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    # =================================================
    # WEEK VIEW
    # =================================================
    elif time_mode == "Week":

        week_df = plot_df.copy()

        week_df['Week'] = week_df['Timestamp'].dt.to_period('W')

        weekly = week_df.groupby('Week')[['Weight 1', 'Weight 2']].mean()

        weekly = weekly.reset_index()

        st.markdown("### 📅 Weekly Analytics")

        # WEEKLY CARDS
        cols = st.columns(3)

        for i, row in weekly.iterrows():

            col = cols[i % 3]

            with col:

                st.markdown(f"""
                <div style="
                background:#111827;
                padding:18px;
                border-radius:18px;
                margin-bottom:15px;
                border:1px solid #374151;
                ">
                <h4 style="color:white;">
                📆 {row['Week']}
                </h4>

                <p style="color:#34d399;">
                ⚖ Weight 1 Avg :
                {row['Weight 1']:.2f} kg
                </p>

                <p style="color:#fb923c;">
                🍯 Weight 2 Avg :
                {row['Weight 2']:.2f} kg
                </p>
                </div>
                """, unsafe_allow_html=True)

        # WEEKLY GRAPH
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=weekly['Week'].astype(str),
            y=weekly['Weight 1'],
            mode='lines+markers',
            name='🐝 Weight 1',

            line=dict(
                color='#00FFB3',
                width=5
            ),

            marker=dict(
                size=10
            )
        ))

        fig.add_trace(go.Scatter(
            x=weekly['Week'].astype(str),
            y=weekly['Weight 2'],
            mode='lines+markers',
            name='🍯 Weight 2',

            line=dict(
                color='#FF8C42',
                width=5
            ),

            marker=dict(
                size=10
            )
        ))

        fig.update_layout(

            template="plotly_dark",

            height=520,

            paper_bgcolor='#0f172a',

            plot_bgcolor='#0f172a',

            title={
                'text': "📊 Weekly Hive Analysis",
                'x': 0.5,
                'font': dict(
                    size=24,
                    color='white'
                )
            },

            font=dict(
                color='white',
                size=16
            ),

            legend=dict(
                font=dict(
                    size=18
                )
            ),

            xaxis_title="Week",

            yaxis_title="Average Weight (kg)"
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    # =================================================
    # MONTH VIEW
    # =================================================
    elif time_mode == "Month":

        month_df = plot_df.copy()

        month_df['Month'] = month_df['Timestamp'].dt.to_period('M')

        monthly = month_df.groupby('Month')[['Weight 1', 'Weight 2']].mean()

        monthly = monthly.reset_index()

        st.markdown("### 📅 Monthly Analytics")

        fig = go.Figure()

        # BAR GRAPH
        fig.add_trace(go.Bar(
            x=monthly['Month'].astype(str),
            y=monthly['Weight 1'],
            name='🐝 Weight 1',
            marker_color='#00FFB3'
        ))

        # LINE GRAPH
        fig.add_trace(go.Scatter(
            x=monthly['Month'].astype(str),
            y=monthly['Weight 2'],
            mode='lines+markers',
            name='🍯 Weight 2',

            line=dict(
                color='#FF8C42',
                width=5
            ),

            marker=dict(
                size=10
            )
        ))

        fig.update_layout(

            template="plotly_dark",

            barmode='group',

            height=520,

            paper_bgcolor='#0f172a',

            plot_bgcolor='#0f172a',

            title={
                'text': "📈 Monthly Hive Performance",
                'x': 0.5,
                'font': dict(
                    size=24,
                    color='white'
                )
            },

            font=dict(
                color='white',
                size=16
            ),

            legend=dict(
                font=dict(
                    size=18
                )
            ),

            xaxis_title="Month",

            yaxis_title="Average Weight (kg)"
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

# TAB 3
# =====================================================

if st.session_state.role == "admin":

    with tab3:

        st.subheader("📅 Smart Slot Analysis")

        # =================================================
        # SLOT FUNCTION
        # =================================================
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

    # =================================================
    # TREND FUNCTION
    # =================================================
    def trend(previous_weight, current_weight):

        if current_weight > previous_weight:
            return "🟢 Increasing"

        elif current_weight < previous_weight:
            return "🔴 Decreasing"

        else:
            return "🟡 Stable"


    # =================================================
    # SLOT DATA
    # =================================================
    temp_df = filtered.copy()

    temp_df['Timestamp'] = pd.to_datetime(
        temp_df['Timestamp'],
        dayfirst=True,
        errors='coerce'
    )

    temp_df['Slot'] = temp_df['Timestamp'].apply(get_slot)

    temp_df['Date'] = temp_df['Timestamp'].dt.date

    temp_df = temp_df.dropna(subset=['Slot'])

    temp_df = temp_df.sort_values("Timestamp")


    # =================================================
    # EMPTY CHECK
    # =================================================
    if temp_df.empty:

        st.warning("⚠ No slot data available")

    else:

        # =================================================
        # AVAILABLE DATES
        # =================================================
        unique_dates = sorted(temp_df['Date'].unique())

        min_date = min(unique_dates)

        max_date = max(unique_dates)


        # =================================================
        # DATE PICKERS
        # =================================================
        col1, col2 = st.columns(2)

        with col1:

            date1 = st.date_input(
                "📅 Previous Date",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="slot_date1"
            )

        with col2:

            date2 = st.date_input(
                "📅 Current Date",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                key="slot_date2"
            )


        # =================================================
        # CONVERT TO DATE
        # =================================================
        date1 = pd.to_datetime(date1).date()

        date2 = pd.to_datetime(date2).date()


        # =================================================
        # VALIDATION
        # =================================================
        if date1 == date2:

            st.warning("⚠ Please select different dates")

        else:

            # =================================================
            # SLOT ANALYSIS
            # =================================================
            all_results = []

            slots = [
                "5–9 AM",
                "9–1 PM",
                "1–4 PM",
                "4–7 PM"
            ]

            for slot in slots:

                d1 = temp_df[
                    (temp_df['Date'] == date1) &
                    (temp_df['Slot'] == slot)
                ]

                d2 = temp_df[
                    (temp_df['Date'] == date2) &
                    (temp_df['Slot'] == slot)
                ]

                if d1.empty or d2.empty:
                    continue


                # =================================================
                # AVERAGES
                # =================================================
                w1_d1 = round(d1['Weight 1'].mean(), 2)
                w1_d2 = round(d2['Weight 1'].mean(), 2)

                w2_d1 = round(d1['Weight 2'].mean(), 2)
                w2_d2 = round(d2['Weight 2'].mean(), 2)


                # =================================================
                # CHANGES
                # =================================================
                w1_change = round(w1_d2 - w1_d1, 2)

                w2_change = round(w2_d2 - w2_d1, 2)


                # =================================================
                # SAVE RESULTS
                # =================================================
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


            # =================================================
            # DATAFRAME
            # =================================================
            all_df = pd.DataFrame(all_results, columns=[

                "Slot",

                "W1 Prev",
                "W1 Current",
                "W1 Change",
                "W1 Trend",

                "W2 Prev",
                "W2 Current",
                "W2 Change",
                "W2 Trend",

                "Records Prev",
                "Records Current"
            ])


            # =================================================
            # EMPTY RESULT CHECK
            # =================================================
            if all_df.empty:

                st.warning("⚠ No slot comparison data available")

            else:

                # =================================================
                # SLOT SUMMARY CARDS
                # =================================================
                st.markdown("### 🐝 Slot Health Cards")

                cols = st.columns(len(all_df))

                for i, row in all_df.iterrows():

                    with cols[i]:

                        st.markdown(f"""
                        <div style="
                            background:linear-gradient(135deg,#1e293b,#0f172a);
                            padding:18px;
                            border-radius:18px;
                            text-align:center;
                            border:1px solid #334155;
                            box-shadow:0px 0px 15px rgba(0,255,255,0.15);
                            margin-bottom:10px;
                        ">

                        <h4 style="color:#38bdf8;">
                        {row['Slot']}
                        </h4>

                        <p style="color:white;font-size:18px;">
                        ⚖ W1 : {row['W1 Current']}
                        </p>

                        <p style="color:white;font-size:18px;">
                        🍯 W2 : {row['W2 Current']}
                        </p>

                        <p style="color:#22c55e;font-size:16px;">
                        {row['W1 Trend']}
                        </p>

                        </div>
                        """, unsafe_allow_html=True)


                # =================================================
                # DATA TABLE
                # =================================================
                st.markdown("### 📊 Slot Comparison Table")

                st.dataframe(
                    all_df,
                    use_container_width=True
                )


                # =================================================
                # SLOT TREND GRAPH
                # =================================================
                st.markdown("### 📈 Slot Trend Graph")

                fig, ax = plt.subplots(figsize=(12,5))

                ax.plot(
                    all_df['Slot'],
                    all_df['W1 Prev'],
                    marker='o',
                    linewidth=3,
                    color='cyan',
                    label=f"W1 {date1}"
                )

                ax.plot(
                    all_df['Slot'],
                    all_df['W1 Current'],
                    marker='o',
                    linewidth=3,
                    color='lime',
                    label=f"W1 {date2}"
                )

                ax.plot(
                    all_df['Slot'],
                    all_df['W2 Prev'],
                    marker='o',
                    linewidth=3,
                    linestyle='--',
                    color='orange',
                    label=f"W2 {date1}"
                )

                ax.plot(
                    all_df['Slot'],
                    all_df['W2 Current'],
                    marker='o',
                    linewidth=3,
                    linestyle='--',
                    color='red',
                    label=f"W2 {date2}"
                )

                ax.set_facecolor("#0f172a")

                fig.patch.set_facecolor("#0f172a")

                ax.tick_params(colors='white')

                ax.spines['bottom'].set_color('white')

                ax.spines['left'].set_color('white')

                ax.set_xlabel(
                    "Time Slot",
                    color='white'
                )

                ax.set_ylabel(
                    "Weight",
                    color='white'
                )

                ax.legend()

                ax.grid(alpha=0.3)

                st.pyplot(fig)


                # =================================================
                # DOWNLOAD BUTTON
                # =================================================
                slot_csv = all_df.to_csv(index=False).encode('utf-8')

                st.download_button(
                    "⬇ Download Slot Analysis CSV",
                    slot_csv,
                    "slot_analysis.csv",
                    "text/csv"
                )