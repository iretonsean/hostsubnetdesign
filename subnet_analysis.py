import tkinter as tk
from tkinter import messagebox


def SubnetAnalysisTab(parent):
    """Set up the Subnet Analysis Practice tab."""
    analysis_frame = tk.Frame(parent, padx=20, pady=20)
    analysis_frame.pack(fill="both", expand=True, anchor="n")

    # Table labels
    labels = ["IP", "CLASS", "DSNM", "NSNM", "# NETBITS", "# SUBNET BITS", "# HOST BITS", "NET ID", "1ST HOST", "BA", "LAST HOST"]
    analysis_entries = {}

    for row, label in enumerate(labels):
        # Add label
        tk.Label(analysis_frame, text=label, bg="gray", fg="black", width=15, anchor="w").grid(row=row, column=0, sticky="nsew", padx=1, pady=1)

        # Add input box
        entry = tk.Entry(analysis_frame, bg="white", width=30)
        entry.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
        analysis_entries[label] = entry

    # Buttons
    tk.Button(analysis_frame, text="Generate Problem", command=lambda: generate_analysis_problem(analysis_entries)).grid(row=len(labels), column=0, padx=5, pady=5)
    tk.Button(analysis_frame, text="Check Answers", command=lambda: check_analysis_answers(analysis_entries)).grid(row=len(labels), column=1, padx=5, pady=5)


def generate_analysis_problem(entries):
    """Generate a subnet analysis problem."""
    # Example problem generation
    entries["IP"].insert(0, "192.168.1.1/24")  # Example IP


def check_analysis_answers(entries):
    """Check answers in the analysis practice tab."""
    # Example checking logic
    for label, entry in entries.items():
        if entry.get() == "correct":  # Replace "correct" with actual logic
            entry.config(bg="lightgreen")
        else:
            entry.config(bg="red")
