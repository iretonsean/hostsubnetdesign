import tkinter as tk
from tkinter import messagebox
import random


def generate_problem():
    mask_entry.delete(0, tk.END)  # Clear any previous answer
    question_label.config(text="")  # Clear any previous question
    scenario = scenario_var.get()
    if scenario == "Host Design":
        generate_host_problem()
    elif scenario == "Subnet Design":
        generate_subnet_problem()


def generate_host_problem():
    global net_id, prefix, required_hosts, correct_mask
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
    question_label.config(text="")  # Clear the question
    scenario_var.set("Host Design")  # Reset the scenario selection to default


def check_answer():
    user_answer = mask_entry.get()
    if user_answer == correct_mask:
        messagebox.showinfo("Result", "You are correct!")
    else:
        messagebox.showinfo(
            "Result",
            f"Sorry, you're incorrect. The correct answer is {correct_mask}. "
            f"Make sure you're using the methodology to determine the new subnet mask."
        )
    reset_ui()  # Reset the UI after the user closes the result window


# Create the GUI
root = tk.Tk()
root.geometry("600x400")
root.title("Subnetting Practice Tool")

# Add padding around the entire content
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="none", expand=False, anchor="n", pady=20)

# Scenario selection
scenario_var = tk.StringVar(value="Host Design")
tk.Label(root, text="Select Scenario:").pack()
tk.Radiobutton(root, text="Host Design", variable=scenario_var, value="Host Design").pack()
tk.Radiobutton(root, text="Subnet Design", variable=scenario_var, value="Subnet Design").pack()

# Generate problem button
generate_button = tk.Button(root, text="Generate Problem", command=generate_problem)
generate_button.pack()

# Question label
question_label = tk.Label(root, text="", wraplength=400, justify="left")
question_label.pack()

# Input for subnet mask
tk.Label(root, text="Enter the new subnet mask:").pack()
mask_entry = tk.Entry(root)
mask_entry.pack()

# Check answer button
check_button = tk.Button(root, text="Check Answer", command=check_answer)
check_button.pack()

# Start the GUI
root.mainloop()
