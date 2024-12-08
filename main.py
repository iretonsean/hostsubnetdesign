import tkinter as tk
from tkinter import ttk, messagebox
import random

def generate_problem():
    mask_entry.delete(0, tk.END)  # Clear any previous answer
    mask_entry.config(fg="white")  # Reset the text color to white
    question_label.config(text="")  # Clear any previous question
    scenario = scenario_var.get()
    if scenario == "Host Design":
        generate_host_problem()
    elif scenario == "Subnet Design":
        generate_subnet_problem()

    # Show input box and button after generating the first problem
    mask_entry.pack(pady=5)
    check_button.pack(pady=10)


def generate_host_problem():
    global net_id, prefix, required_hosts, correct_mask
    if random.choice([True, False]):  # 50% chance to use an even octet
        prefix = random.choice([8, 16, 24])
    else:
        prefix = random.randint(8, 24)  # Random starting prefix
    net_id = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.0/{prefix}"
    required_hosts = random.randint(200, 4000)  # Random number of hosts

    # Determine new subnet mask using the methodology
    host_bits = 0
    while (2 ** host_bits - 2) < required_hosts:
        host_bits += 1
    new_prefix = 32 - host_bits

    if new_prefix < prefix or new_prefix > 32:  # Ensure a valid prefix
        generate_host_problem()
        return

    correct_mask = prefix_to_mask(new_prefix)

    question_label.config(
        text=f"Design a network scheme such that it supports at least {required_hosts} hosts per subnet using the Net ID of {net_id}. What's the new subnet mask?"
    )


def generate_subnet_problem():
    global net_id, prefix, required_subnets, correct_mask
    if random.choice([True, False]):  # 50% chance to use an even octet
        prefix = random.choice([8, 16, 24])
    else:
        prefix = random.randint(8, 24)  # Random starting prefix
    net_id = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.0/{prefix}"
    required_subnets = random.randint(16, 20000)  # Random number of subnets

    # Determine new subnet mask using the methodology
    subnet_bits = 0
    while (2 ** subnet_bits) < required_subnets:
        subnet_bits += 1
    new_prefix = prefix + subnet_bits

    if new_prefix > 32:  # Ensure a valid prefix
        generate_subnet_problem()
        return

    correct_mask = prefix_to_mask(new_prefix)

    question_label.config(
        text=f"Design a network scheme such that it supports at least {required_subnets} subnets using the Net ID of {net_id}. What's the new subnet mask?"
    )


def prefix_to_mask(prefix):
    mask = [0, 0, 0, 0]
    for i in range(prefix):
        mask[i // 8] += (1 << (7 - (i % 8)))
    return ".".join(map(str, mask))


def reset_ui():
    """Reset the UI to its default state."""
    mask_entry.delete(0, tk.END)  # Clear the input field
    mask_entry.config(fg="black")  # Reset the text color to black
    question_label.config(text="")  # Clear the question
    scenario_var.set("Host Design")  # Reset the scenario selection to default


def check_answer():
    user_answer = mask_entry.get().strip()
    if not user_answer:  # Check if the input is empty
        messagebox.showerror("Error", "Please enter a subnet mask before submitting.")
        return
    if user_answer == correct_mask:
        messagebox.showinfo("Result", "You are correct!")
        mask_entry.config(fg="green")  # Set the text color to green for correct answers
    else:
        messagebox.showinfo(
            "Result",
            f"Sorry, you're incorrect. The correct answer is {correct_mask}. "
            f"Make sure you're using the methodology to determine the new subnet mask."
        )
        mask_entry.config(fg="red")  # Set the text color to red for incorrect answers


# Create the GUI
root = tk.Tk()
root.geometry("800x600")  # Set the window size
root.title("Subnetting Practice Tool")

# Create the tabs using ttk.Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Tab 1: Subnet Design Practice
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Subnet Design Practice")

# Add padding around the entire content in tab1
main_frame = tk.Frame(tab1, padx=20, pady=20)
main_frame.pack(fill="both", expand=True, anchor="n")

# Scenario selection in tab1
scenario_var = tk.StringVar(value="Host Design")
tk.Label(main_frame, text="Select Scenario:").pack(pady=5)
tk.Radiobutton(main_frame, text="Host Design", variable=scenario_var, value="Host Design").pack(pady=2)
tk.Radiobutton(main_frame, text="Subnet Design", variable=scenario_var, value="Subnet Design").pack(pady=2)

# Generate problem button in tab1
generate_button = tk.Button(main_frame, text="Generate Problem", command=generate_problem)
generate_button.pack(pady=10)

# Question label in tab1
question_label = tk.Label(main_frame, text="", wraplength=550, justify="left")
question_label.pack(pady=10)

# Input for subnet mask in tab1
mask_entry = tk.Entry(main_frame, fg="white", bg="black")  # Set initial font color to white
mask_entry.pack_forget()  # Initially hidden

# Bind the Return key (main keyboard) and Enter key (external/numpad) to check_answer
root.bind('<Return>', lambda event: check_answer())
root.bind('<KP_Enter>', lambda event: check_answer())

# Check answer button in tab1
check_button = tk.Button(main_frame, text="Check Answer", command=check_answer)
check_button.pack_forget()  # Initially hidden

# Tab 2: Subnet Analysis Practice (Empty for now)
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Subnet Analysis Practice")

# Placeholder content for Tab 2
tk.Label(tab2, text="Subnet Analysis Practice Content Goes Here", font=("Arial", 14)).pack(pady=20)

# Start the GUI
root.mainloop()
