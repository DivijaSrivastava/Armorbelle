# Armorbelle
A key To Womens Safety.
# ArmorBelle Safety Dashboard

## Overview

ArmorBelle is a simulated safety and emergency response dashboard application built with Python and Tkinter. The application provides a visual interface for initiating SOS alerts and displays real-time location information to simulate a personal safety device.

## Features

- **SOS Alert System**: Initiate emergency alerts with a single click
- **Real-time Location Tracking**: Displays IP address, city, and country information
- **Visual Status Indicators**: Color-coded status display with pulsing alert animations
- **Threaded Operations**: Non-blocking background processes ensure smooth UI performance
- **Simulated Emergency Response**: Demonstrates alert confirmation and acknowledgment flow

## System States

The dashboard operates in three distinct states:

- **SAFE** (Green): Normal operation mode
- **ALERT** (Red): SOS signal initiated and in progress
- **TIMEOUT** (Gold): Awaiting system check or confirmation

## Requirements

### Python Version
- Python 3.6 or higher

### Dependencies

```bash
pip install requests
```

Built-in libraries used:
- `tkinter` (usually included with Python)
- `threading`
- `time`
- `random`
- `json`

## Installation

1. Clone or download the application files
2. Install required dependencies:
   ```bash
   pip install requests
   ```
3. Run the application:
   ```bash
   python armorbelle_dashboard.py
   ```

## Usage

### Starting the Application

Run the main Python file to launch the dashboard:

```bash
python armorbelle_dashboard.py
```

### Initiating an SOS Alert

1. Click the **"Help just a click away!"** button
2. The system will enter ALERT mode with a pulsing red indicator
3. A confirmation message will appear
4. The system simulates a 5-second wait period for alert transmission
5. After transmission, it awaits acknowledgment (another 5 seconds)
6. A success or failure message will be displayed

### Canceling an SOS Alert

While an SOS sequence is active, the button changes to **"CANCEL SOS"**. Click it to abort the current alert sequence.

## Application Architecture

### Main Components

- **SafetyDashboardApp**: Main application class managing UI and state
- **Status Panel**: Displays current system status with visual indicators
- **Data Panel**: Shows location information retrieved from ipinfo.io API
- **Control Button**: Primary interaction point for SOS functionality

### Threading Model

The application uses threading to prevent UI freezing during simulated network operations:
- Main thread handles all UI updates and user interactions
- Background thread manages SOS sequence timing and logic
- `root.after()` method ensures thread-safe UI updates

## Location Services

The application fetches location data from the ipinfo.io API at startup:
- Public IP address
- City
- Region
- Country

If the API call fails (offline mode), default "N/A - Offline" values are displayed.

## Customization

### Modifying SOS States

Edit the `SOS_STATES` dictionary to customize colors and messages:

```python
SOS_STATES = {
    'SAFE': {'color': '#3C9D9B', 'text': 'Your custom safe message'},
    'ALERT': {'color': '#F05454', 'text': 'Your custom alert message'},
    'TIMEOUT': {'color': '#FFD700', 'text': 'Your custom timeout message'},
}
```

### Adjusting Timing

Modify sleep durations in `_sos_sequence_logic()` method:

```python
time.sleep(5)  # Change wait time (in seconds)
```

## Limitations

- **Simulation Only**: This is a demonstration application and does not send real emergency alerts
- **Location Accuracy**: Uses IP-based geolocation which may not reflect precise physical location
- **No Persistent Storage**: Alert history is not saved between sessions
- **Internet Required**: Location services require active internet connection

## Security Considerations

- Location data is fetched from a third-party API (ipinfo.io)
- No sensitive data is stored or transmitted
- For production use, implement proper authentication and encryption

## Future Enhancements

Potential improvements for a production version:
- Integration with actual emergency services APIs
- GPS-based precise location tracking
- Alert history and logging
- Contact management for emergency notifications
- SMS/Email notification capabilities
- User authentication system
- Database integration for persistent storage

## Troubleshooting

### Application Won't Start
- Verify Python 3.6+ is installed: `python --version`
- Check if tkinter is available: `python -m tkinter`

### Location Shows "N/A - Offline"
- Check internet connection
- Verify ipinfo.io is accessible
- Check firewall settings

### UI Freezes During SOS
- This shouldn't happen due to threading, but if it does, restart the application
- Check console for error messages


