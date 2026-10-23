
# 🌊 ReliefGrid
### Smarter Flood Response, Faster Relief

**ReliefGrid** is a flood emergency coordination and relief resource management platform designed to organize emergency reports, prioritize assistance requests, visualize reported incidents, and manage relief resources through a centralized, user-friendly dashboard.

The project demonstrates how digital technology can support disaster-response coordination by making emergency information easier to record, monitor, search, and analyze.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Deployment](#-deployment)
- [Database Design](#-database-design)
- [Benefits and Impact](#-benefits-and-impact)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌍 Overview

Floods can cause severe damage to homes, infrastructure, and livelihoods. During a flood, affected communities may urgently need rescue operations, medical assistance, food, clean drinking water, and temporary shelter.

Managing emergency requests and relief supplies using separate records can make coordination difficult.

ReliefGrid provides a centralized interface for recording emergency incidents, monitoring their status, identifying high-priority requests, and maintaining an inventory of relief resources.

The current project is a working prototype built with Python and Streamlit, with SQLite used for local data storage.

### Project Information

| Detail | Description |
|---|---|
| Project Name | ReliefGrid |
| Tagline | Smarter Flood Response, Faster Relief |
| Domain | Disaster Management |
| Application Type | Web-Based Dashboard |
| Frontend and Interface | Streamlit |
| Backend Logic | Python |
| Database | SQLite |
| Data Processing | Pandas |
| Visualization | Plotly |
| Project Stage | Hackathon Prototype |

---

## 🚨 Problem Statement

Flood emergencies create several coordination challenges:

1. **Scattered emergency information:** Requests for assistance can be difficult to organize and track.
2. **Difficulty identifying urgent cases:** Response teams need a structured way to identify reports marked as critical or high severity.
3. **Limited incident visibility:** Without a map, understanding the geographical distribution of recorded incidents can be difficult.
4. **Resource coordination challenges:** Information about food, drinking water, shelters, medical teams, and rescue resources needs to be organized.
5. **Limited progress tracking:** Emergency reports need clear statuses so that users can monitor their progress.
6. **Difficult reporting:** Manually compiling incident and resource information can take additional time.

These challenges motivate the development of a centralized flood-relief coordination prototype.

---

## 💡 Our Solution

ReliefGrid brings emergency reporting, incident management, geographical visualization, and relief resource tracking into a single dashboard.

Users can submit emergency reports, record the number of people affected, specify the assistance required, assign a severity level, and optionally provide geographical coordinates.

The application calculates a priority score for recorded incidents, displays open reports in a priority queue, and allows users to update their status.

A separate resource inventory helps users record and search information about relief resources.

---

## ✨ Key Features

### 1. 🚨 Emergency SOS Reporting

Users can submit structured emergency reports containing:

- Reporter name
- Contact number
- Village, town, or location
- Number of people affected
- Type of assistance required
- Emergency severity
- Optional latitude and longitude
- Additional incident details

The application validates required fields and geographical coordinate ranges before saving a report.

New reports are stored in the local SQLite database and initially receive the `Pending` status.

**Available assistance categories include:**

- Rescue
- Medical help
- Drinking water
- Food
- Shelter
- Other

### 2. 🗺️ Interactive Incident Map

ReliefGrid uses Plotly to visualize recorded incidents with geographical coordinates.

The map supports:

- Geographical visualization of recorded reports
- Severity-based marker colors
- Marker sizes based on the number of people affected
- Hover information for incident details
- Interactive map navigation

The map displays stored report coordinates. It does not independently detect floods or verify real-world emergency locations.

### 3. 🎯 Priority-Based Incident Management

The application calculates a priority score using the reported severity, number of people affected, and certain assistance requirements.

The scoring logic is:

- Critical severity: 100 base points
- High severity: 70 base points
- Medium severity: 40 base points
- Low severity: 15 base points
- Additional points based on the number of people affected, capped at 100
- An additional 20 points for Rescue or Medical help requests

The resulting score helps order open incidents in the dashboard's priority queue.

**Important:** This is a prototype scoring formula, not a validated emergency triage model. Actual response decisions require trained personnel and verified information.

### 4. 📋 Incident Management

The incident management section allows users to:

- View recorded incidents in a table
- Filter reports by status
- Filter reports by severity
- Review reporter and location information
- View the requested assistance
- See the number of people affected
- Update an incident's workflow status

Available statuses:

- **Pending:** The report is awaiting action.
- **Assigned:** The report has been marked as assigned.
- **Resolved:** The report has been marked as resolved.

These statuses are administrative records. They do not confirm that a rescue team has actually been dispatched or that an emergency has been independently verified.

### 5. 🏥 Relief Resource Management

ReliefGrid maintains a resource inventory for organizing information about relief supplies and services.

Example resource categories include:

- Shelter and accommodation
- Food supplies
- Drinking water
- Medical assistance
- Rescue units

Resource records include a name, category, quantity, location, and optional geographical coordinates.

Users can search resource names, types, and locations, filter by category, and view mapped resource locations when coordinates are available.

The current prototype includes resource viewing and filtering. Resource creation, editing, and deletion are not yet available through the existing interface.

### 6. 📊 Situation Overview Dashboard

The overview dashboard presents key indicators:

- Open incidents
- High-priority incidents
- People affected across open reports
- Number of resource entries

It also includes a priority queue and a table of recent incident reports.

These indicators help users understand the information currently recorded in the application without manually reviewing every incident.

### 7. 🔎 Search and Filtering

The application provides filtering tools to help users find relevant information.

Users can filter incidents by severity and workflow status and search the resource inventory by resource name, type, or location.

This makes the recorded information easier to navigate as the number of entries increases.

### 8. 📥 CSV Data Export

Incident and resource information can be exported as CSV files for use in spreadsheet software, further analysis, and reporting.

CSV exports can help with preparing summaries and sharing structured records.

### 9. 💾 Local Database Storage

ReliefGrid uses SQLite to store incident and resource information.

The database is created automatically when the application starts. The prototype also inserts fictional demonstration records when the corresponding tables are empty.

Because the application uses local SQLite storage, persistent storage and multi-user synchronization require additional consideration when deployed to a cloud environment.

---

## 🔄 How It Works

The application's primary workflow is:

1. **Record an emergency:** Enter the reporter's information, location, assistance required, severity, and other details.
2. **Validate the report:** Check required fields and optional geographical coordinates.
3. **Store the report:** Save the incident in the SQLite database.
4. **Calculate priority:** Generate a score using the configured priority formula.
5. **Review the dashboard:** View open incidents, priority indicators, and mapped reports.
6. **Manage the response record:** Update the report status as its workflow progresses.
7. **Review resources:** Search and filter the recorded relief resource inventory.
8. **Export information:** Download available records as CSV files.

### Workflow Diagram

```text
        Emergency Report
               |
               v
       Input Validation
               |
               v
       SQLite Database
               |
               v
      Priority Calculation
               |
               v
       Overview Dashboard
          /          \
         v            v
 Incident Tracking  Resource Review
         \            /
          v          v
          CSV Export
```

---

## 🛠️ Technology Stack

### Python

Python implements the application's logic, database operations, data validation, priority scoring, and incident management.

### Streamlit

Streamlit provides the interactive web interface, including navigation, forms, tables, metrics, filters, and dashboard components.

### Pandas

Pandas loads, processes, filters, and formats incident and resource records for analysis and presentation.

### Plotly

Plotly creates interactive geographical visualizations of incidents and supports map-based exploration of recorded information.

### SQLite

SQLite provides a lightweight relational database for storing incidents and relief resources without requiring a separate database server.

### Technology Summary

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| Pandas | Data processing |
| Plotly | Interactive maps |
| SQLite | Data storage |

---

## 🏗️ System Architecture

ReliefGrid follows a simple application architecture:

**User Interface Layer**
- Streamlit pages, forms, filters, and dashboard components.

**Application Logic Layer**
- Input validation
- Incident creation
- Priority scoring
- Status updates
- Data filtering and export

**Data Layer**
- SQLite database
- Incident records
- Relief resource records

**Visualization Layer**
- Interactive incident map
- Resource location map
- Dashboard metrics and tabular reports

The current implementation runs these components within a single Python application.

---

## 📁 Project Structure

The main files are organized as follows:

```text
reliefgrid/
│
├── app.py
├── requirements.txt
├── README.md
└── floodrelief.db
```

### File Descriptions

- `app.py` — Main Streamlit application.
- `requirements.txt` — Python dependencies installed during setup and deployment.
- `README.md` — Project documentation.
- `floodrelief.db` — SQLite database generated when the application runs.

The database file may not exist in the repository before the first local run because the application creates it automatically.

Avoid committing real personal information or sensitive emergency records to a public repository.

---

## ⚙️ Installation and Setup

### Prerequisites

Install:

- Python
- Git (optional, for cloning the repository)
- A web browser

### Step 1: Clone the Repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/reliefgrid.git
cd reliefgrid
```

Alternatively, download the repository as a ZIP file and extract it.

### Step 2: Create the Requirements File

Create a file named `requirements.txt` in the same directory as `app.py`.

Add the following dependencies:

```text
streamlit
pandas
plotly
```

### Step 3: Install Dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

### Step 4: Start the Application

Run:

```bash
python -m streamlit run app.py
```

### Step 5: Open the Dashboard

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open this URL in your browser.

---

## ☁️ Deployment

### Deploy Using Streamlit Community Cloud

ReliefGrid can be deployed to Streamlit Community Cloud for online demonstrations.

1. Upload `app.py`, `requirements.txt`, and the README to a GitHub repository.
2. Visit https://share.streamlit.io/
3. Sign in with your GitHub account.
4. Create a new application.
5. Select the repository and deployment branch.
6. Set the main application file to `app.py`.
7. Deploy the application.
8. Share the generated public URL.

### Cloud Database Considerations

The current application stores records in a local SQLite database. Cloud restarts, rebuilds, or changes to the runtime may affect locally stored data.

For a production or multi-user version, use a persistent database service and implement suitable access controls, backups, and data validation.

---

## 🗄️ Database Design

ReliefGrid uses two main database tables.

### Incidents

The incidents table records emergency requests.

| Field | Description |
|---|---|
| `id` | Unique incident identifier |
| `name` | Reporter name |
| `phone` | Contact number |
| `location` | Reported location |
| `lat` | Latitude, if available |
| `lon` | Longitude, if available |
| `people` | Number of people affected |
| `need` | Assistance required |
| `severity` | Reported severity |
| `notes` | Additional details |
| `status` | Incident workflow status |
| `created_at` | Report creation timestamp |

### Resources

The resources table records available relief resources.

| Field | Description |
|---|---|
| `id` | Unique resource identifier |
| `name` | Resource name |
| `type` | Resource category |
| `quantity` | Recorded quantity or capacity |
| `location` | Resource location |
| `lat` | Latitude, if available |
| `lon` | Longitude, if available |

The current prototype does not independently verify whether listed resources are available in the real world.

---

## 🌟 Benefits and Potential Impact

ReliefGrid demonstrates several ways software can support disaster-response information management:

- **Centralized records:** Keep incident and resource information in one interface.
- **Clearer priorities:** Use a consistent prototype scoring formula to organize open reports.
- **Geographical visibility:** Display the locations associated with recorded reports.
- **Simplified tracking:** Monitor the administrative status of incidents.
- **Organized resource information:** Search and filter recorded relief resources.
- **Accessible interface:** Use a browser-based dashboard rather than a specialized desktop application.
- **Reusable reporting:** Export records for analysis and documentation.

The platform is intended to support coordination and information organization, not replace emergency services or trained disaster-response personnel.

---

## ⚠️ Current Limitations

ReliefGrid is a hackathon prototype and has the following limitations:

- Demonstration incidents and resources may be fictional.
- Flood-risk data and weather conditions are not obtained from a verified live data feed.
- SOS reports are saved locally and are not automatically sent to emergency services.
- The application does not dispatch rescue teams.
- Priority scores are illustrative and are not clinically or operationally validated.
- Local SQLite storage does not provide automatic multi-user synchronization.
- Resource information is not independently verified.
- Automated flood-safe route planning is not implemented.
- User authentication and role-based permissions are not implemented in the current workflow.

These limitations should be addressed before considering real-world emergency deployment.

---

## 🔮 Future Enhancements

Potential future development includes:

### 1. Live Flood and Weather Data
Integrate verified weather services, flood warnings, river-level observations, and other authoritative data sources.

### 2. Persistent Cloud Database
Introduce a hosted database to support reliable storage and synchronized access from multiple devices.

### 3. User Authentication
Create appropriate roles for administrators, coordinators, and authorized relief workers.

### 4. Emergency Notifications
Integrate authorized notification services for status updates and emergency communication.

### 5. Route Planning
Explore verified road-network data and routing methods to help identify possible routes to reported locations and relief facilities.

### 6. Resource Allocation
Develop tools to match recorded needs with verified resource capacity and availability.

### 7. Mobile-Friendly Reporting
Improve mobile usability and explore location-sharing capabilities with clear user consent.

### 8. Audit Logs and Data Protection
Add accountability features, access restrictions, backups, and privacy safeguards for sensitive records.

These are proposed enhancements and are not claimed to be implemented in the current version.

---

## 🤝 Contributing

Contributions and suggestions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch for your change.
3. Make and test your changes.
4. Commit the changes with a clear message.
5. Open a pull request describing your improvement.

Please avoid submitting real personal information, private contact details, or unverified emergency data.

---

## 📄 License

No license has been specified for this project yet.

Before allowing reuse or redistribution, add a suitable open-source license file, such as an MIT License, if that matches the project's intended terms.

---

## 👨‍💻 Project Summary

**ReliefGrid — Smarter Flood Response, Faster Relief**

ReliefGrid is a Python-based flood emergency coordination prototype that combines emergency reporting, priority scoring, incident tracking, geographical visualization, and relief resource management in a single Streamlit dashboard.

The project demonstrates how accessible software technologies can help organize disaster-response information and provides a foundation for future improvements in live data integration, secure collaboration, and resource coordination.

**Built for innovation. Designed for coordination. Focused on faster relief.**
