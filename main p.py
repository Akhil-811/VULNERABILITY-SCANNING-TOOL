import tkinter as tk
from tkinter import messagebox
import socket
import os
import threading

def scan_network():
    """
    Function to scan the network for open ports on a specific IP range.
    """
    ip_range = ip_range_entry.get()
    if not ip_range:
        messagebox.showerror("Error", "Please enter an IP range.")
        return

    start_ip, end_ip = ip_range.split('-')

    # Scanning open ports for each IP in the range
    open_ports = []
    for ip in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1]) + 1):
        ip_to_scan = f"{start_ip.rsplit('.', 1)[0]}.{ip}"
        for port in range(1, 65535):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip_to_scan, port))
            if result == 0:
                open_ports.append(f"{ip_to_scan}:{port}")
            sock.close()

    if open_ports:
        ports_info.set(f"Open ports found: {', '.join(open_ports)}")
    else:
        ports_info.set("No open ports found.")

def check_software_versions():
    """
    Function to check for outdated software versions.
    """
    software_list = [
        {"name": "Python", "command": "python --version"},
        {"name": "Node.js", "command": "node --version"},
        # Add more software if needed
    ]

    outdated_softwares = []

    for software in software_list:
        try:
            result = os.popen(software["command"]).read().strip()
            if "not found" in result.lower() or "v" in result.lower():
                outdated_softwares.append(software["name"])
        except Exception as e:
            outdated_softwares.append(software["name"])

    if outdated_softwares:
        versions_info.set(f"Outdated software versions: {', '.join(outdated_softwares)}")
    else:
        versions_info.set("No outdated software versions found.")

def on_scan_button_click():
    """
    Function to be called when the 'Scan Network' button is clicked.
    It starts network scan and software version checks in separate threads.
    """
    # Clear previous results
    ports_info.set("")
    versions_info.set("")

    # Start scanning in separate threads
    network_thread = threading.Thread(target=scan_network)
    version_thread = threading.Thread(target=check_software_versions)

    network_thread.start()
    version_thread.start()

# Initialize the main application window
root = tk.Tk()
root.title("Vulnerability Scanning Tool")

# Set the size of the window
root.geometry("400x300")

# Create an entry for IP range input
ip_range_label = tk.Label(root, text="Enter IP Range (e.g., 192.168.1.1-192.168.1.255):")
ip_range_label.pack(pady=10)

ip_range_entry = tk.Entry(root, width=30)
ip_range_entry.pack(pady=10)

# Create a button to start the network scan
scan_button = tk.Button(root, text="Scan Network", command=on_scan_button_click)
scan_button.pack(pady=10)

# Label to display information about open ports
ports_info = tk.StringVar()
ports_info_label = tk.Label(root, textvariable=ports_info, font=("Helvetica", 12))
ports_info_label.pack(pady=10)

# Label to display information about outdated software versions
versions_info = tk.StringVar()
versions_info_label = tk.Label(root, textvariable=versions_info, font=("Helvetica", 12))
versions_info_label.pack(pady=10)

# Run the main application loop
root.mainloop()
