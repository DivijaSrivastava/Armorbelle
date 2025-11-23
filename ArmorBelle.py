import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import requests
import json 


# Configuration for the simulated SOS states
SOS_STATES = {
    'SAFE': {'color': '#3C9D9B', 'text': 'System Status: SAFE & NOMINAL'},
    'ALERT': {'color': '#F05454', 'text': 'ALERT: SOS Signal Initiated'},
    'TIMEOUT': {'color': '#FFD700', 'text': 'Standby: Pending System Check'},
}

# Fetch location data from an external service (Global scope variables)
try:
    response = requests.get('http://ipinfo.io/json')
    data = response.json()
    # These variables are accessed globally in _update_location_data
    ip_address = data['ip']
    city = data['city']
    region = data['region']
    country = data['country']
except requests.exceptions.RequestException:
    # Set safe defaults if API call fails
    ip_address = "N/A - Offline"
    city = "N/A - Offline"
    region = ""
    country = "N/A - Offline"


print(f"IP Address: {ip_address}")
print(f"Location: {city}, {region}, {country}")

# --- Main Application Class ---

class SafetyDashboardApp:
    """
    A complete Tkinter application simulating a safety and status dashboard.
    Uses threading for simulated background operations without freezing the GUI.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("ArmorBelle Safety Dashboard")
        self.root.geometry("800x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#E0E0E0")

        # Application state
        self.is_sos_active = False
        self.current_sos_state = 'SAFE'
        self.background_thread = None

        self._setup_ui()

    def _setup_ui(self):
        """Sets up the main layout and widgets."""

        # 1. Main Content Frame (Centered)
        main_frame = tk.Frame(self.root, bg="#FFFFFF", padx=20, pady=20, bd=1, relief=tk.RAISED)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        tk.Label(
            main_frame,
            text="🛡️ArmorBelle - Your E-Armor",
            font=("Georgia", 18, "bold"),
            bg="#BA5E7C",
            fg="#F1F1F1"
        ).pack(pady=(0, 20))

        # Two-Panel Layout (using grid)
        content_frame = tk.Frame(main_frame, bg="#FFFFFF")
        content_frame.pack(fill="both", expand=True)

        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # 2. Status Panel (Left)
        self.status_panel = self._create_status_panel(content_frame)
        self.status_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # 3. Data Panel (Right)
        self.data_panel = self._create_data_panel(content_frame)
        self.data_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 4. Control Button (Bottom)
        self.sos_button = tk.Button(
            main_frame,
            text="Help just a click away!",
            command=self._start_sos_sequence,
            font=("Georgia", 14, "bold"),
            bg="#AB5178",
            fg="white",
            activebackground="#C2185B",
            activeforeground="white",
            width=20,
            relief=tk.RAISED,
            bd=5
        )
        self.sos_button.pack(pady=20)

        # Initial UI update
        self._update_ui()
       
        self._update_location_data() 


    def _create_status_panel(self, parent):
        """Creates the SOS status display panel."""
        panel = tk.LabelFrame(
            parent,
            text="🚨 System Status",
            font=("Arial", 12, "bold"),
            bg='#F0F0F0',
            padx=10,
            pady=10
        )

        # Status Text Label
        self.status_label = tk.Label(
            panel,
            text=SOS_STATES['SAFE']['text'],
            font=("Times New Roman", 12),
            bg=panel['bg'],
            wraplength=200
        )
        self.status_label.pack(pady=(10, 5))

        # Visual Indicator (Canvas)
        self.indicator_canvas = tk.Canvas(panel, width=150, height=150, bg=panel['bg'], highlightthickness=0)
        self.indicator_canvas.pack(pady=10, padx=10)

        # Create a circle on the canvas
        self.indicator_circle = self.indicator_canvas.create_oval(
            10, 10, 140, 140,
            fill=SOS_STATES['SAFE']['color'],
            outline=SOS_STATES['SAFE']['color'],
            width=2
        )

        return panel

    def _create_data_panel(self, parent):
        """Creates the location and auxiliary data display panel."""
        panel = tk.LabelFrame(
            parent,
            text="📍 Your location",
            font=("Times New Roman", 12, "bold"),
            bg="#F8F8F8",
            padx=10,
            pady=10
        )

        # Location labels setup
        tk.Label(panel, text="Public IP:", font=("Times New Roman", 10, "bold"), anchor="w", bg=panel['bg']).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.ip_label = tk.Label(panel, text="Loading...", font=("Times New Roman", 10), anchor="w", bg=panel['bg'])
        self.ip_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        tk.Label(panel, text="City:", font=("Times New Roman", 10, "bold"), anchor="w", bg=panel['bg']).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.city_label = tk.Label(panel, text="Loading...", font=("Times New Roman", 10), anchor="w", bg=panel['bg'])
        self.city_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        tk.Label(panel, text="Country:", font=("Times New Roman", 10, "bold"), anchor="w", bg=panel['bg']).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.country_label = tk.Label(panel, text="Loading...", font=("Times New Roman", 10), anchor="w", bg=panel['bg'])
        self.country_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # Simulation/Log Message
        self.log_label = tk.Label(
            panel,
            text="Awaiting user command...",
            font=("Times New Roman", 9, "italic"),
            fg="#757575",
            bg=panel['bg'],
            pady=10
        )
        self.log_label.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        return panel

    def _update_location_data(self):
        """Updates the Geo & Device Info panel with initial location data."""
        # Accessing global variables defined outside the class
        global ip_address, city, region, country 
        
        self.ip_label.config(text=ip_address)
        self.city_label.config(text=city)
        self.country_label.config(text=f"{country} ({region})")

    def _start_sos_sequence(self):
        """Handles the SOS button press and starts the threaded sequence."""
        if self.is_sos_active:
            # If active, the button acts as a CANCEL/RESET button
            self._reset_sos()
        else:
            # If inactive, start the sequence
            self.is_sos_active = True
            self.sos_button.config(text="CANCEL SOS", bg="#3C9D9B")
            self.log_label.config(text="SOS sequence starting...")

            # Start the background thread for the sequence
            self.background_thread = threading.Thread(target=self._sos_sequence_logic)
            self.background_thread.start()

            # Update UI immediately
            self.current_sos_state = 'ALERT'
            self._update_ui()

            messagebox.showwarning("SOS Initiated", "The SOS sequence has been started. Sending alert in 5 seconds.")

    def _sos_sequence_logic(self):
        """
        The heavy-lifting logic that runs in a separate thread.
        NOTE: Tkinter widgets cannot be directly modified from this thread.
        Use self.root.after() to schedule UI updates on the main thread.
        """
        try:
            # Step 1: Simulated Wait (e.g., waiting for GPS fix, contacting server)
            time.sleep(5)

            # Check if the user cancelled during the wait
            if not self.is_sos_active:
                return

            # Step 2: Confirmation / Timeout (Schedule UI update via main thread)
            self.root.after(0, lambda: self.log_label.config(text="Confirmation sent. Awaiting acknowledgment..."))
            self.root.after(0, lambda: self._update_sos_state('TIMEOUT'))

            # Step 3: Simulated Server Response Wait
            time.sleep(5)

            # Check if the user cancelled during the wait
            if not self.is_sos_active:
                return

            # Step 4: Final Success/Failure (Schedule UI update via main thread)
            success = random.choice([True, False])

            if success:
                self.root.after(0, lambda: self._show_success("SOS ACKNOWLEDGED", "Help is on the way. Tracking device location."))
            else:
                self.root.after(0, lambda: self._show_failure("SOS FAILED", "Attempt to contact server failed. Retrying..."))

            # Step 5: Reset after final message
            time.sleep(3)
            self.root.after(0, self._reset_sos)


        except Exception as e:
            self.root.after(0, lambda: self.log_label.config(text=f"ERROR in thread: {e}"))
            self.root.after(0, self._reset_sos)
            
    def _update_sos_state(self, new_state):
        """Updates the internal state and calls the UI update function."""
        self.current_sos_state = new_state
        self._update_ui()
        
    def _show_success(self, title, message):
        """Handles success message and logs."""
        messagebox.showinfo(title, message)
        self.log_label.config(text=f"SUCCESS: {message}")

    def _show_failure(self, title, message):
        """Handles failure message and logs."""
        messagebox.showerror(title, message)
        self.log_label.config(text=f"FAILURE: {message}")

    def _reset_sos(self):
        """Resets the application to the default 'SAFE' state."""
        self.is_sos_active = False
        self.current_sos_state = 'SAFE'
        self.sos_button.config(text="Help just a click away", bg="#AF416D")
        self.log_label.config(text="System reset and awaiting command.")
        self._update_ui()


    def _update_ui(self):
        """
        Refreshes all GUI elements based on the current application state.
        This must always be called on the main thread (i.e., not inside _sos_sequence_logic).
        """
        state_config = SOS_STATES[self.current_sos_state]
        color = state_config['color']
        text = state_config['text']

        self.status_label.config(text=text, fg=color)

        # Update Canvas Circle
        self.indicator_canvas.itemconfig(self.indicator_circle, fill=color, outline=color)

        # Add a simple pulsing effect for ALERT state using root.after
        if self.current_sos_state == 'ALERT':
            # Toggle indicator color every 500ms
            current_fill = self.indicator_canvas.itemcget(self.indicator_circle, 'fill')
            new_color = "#FF8C00" if current_fill == color else color
            self.indicator_canvas.itemconfig(self.indicator_circle, fill=new_color, outline=new_color)

            # Schedule the next toggle
            self.pulse_job = self.root.after(500, self._update_ui)
        else:
            # Stop the pulsing effect if it's running
            if hasattr(self, 'pulse_job'):
                self.root.after_cancel(self.pulse_job)
                del self.pulse_job

            # Ensure the color is set correctly to the final state color
            self.indicator_canvas.itemconfig(self.indicator_circle, fill=color, outline=color)


if __name__ == '__main__':
    root = tk.Tk()
    app = SafetyDashboardApp(root)
    root.mainloop()