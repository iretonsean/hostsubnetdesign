import tkinter as tk
from tkinter import messagebox
import random
import ipaddress


def SubnetAnalysisTab(parent):
    """Set up the Subnet Analysis Practice tab."""
    analysis_frame = tk.Frame(parent, padx=20, pady=20)
    analysis_frame.pack(fill="both", expand=True, anchor="n")

    # Table labels
    labels = ["IP", "CLASS", "DSNM", "NSNM", "# NETBITS", "# SUBNET BITS", "# HOST BITS", "NET ID", "1ST HOST", "BA", "LAST HOST"]
    analysis_entries = {}
    global problem_ip, prefix_length, correct_values

    # Generate table with labels and inputs
    for row, label in enumerate(labels):
        # Add static label
        tk.Label(analysis_frame, text=label, bg="gray", fg="black", width=15, anchor="w").grid(row=row, column=0, sticky="nsew", padx=1, pady=1)

        # IP will be a label, not editable
        if label == "IP":
            problem_ip_label = tk.Label(analysis_frame, text="", bg="white", width=30, anchor="w")
            problem_ip_label.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
        else:
            # Add input box for other fields
            entry = tk.Entry(analysis_frame, bg="white", width=30)
            entry.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
            analysis_entries[label] = entry

    # Buttons for generating and checking answers
    tk.Button(analysis_frame, text="Generate Problem", command=lambda: generate_analysis_problem(problem_ip_label, analysis_entries)).grid(row=len(labels), column=0, padx=5, pady=5)
    tk.Button(analysis_frame, text="Check Answers", command=lambda: check_analysis_answers(analysis_entries)).grid(row=len(labels), column=1, padx=5, pady=5)


def generate_analysis_problem(ip_label, entries):
    """Generate a random IP and subnet mask, and display the problem."""
    global problem_ip, prefix_length, correct_values

    # Generate random IP and prefix length
    problem_ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    prefix_length = random.randint(24, 30)  # For simplicity, restrict to /24 to /30

    # Calculate the network
    network = ipaddress.ip_network(f"{problem_ip}/{prefix_length}", strict=False)

    # Set correct values
    correct_values = {
        "CLASS": get_ip_class(problem_ip),
        "DSNM": prefix_to_mask(network.network_address.max_prefixlen),
        "NSNM": prefix_to_mask(prefix_length),
        "# NETBITS": network.network_address.max_prefixlen,
        "# SUBNET BITS": prefix_length - network.network_address.max_prefixlen,
        "# HOST BITS": 32 - prefix_length,
        "NET ID": str(network.network_address),
        "1ST HOST": str(network[1]) if network.num_addresses > 2 else str(network.network_address),
        "BA": str(network.broadcast_address),
        "LAST HOST": str(network[-2]) if network.num_addresses > 2 else str(network.broadcast_address),
    }

    # Update the IP label
    ip_label.config(text=f"{problem_ip}/{prefix_length}")

    # Clear all input fields
    for entry in entries.values():
        entry.delete(0, tk.END)
        entry.config(bg="white")


def get_ip_class(ip):
    """Determine the class of an IP address."""
    first_octet = int(ip.split('.')[0])
    if first_octet <= 126:
        return "A"
    elif first_octet <= 191:
        return "B"
    elif first_octet <= 223:
        return "C"
    else:
        return "N/A"


def prefix_to_mask(prefix):
    """Convert prefix length to dotted decimal subnet mask."""
    mask = [0, 0, 0, 0]
    for i in range(prefix):
        mask[i // 8] += (1 << (7 - (i % 8)))
    return ".".join(map(str, mask))


def check_analysis_answers(entries):
    """Check the user's answers against the correct values."""
    all_correct = True
    for key, entry in entries.items():
        user_input = entry.get().strip()
        if user_input == str(correct_values[key]):
            entry.config(bg="lightgreen")  # Highlight correct answers in green
        else:
            entry.config(bg="red")  # Highlight incorrect answers in red
            all_correct = False

    if all_correct:
        messagebox.showinfo("Result", "All answers are correct!")
    else:
        messagebox.showinfo("Result", "Some answers are incorrect. Please check the highlighted fields.")
