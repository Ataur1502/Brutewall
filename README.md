# BruteWall: Brute-Force Attack Simulator & Protector

BruteWall is a Django application designed to simulate and protect against brute-force login attacks. It provides a hands-on demonstration of how rate limiting and temporary IP blocking can be used to secure a web application. The project includes a dashboard for visualizing attack patterns and managing blocked IPs.

## Features

- **IP-Based Attempt Tracking:** Monitors and records login attempts from unique IP addresses.
- **Configurable Brute-Force Threshold:** Set a limit on how many failed login attempts are allowed before an IP is blocked.
- **Temporary IP Blocking:** Automatically blocks IPs that exceed the failure threshold for a configurable duration.
- **Progressive Delays:** Introduces increasing delays after successive failed login attempts to slow down attackers.
- **Visual Dashboard:** A comprehensive dashboard that displays:
  - A list of all tracked IPs with their current status.
  - Counts of blocked vs. active IPs.
  - A heatmap visualizing login attempt frequency by date and hour.
- **Admin Controls:**
  - Manually reset or unblock any IP address.
  - Export all login attempt logs to a CSV file.
- **Simulated Login:** A simple login form to test the brute-force protection mechanisms.

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/brutewall.git
    cd brutewall
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file is not yet present. I will add one.)*

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser to access the admin dashboard:**
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

1.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

2.  **Access the application:**
    - **Login Page:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - **Admin Dashboard:** [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/) (requires login)

## Project Structure

```
brutewall/
├── brutewall/         # Django project directory
│   ├── settings.py    # Project settings
│   ├── urls.py        # Root URL configuration
│   └── ...
├── core/              # Main application
│   ├── models.py      # Database models (IPAttempt)
│   ├── views.py       # Application views (login, dashboard, etc.)
│   ├── urls.py        # App-specific URLs
│   ├── admin.py       # Admin site configurations
│   └── templates/     # HTML templates
├── manage.py          # Django's command-line utility
└── db.sqlite3         # SQLite database
```

## Configuration

The primary settings for the brute-force protection can be configured in `brutewall/settings.py`:

- `BRUTE_BLOCK_THRESHOLD`: The number of failed attempts before an IP is blocked. (Default: `5`)
- `BRUTE_BLOCK_DURATION_MINUTES`: The duration in minutes for which an IP is blocked. (Default: `10`)

## Admin Features

### Dashboard

The main dashboard provides a real-time overview of all IP activity. You can see which IPs are currently blocked, how many attempts each has made, and when they were last active.

### Resetting an IP

If an IP is blocked, you can manually unblock it from the dashboard by clicking the "Reset" button next to the IP address. This will reset its attempt count and remove the block.

### Exporting Logs

You can download a complete record of all IP attempts by clicking the "Export Logs (CSV)" button on the dashboard. This is useful for analysis and record-keeping.
