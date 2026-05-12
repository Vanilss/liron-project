# Dashboard אישי (Personal Dashboard)

A Streamlit-based Hebrew data visualization dashboard application.

## Features

- **Home Page (מסך הבית)**: Overview metrics display
- **Financial Analysis (ניתוח פיננסי)**: Sector comparison charts with growth rate visualization
- **Performance Tracking (מעקב ביצועים)**: Detailed data tables
- **Data Management (הגדרות נתונים)**: Excel/CSV file upload functionality

## Project Structure

```
.
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration for Coolify
├── .dockerignore       # Files to exclude from Docker build
└── README.md           # This file
```

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

The application will open at `http://localhost:8501`

## Docker Deployment (Coolify)

### Building the Docker image

```bash
docker build -t dashboard-app .
```

### Running the Docker container

```bash
docker run -p 8501:8501 dashboard-app
```

Access the application at `http://localhost:8501`

### Deploying to Coolify

1. Push this repository to your Git provider (GitHub, GitLab, etc.)
2. Create a new application in Coolify
3. Connect your Git repository
4. Select the Dockerfile option
5. Set the port to `8501`
6. Deploy

## Environment Variables

- `STREAMLIT_SERVER_HEADLESS`: Set to `true` (required for Docker)
- `STREAMLIT_SERVER_PORT`: Set to `8501` (default Streamlit port)
- `STREAMLIT_SERVER_ADDRESS`: Set to `0.0.0.0` (listen on all interfaces)

## Dependencies

- `streamlit`: Web app framework
- `pandas`: Data manipulation
- `plotly.express`: Interactive visualizations
