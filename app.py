
import sqlite3
import html
from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# RELIEFGRID — FLOOD RESPONSE AND RELIEF COORDINATION PROTOTYPE
# =========================================================

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "floodrelief.db"

st.set_page_config(
    page_title="ReliefGrid | Flood Response",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------- THEME ----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #f4f7fc;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1735 0%, #132b52 100%);
}
[data-testid="stSidebar"] * {
    color: #edf4ff !important;
}
.hero {
    background: linear-gradient(115deg, #102b55, #1769aa);
    padding: 30px;
    border-radius: 22px;
    color: white;
    margin-bottom: 22px;
}
.hero h1 {
    color: white;
    font-size: 34px;
    margin: 0 0 8px 0;
    font-weight: 800;
}
.hero p {
    color: #d8e8ff;
    margin: 0;
    font-size: 15px;
}
.metric-card {
    background: white;
    border: 1px solid #e4eaf4;
    padding: 20px;
    border-radius: 16px;
    min-height: 125px;
    box-shadow: 0 5px 20px rgba(18, 43, 83, .04);
}
.metric-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
}
.metric-value {
    color: #102b55;
    font-size: 30px;
    font-weight: 800;
    margin-top: 9px;
}
.metric-note {
    color: #718198;
    font-size: 12px;
    margin-top: 4px;
}
.section-title {
    color: #102b55;
    font-size: 22px;
    font-weight: 800;
    margin: 12px 0 5px;
}
.section-subtitle {
    color: #718198;
    font-size: 13px;
    margin-bottom: 14px;
}
.priority-card {
    background: white;
    border: 1px solid #e4eaf4;
    border-radius: 14px;
    padding: 15px;
    margin: 8px 0;
}
.pill {
    display: inline-block;
    padding: 4px 9px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
}
.critical { background: #fee2e2; color: #b91c1c; }
.high { background: #ffedd5; color: #c2410c; }
.medium { background: #fef3c7; color: #92400e; }
.low { background: #dbeafe; color: #1d4ed8; }
.small-muted {
    color: #718198;
    font-size: 12px;
}
.stButton > button[kind="primary"] {
    background: #1769aa;
    border-color: #1769aa;
    border-radius: 10px;
}
div[data-testid="stForm"] {
    background: white;
    padding: 20px;
    border: 1px solid #e4eaf4;
    border-radius: 16px;
}

.stApp { color: #18243a; }
.block-container { padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1500px; }
.stButton > button, .stDownloadButton > button { border-radius: 10px; font-weight: 700; min-height: 2.7rem; }
.stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] { border-radius: 10px; }
div[data-testid="stMetric"] { background: white; border: 1px solid #e4eaf4; padding: 14px 16px; border-radius: 14px; }
div[data-testid="stMetric"] label { color: #64748b; }
@media (max-width: 768px) {
  .hero { padding: 22px; }
  .hero h1 { font-size: 27px; }
  .block-container { padding-left: 1rem; padding-right: 1rem; }
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ----------------------- DATABASE ------------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                location TEXT NOT NULL,
                lat REAL,
                lon REAL,
                people INTEGER NOT NULL DEFAULT 1,
                need TEXT NOT NULL,
                severity TEXT NOT NULL,
                notes TEXT,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                quantity TEXT NOT NULL,
                location TEXT NOT NULL,
                lat REAL,
                lon REAL
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM incidents"
        ).fetchone()[0]

        if count == 0:
            demo_incidents = [
                (
                    "Demo: Ananya Das", "9000000001", "Dibrugarh",
                    27.4728, 94.9120, 8, "Rescue", "Critical",
                    "Demo record — verify before taking action.",
                    "Pending", datetime.now().isoformat(timespec="seconds")
                ),
                (
                    "Demo: Rohan Bora", "9000000002", "Jorhat",
                    26.7509, 94.2037, 5, "Medical help", "High",
                    "Demo medical assistance request.",
                    "Assigned", datetime.now().isoformat(timespec="seconds")
                ),
                (
                    "Demo: Mira Saikia", "9000000003", "Majuli",
                    26.9500, 94.1700, 12, "Drinking water", "High",
                    "Demo drinking water request.",
                    "Pending", datetime.now().isoformat(timespec="seconds")
                ),
                (
                    "Demo: Arup Nath", "9000000004", "Guwahati",
                    26.1445, 91.7362, 4, "Food", "Medium",
                    "Demo food assistance request.",
                    "Pending", datetime.now().isoformat(timespec="seconds")
                ),
                (
                    "Demo: Purnima Das", "9000000005", "Tezpur",
                    26.6528, 92.7926, 3, "Shelter", "Low",
                    "Demo shelter request.",
                    "Resolved", datetime.now().isoformat(timespec="seconds")
                ),
            ]

            conn.executemany("""
                INSERT INTO incidents
                (name, phone, location, lat, lon, people, need,
                 severity, notes, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, demo_incidents)

        resource_count = conn.execute(
            "SELECT COUNT(*) FROM resources"
        ).fetchone()[0]

        if resource_count == 0:
            demo_resources = [
                ("Demo Relief Camp", "Shelter", "120 beds",
                 "Dibrugarh", 27.4728, 94.9120),
                ("Demo Water Supply", "Drinking water", "500 bottles",
                 "Jorhat", 26.7509, 94.2037),
                ("Demo Medical Unit", "Medical help", "3 teams",
                 "Guwahati", 26.1445, 91.7362),
                ("Demo Food Store", "Food", "250 meal packs",
                 "Tezpur", 26.6528, 92.7926),
                ("Demo Rescue Unit", "Rescue", "2 boats",
                 "Majuli", 26.9500, 94.1700),
            ]

            conn.executemany("""
                INSERT INTO resources
                (name, type, quantity, location, lat, lon)
                VALUES (?, ?, ?, ?, ?, ?)
            """, demo_resources)


def fetch_table(table):
    if table not in ("incidents", "resources"):
        raise ValueError("Invalid table")

    with get_connection() as conn:
        return pd.read_sql_query(
            f"SELECT * FROM {table} ORDER BY id DESC", conn
        )


initialize_database()


# ----------------------- HELPERS -------------------------

SEVERITY_SCORE = {
    "Critical": 100,
    "High": 70,
    "Medium": 40,
    "Low": 15,
}


def priority_score(row):
    score = SEVERITY_SCORE.get(row["severity"], 15)
    score += min(max(int(row["people"]), 0), 100)

    if row["need"] in ("Rescue", "Medical help"):
        score += 20

    return score


def priority_label(row):
    # The user-selected severity is preserved as the displayed level.
    return row["severity"]


def severity_html(severity):
    safe = severity if severity in SEVERITY_SCORE else "Low"
    css_class = safe.lower()
    return f'<span class="pill {css_class}">{safe}</span>'


def add_incident(data):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO incidents
            (name, phone, location, lat, lon, people, need,
             severity, notes, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
        """, (
            data["name"],
            data["phone"],
            data["location"],
            data["lat"],
            data["lon"],
            data["people"],
            data["need"],
            data["severity"],
            data["notes"],
            datetime.now().isoformat(timespec="seconds"),
        ))


def update_status(incident_id, status):
    if status not in ("Pending", "Assigned", "Resolved"):
        raise ValueError("Invalid incident status")

    with get_connection() as conn:
        conn.execute(
            "UPDATE incidents SET status = ? WHERE id = ?",
            (status, incident_id),
        )


# ----------------------- SIDEBAR -------------------------

with st.sidebar:
    st.markdown("# 🌊 ReliefGrid")
    st.markdown("### FLOOD RESPONSE NETWORK")
    st.caption("Emergency coordination platform")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Report an Emergency",
            "Manage Incidents",
            "Relief Resources",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.markdown("**Prototype status**")
    st.markdown("🟢 Local database connected")
    st.caption("Demo mode · Not connected to emergency services")
    st.divider()
    st.caption("ReliefGrid · Hackathon prototype")
    st.caption("Tip: use the navigation above to report, track and coordinate requests.")
    if st.button("↻ Refresh dashboard", use_container_width=True):
        st.rerun()


# ----------------------- DATA -----------------------------

incidents_df = fetch_table("incidents")
resources_df = fetch_table("resources")

if not incidents_df.empty:
    incidents_df["priority_score"] = incidents_df.apply(
        priority_score, axis=1
    )

open_df = incidents_df[
    incidents_df["status"] != "Resolved"
].copy()

critical_df = open_df[
    open_df["severity"].isin(["Critical", "High"])
]

people_affected = (
    int(open_df["people"].sum()) if not open_df.empty else 0
)


# ----------------------- HEADER ---------------------------

st.markdown("""
<div class="hero">
    <h1>ReliefGrid 🌊</h1>
    <p>Emergency coordination · Incident management · Relief resources</p>
</div>
""", unsafe_allow_html=True)

st.warning(
    "DEMO MODE: All preloaded incidents and resources are fictional. "
    "Locations, supplies and routes are not verified. "
    "Do not use this prototype as a live emergency dispatch system."
)


# ----------------------- OVERVIEW ------------------------

if page == "Overview":
    st.markdown(
        '<div class="section-title">Situation Overview</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        'A snapshot of reports recorded in this prototype.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "OPEN INCIDENTS", len(open_df), "Not yet resolved"),
        (c2, "HIGH PRIORITY", len(critical_df), "Critical + high severity"),
        (c3, "PEOPLE AFFECTED", people_affected, "Across open reports"),
        (c4, "RESOURCE TYPES", len(resources_df), "Listed resource entries"),
    ]

    for column, label, value, note in metrics:
        with column:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value:,}</div>
                <div class="metric-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([1.7, 1])

    with left:
        st.markdown(
            '<div class="section-title">Incident Map</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Markers show stored demo coordinates, not confirmed flood zones."
        )

        map_df = incidents_df.dropna(subset=["lat", "lon"]).copy()

        if not map_df.empty:
            map_df["Priority"] = map_df["severity"]
            map_df["People"] = map_df["people"].astype(str)
            map_df["Incident"] = map_df["name"]
            map_df["Need"] = map_df["need"]
            map_df["Status"] = map_df["status"]

            fig = px.scatter_map(
                map_df,
                lat="lat",
                lon="lon",
                color="Priority",
                size="people",
                hover_name="Incident",
                hover_data=["Need", "People", "Status", "location"],
                color_discrete_map={
                    "Critical": "#dc2626",
                    "High": "#ea580c",
                    "Medium": "#d97706",
                    "Low": "#2563eb",
                },
                zoom=6,
                center={"lat": 26.6, "lon": 93.0},
                map_style="open-street-map",
                height=450,
            )
            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                legend_title_text="Severity",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No incidents with valid coordinates.")

    with right:
        st.markdown(
            '<div class="section-title">Priority Queue</div>',
            unsafe_allow_html=True,
        )
        st.caption("Open reports, ordered by priority score.")

        if open_df.empty:
            st.success("No open incidents recorded.")
        else:
            queue = open_df.sort_values(
                "priority_score", ascending=False
            ).head(6)

            for _, row in queue.iterrows():
                st.markdown(f"""
                <div class="priority-card">
                    <div style="display:flex;justify-content:space-between;
                                gap:8px;align-items:center">
                        <strong>{html.escape(str(row["name"]))}</strong>
                        {severity_html(row["severity"])}
                    </div>
                    <div style="color:#718198;font-size:13px;margin-top:8px">
                        📍 {html.escape(str(row["location"]))}
                    </div>
                    <div style="font-size:13px;margin-top:7px">
                        <b>{html.escape(str(row["need"]))}</b> · {int(row["people"])} people
                    </div>
                    <div class="small-muted" style="margin-top:6px">
                        Priority score: {row["priority_score"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.write("")
    st.markdown(
        '<div class="section-title">Recent Incident Reports</div>',
        unsafe_allow_html=True,
    )

    if incidents_df.empty:
        st.info("No reports yet.")
    else:
        recent = incidents_df.sort_values(
            "id", ascending=False
        ).head(8)

        display = recent[
            ["id", "name", "location", "need", "severity",
             "people", "status"]
        ].rename(columns={
            "id": "ID",
            "name": "Reporter",
            "location": "Location",
            "need": "Requested Help",
            "severity": "Severity",
            "people": "People",
            "status": "Status",
        })

        st.dataframe(display, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Export recent reports (CSV)",
            data=display.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"reliefgrid_recent_reports_{datetime.now():%Y%m%d_%H%M}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.write("")
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.markdown('<div class="section-title">Reports by severity</div>', unsafe_allow_html=True)
        if incidents_df.empty:
            st.info("Severity analytics will appear after reports are recorded.")
        else:
            severity_counts = (incidents_df["severity"].value_counts()
                               .reindex(["Critical", "High", "Medium", "Low"], fill_value=0)
                               .rename_axis("Severity").reset_index(name="Reports"))
            chart = px.bar(severity_counts, x="Severity", y="Reports", color="Severity",
                           color_discrete_map={"Critical":"#dc2626","High":"#ea580c",
                                               "Medium":"#d97706","Low":"#2563eb"})
            chart.update_layout(margin=dict(l=0,r=0,t=15,b=0), showlegend=False,
                                plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(chart, use_container_width=True)
    with chart_right:
        st.markdown('<div class="section-title">Workflow status</div>', unsafe_allow_html=True)
        if incidents_df.empty:
            st.info("Status analytics will appear after reports are recorded.")
        else:
            status_counts = (incidents_df["status"].value_counts()
                             .reindex(["Pending", "Assigned", "Resolved"], fill_value=0)
                             .rename_axis("Status").reset_index(name="Reports"))
            chart = px.pie(status_counts, names="Status", values="Reports", hole=0.58,
                           color="Status", color_discrete_map={"Pending":"#ea580c",
                           "Assigned":"#2563eb","Resolved":"#16a34a"})
            chart.update_layout(margin=dict(l=0,r=0,t=15,b=0), paper_bgcolor="white")
            st.plotly_chart(chart, use_container_width=True)


# ----------------------- REPORT SOS -----------------------

elif page == "Report an Emergency":
    st.markdown(
        '<div class="section-title">Submit an SOS Report</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        'Record a request for assistance. Reports are saved locally.</div>',
        unsafe_allow_html=True,
    )

    with st.form("sos_form", clear_on_submit=True):
        st.subheader("Reporter Information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Reporter name *", placeholder="Enter full name"
            )
            phone = st.text_input(
                "Phone number", placeholder="Contact number"
            )

        with col2:
            location = st.text_input(
                "Village / town / location *",
                placeholder="e.g. Jorhat",
            )
            people = st.number_input(
                "People affected *",
                min_value=1,
                max_value=10000,
                value=1,
                step=1,
            )

        st.subheader("Emergency Details")

        col3, col4 = st.columns(2)

        with col3:
            need = st.selectbox(
                "Assistance required",
                [
                    "Rescue",
                    "Medical help",
                    "Drinking water",
                    "Food",
                    "Shelter",
                    "Other",
                ],
            )

        with col4:
            severity = st.selectbox(
                "Severity",
                ["Critical", "High", "Medium", "Low"],
            )

        st.subheader("Optional Map Coordinates")
        st.caption(
            "Use verified coordinates if available. "
            "Leave blank if the location is not known accurately."
        )

        col5, col6 = st.columns(2)

        with col5:
            lat_text = st.text_input(
                "Latitude", placeholder="e.g. 26.7509"
            )

        with col6:
            lon_text = st.text_input(
                "Longitude", placeholder="e.g. 94.2037"
            )

        notes = st.text_area(
            "Additional details",
            placeholder="Describe the situation and assistance needed.",
            max_chars=1000,
        )

        submitted = st.form_submit_button(
            "🚨 Submit SOS Report",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not name.strip() or not location.strip():
                st.error("Please enter the reporter's name and location.")
            elif phone.strip() and not phone.strip().replace("+", "").replace("-", "").replace(" ", "").isdigit():
                st.error("Please enter a valid phone number or leave the field blank.")
            else:
                try:
                    lat = float(lat_text) if lat_text.strip() else None
                    lon = float(lon_text) if lon_text.strip() else None

                    if lat is not None and not -90 <= lat <= 90:
                        raise ValueError("Latitude must be between -90 and 90.")

                    if lon is not None and not -180 <= lon <= 180:
                        raise ValueError("Longitude must be between -180 and 180.")

                    if (lat is None) != (lon is None):
                        raise ValueError(
                            "Enter both latitude and longitude, or leave both blank."
                        )

                    add_incident({
                        "name": name.strip(),
                        "phone": phone.strip(),
                        "location": location.strip(),
                        "lat": lat,
                        "lon": lon,
                        "people": int(people),
                        "need": need,
                        "severity": severity,
                        "notes": notes.strip(),
                    })

                    st.success(
                        "SOS report saved successfully. "
                        "It is stored locally and has not been sent "
                        "to emergency services."
                    )
                    st.info(
                        "Open Manage Incidents to review the new report."
                    )

                except ValueError as exc:
                    st.error(str(exc))
                except sqlite3.Error:
                    st.error("Database error: the report could not be saved.")


# ----------------------- MANAGE INCIDENTS ----------------

elif page == "Manage Incidents":
    st.markdown(
        '<div class="section-title">Incident Management</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        'Review reports and update their workflow status.</div>',
        unsafe_allow_html=True,
    )

    if incidents_df.empty:
        st.info("No incidents recorded.")
    else:
        f1, f2, f3 = st.columns([1, 1, 1.4])

        with f1:
            status_filter = st.selectbox(
                "Filter by status",
                ["All", "Pending", "Assigned", "Resolved"],
            )

        with f2:
            severity_filter = st.selectbox(
                "Filter by severity",
                ["All", "Critical", "High", "Medium", "Low"],
            )
        with f3:
            incident_search = st.text_input(
                "Search reports", placeholder="Name, location, need or ID"
            )

        filtered = incidents_df.copy()

        if status_filter != "All":
            filtered = filtered[filtered["status"] == status_filter]

        if severity_filter != "All":
            filtered = filtered[filtered["severity"] == severity_filter]
        if incident_search.strip():
            term = incident_search.strip().lower()
            searchable = (
                filtered["name"].astype(str).str.lower().str.contains(term, na=False)
                | filtered["location"].astype(str).str.lower().str.contains(term, na=False)
                | filtered["need"].astype(str).str.lower().str.contains(term, na=False)
                | filtered["id"].astype(str).str.contains(term, na=False)
            )
            filtered = filtered[searchable]

        table = filtered[
            ["id", "name", "location", "need", "severity",
             "people", "status", "created_at"]
        ].rename(columns={
            "id": "ID",
            "name": "Reporter",
            "location": "Location",
            "need": "Need",
            "severity": "Severity",
            "people": "People",
            "status": "Status",
            "created_at": "Created At",
        })

        st.dataframe(table, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Export filtered incidents (CSV)",
            data=table.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"reliefgrid_incidents_{datetime.now():%Y%m%d_%H%M}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.divider()
        st.subheader("Update Incident Status")

        ids = filtered["id"].tolist()

        if ids:
            selected_id = st.selectbox(
                "Select incident ID",
                ids,
                format_func=lambda value: (
                    f"#{value} — "
                    f"{filtered.loc[filtered['id'] == value, 'name'].iloc[0]}"
                ),
            )

            current_status = incidents_df.loc[
                incidents_df["id"] == selected_id, "status"
            ].iloc[0]

            new_status = st.selectbox(
                "New status",
                ["Pending", "Assigned", "Resolved"],
                index=["Pending", "Assigned", "Resolved"].index(
                    current_status
                ),
            )

            if st.button("Save Status", type="primary"):
                update_status(int(selected_id), new_status)
                st.success(f"Incident #{selected_id} updated to {new_status}.")
                st.rerun()
        else:
            st.info("No incidents match these filters.")


# ----------------------- RESOURCES -----------------------

elif page == "Relief Resources":
    st.markdown(
        '<div class="section-title">Relief Resource Inventory</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        'View resources entered into the local prototype database.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("➕ Add a relief resource", expanded=False):
        with st.form("add_resource_form", clear_on_submit=True):
            r1, r2 = st.columns(2)
            with r1:
                resource_name = st.text_input("Resource / facility name *", placeholder="e.g. Community Relief Camp")
                resource_type = st.selectbox("Resource category *", [
                    "Shelter", "Drinking water", "Medical help", "Food", "Rescue", "Other"
                ])
                resource_quantity = st.text_input("Available quantity *", placeholder="e.g. 40 beds / 200 kits")
            with r2:
                resource_location = st.text_input("Location *", placeholder="Village / town / district")
                resource_lat = st.text_input("Latitude (optional)", placeholder="e.g. 26.7509")
                resource_lon = st.text_input("Longitude (optional)", placeholder="e.g. 94.2037")
            resource_submit = st.form_submit_button("Save resource", type="primary", use_container_width=True)
            if resource_submit:
                if not all([resource_name.strip(), resource_quantity.strip(), resource_location.strip()]):
                    st.error("Please complete the resource name, quantity and location.")
                else:
                    try:
                        rlat = float(resource_lat) if resource_lat.strip() else None
                        rlon = float(resource_lon) if resource_lon.strip() else None
                        if (rlat is None) != (rlon is None):
                            raise ValueError("Enter both coordinates, or leave both blank.")
                        if rlat is not None and not -90 <= rlat <= 90:
                            raise ValueError("Latitude must be between -90 and 90.")
                        if rlon is not None and not -180 <= rlon <= 180:
                            raise ValueError("Longitude must be between -180 and 180.")
                        with get_connection() as conn:
                            conn.execute(
                                "INSERT INTO resources (name, type, quantity, location, lat, lon) VALUES (?, ?, ?, ?, ?, ?)",
                                (resource_name.strip(), resource_type, resource_quantity.strip(),
                                 resource_location.strip(), rlat, rlon)
                            )
                        st.success("Resource saved to the local inventory.")
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
                    except sqlite3.Error:
                        st.error("Database error: the resource could not be saved.")

    # Reload after a resource has been added
    resources_df = fetch_table("resources")
    if resources_df.empty:
        st.info("No resources listed.")
    else:
        search = st.text_input(
            "Search resources",
            placeholder="Search by name, type or location",
        )

        resource_types = ["All"] + sorted(
            resources_df["type"].dropna().unique().tolist()
        )

        selected_type = st.selectbox(
            "Resource category", resource_types
        )

        filtered_resources = resources_df.copy()

        if search.strip():
            search_lower = search.strip().lower()
            mask = (
                filtered_resources["name"].str.lower().str.contains(
                    search_lower, na=False
                )
                | filtered_resources["type"].str.lower().str.contains(
                    search_lower, na=False
                )
                | filtered_resources["location"].str.lower().str.contains(
                    search_lower, na=False
                )
            )
            filtered_resources = filtered_resources[mask]

        if selected_type != "All":
            filtered_resources = filtered_resources[
                filtered_resources["type"] == selected_type
            ]

        st.caption(
            f"{len(filtered_resources)} resource entries match your filters."
        )

        columns = st.columns(3)

        for index, (_, row) in enumerate(filtered_resources.iterrows()):
            with columns[index % 3]:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:14px">
                    <div class="metric-label">{row["type"]}</div>
                    <div style="color:#102b55;font-size:18px;
                                font-weight:800;margin-top:12px">
                        {html.escape(str(row["name"]))}
                    </div>
                    <div style="color:#1769aa;font-size:21px;
                                font-weight:800;margin-top:12px">
                        {html.escape(str(row["quantity"]))}
                    </div>
                    <div class="metric-note" style="margin-top:8px">
                        📍 {html.escape(str(row["location"]))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.download_button(
            "⬇️ Export resource inventory (CSV)",
            data=filtered_resources.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"reliefgrid_resources_{datetime.now():%Y%m%d_%H%M}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.divider()
        st.subheader("Resource Locations")

        mapped_resources = filtered_resources.dropna(
            subset=["lat", "lon"]
        )

        if not mapped_resources.empty:
            st.map(
                mapped_resources[["lat", "lon"]],
                latitude="lat",
                longitude="lon",
                size=20,
            )
        else:
            st.info("No mapped resource locations are available.")


# ----------------------- FOOTER --------------------------

st.divider()
st.caption(
    "ReliefGrid | Flood response prototype | "
    "Demo records are fictional; emergency information must be verified."
)
