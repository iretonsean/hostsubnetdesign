import tkinter as tk
from tkinter import messagebox
import random
import ipcalc


def SubnetAnalysisTab(parent):
    """Set up the Subnet Analysis Practice tab."""
    analysis_frame = tk.Frame(parent, padx=20, pady=20)
    analysis_frame.pack(fill="both", expand=True, anchor="n")

    # Table labels
    labels = ["IP", "CLASS", "DSNM", "NSNM", "# NETBITS", "# SUBNET BITS", "# HOST BITS", "NET ID", "1ST HOST", "BA", "LAST HOST"]
    analysis_entries = {}
    global problem_ip, prefix_length

    # Generate table with labels and inputs
    for row, label in enumerate(labels):
        # Add static label
        tk.Label(analysis_frame, text=label, bg="gray", fg="black", width=15, anchor="w").grid(row=row, column=0, sticky="nsew", padx=1, pady=1)

        # IP will be a label, not editable
        if label == "IP":
            problem_ip_label = tk.Label(analysis_frame, text="", bg="gray20", fg="white", width=30, anchor="w")
            problem_ip_label.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
        else:
            # Add input box for other fields
            entry = tk.Entry(analysis_frame, bg="white", fg="black", insertbackground="black", width=30)
            entry.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
            analysis_entries[label] = entry

    # Buttons below the table
    button_frame = tk.Frame(analysis_frame)
    button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

    # Generate and Check Buttons
    tk.Button(button_frame, text="Generate Problem", command=lambda: generate_analysis_problem(problem_ip_label, analysis_entries)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Check Answers", command=lambda: check_analysis_answers(analysis_entries)).pack(side="left", padx=5)

    # Auto-generate a problem when the tab is loaded
    generate_analysis_problem(problem_ip_label, analysis_entries)


def generate_analysis_problem(ip_label, entries):
    """Generate a random IP and subnet mask, and display the problem."""
    global problem_ip, prefix_length

    # Generate random IP within valid Class A, B, or C range
    first_octet = random.randint(1, 223)  # Restrict first octet to valid range
    problem_ip = f"{first_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

    # 50% chance for even octet boundary
    if random.choice([True, False]):
        prefix_length = random.choice([8, 16, 24])
    else:
        prefix_length = random.randint(8, 30)  # Wider range, including below /20

    # Update the IP label
    ip_label.config(text=f"{problem_ip}/{prefix_length}")

    # Clear all input fields
    for entry in entries.values():
        entry.delete(0, tk.END)
        entry.config(bg="white")


def check_analysis_answers(entries):
    """Dynamically check the user's answers using ipcalc."""
    # Check if all fields are filled
    for key, entry in entries.items():
        if not entry.get().strip():  # If the field is empty
            messagebox.showerror("Error", f"Please fill out all fields before checking answers. Missing: {key}")
            return

    all_correct = True

    # Parse the IP and prefix length
    network = ipcalc.Network(f"{problem_ip}/{prefix_length}")

    # Dynamically calculate expected values using ipcalc
    calculated_values = {
        "CLASS": get_ip_class(problem_ip),
        "DSNM": prefix_to_mask(get_default_netbits(problem_ip)),
        "NSNM": prefix_to_mask(prefix_length),
        "# NETBITS": get_default_netbits(problem_ip),
        "# SUBNET BITS": max(0, prefix_length - get_default_netbits(problem_ip)),
        "# HOST BITS": 32 - prefix_length,
        "NET ID": str(network.network()),
        "1ST HOST": str(network.host_first()),
        "BA": str(network.broadcast()),
        "LAST HOST": str(network.host_last()),
    }

    # Validate user input against dynamically calculated values
    for key, entry in entries.items():
        user_input = entry.get().strip()
        if user_input == str(calculated_values[key]):
            entry.config(bg="lightgreen")  # Highlight correct answers in green
        else:
            entry.config(bg="red")  # Highlight incorrect answers in red
            all_correct = False

    # Provide feedback based on correctness
    if all_correct:
        messagebox.showinfo("Result", "All answers are correct!")
    else:
        messagebox.showinfo("Result", "Some answers are incorrect. Please check the highlighted fields.")


def prefix_to_mask(prefix):
    """Convert prefix length to dotted decimal subnet mask."""
    mask = [0, 0, 0, 0]
    for i in range(prefix):
        mask[i // 8] += (1 << (7 - (i % 8)))
    return ".".join(map(str, mask))


def get_ip_class(ip):
    """Determine the class of an IP address."""
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        return "A"
    elif 128 <= first_octet <= 191:
        return "B"
    elif 192 <= first_octet <= 223:
        return "C"
    else:
        return "N/A"


def get_default_netbits(ip):
    """Get the default subnet bits for an IP address based on its class."""
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        return 8  # Class A
    elif 128 <= first_octet <= 191:
        return 16  # Class B
    elif 192 <= first_octet <= 223:
        return 24  # Class C
    else:
        return 0
