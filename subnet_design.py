import tkinter as tk
from tkinter import messagebox
import random


def SubnetDesignTab(parent):
    """Set up the Subnet Design Practice tab."""
    main_frame = tk.Frame(parent, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True, anchor="n")

    # Scenario selection
    scenario_var = tk.StringVar(value="Host Design")
    tk.Label(main_frame, text="Select Scenario:").pack(pady=5)
    tk.Radiobutton(main_frame, text="Host Design", variable=scenario_var, value="Host Design").pack(pady=2)
    tk.Radiobutton(main_frame, text="Subnet Design", variable=scenario_var, value="Subnet Design").pack(pady=2)

    # Question label
    question_label = tk.Label(main_frame, text="", wraplength=550, justify="left")
    question_label.pack(pady=10)

    # Input for subnet mask
    mask_entry = tk.Entry(main_frame, fg="white", bg="black")
    mask_entry.pack_forget()

    # Bind Return and Enter keys for submitting the answer
    mask_entry.bind('<Return>', lambda event: check_answer(mask_entry, question_label))
    mask_entry.bind('<KP_Enter>', lambda event: check_answer(mask_entry, question_label))

    # Check answer button
    check_button = tk.Button(main_frame, text="Check Answer", command=lambda: check_answer(mask_entry, question_label))
    check_button.pack_forget()

    # Generate problem button
    generate_button = tk.Button(
        main_frame,
        text="Generate Problem",
        command=lambda: generate_problem(question_label, mask_entry, check_button, scenario_var),
    )
    generate_button.pack(pady=10)


def generate_problem(question_label, mask_entry, check_button, scenario_var):
    """Generate a subnetting problem."""
    scenario = scenario_var.get()

    # Reset the input box and button visibility
    mask_entry.delete(0, tk.END)
    mask_entry.pack(pady=5)
    mask_entry.config(fg="white", bg="black")

    check_button.pack(pady=10)

    # Generate a random question based on the scenario
    global correct_mask  # Store the dynamically calculated mask
    prefix = generate_random_prefix()  # Always generates /8, /16, or /24
    first_octet = random.randint(1, 223)
    second_octet = random.randint(0, 255)
    third_octet = random.randint(0, 255)

    # Zero out host octets based on the prefix
    if prefix == 8:
        net_id = f"{first_octet}.0.0.0/{prefix}"
    elif prefix == 16:
        net_id = f"{first_octet}.{second_octet}.0.0/{prefix}"
    elif prefix == 24:
        net_id = f"{first_octet}.{second_octet}.{third_octet}.0/{prefix}"

    if scenario == "Host Design":
        # Generate more challenging host requirements
        required_hosts = random.randint(1000, 17000)

        # Calculate the correct subnet mask
        host_bits = 0
        while (2 ** host_bits - 2) < required_hosts:
            host_bits += 1
        new_prefix = 32 - host_bits
        if new_prefix < prefix or new_prefix > 32:
            generate_problem(question_label, mask_entry, check_button, scenario_var)
            return
        correct_mask = prefix_to_mask(new_prefix)

        question_label.config(
            text=f"Design a network scheme such that it supports at least {required_hosts} hosts per subnet using the Net ID of {net_id}. "
                 f"What's the new subnet mask?"
        )

    elif scenario == "Subnet Design":
        # Generate more challenging subnet requirements
        required_subnets = random.randint(500, 17000)

        # Calculate the correct subnet mask
        subnet_bits = 0
        while (2 ** subnet_bits) < required_subnets:
            subnet_bits += 1
        new_prefix = prefix + subnet_bits
        if new_prefix > 32:
            generate_problem(question_label, mask_entry, check_button, scenario_var)
            return
        correct_mask = prefix_to_mask(new_prefix)

        question_label.config(
            text=f"Design a network scheme such that it supports at least {required_subnets} subnets using the Net ID of {net_id}. "
                 f"What's the new subnet mask?"
        )


def check_answer(mask_entry, question_label):
    """Check the answer provided by the user."""
    user_answer = mask_entry.get().strip()
    if not user_answer:
        messagebox.showerror("Error", "Please enter a subnet mask before submitting.")
        return

    # Validate the user's answer against the dynamically calculated correct mask
    if user_answer == correct_mask:
        messagebox.showinfo("Result", "You are correct!")
        mask_entry.config(fg="green")
    else:
        messagebox.showinfo("Result", f"Sorry, incorrect. The correct answer is {correct_mask}.")
        mask_entry.config(fg="red")


def prefix_to_mask(prefix):
    """Convert CIDR prefix to dotted decimal subnet mask."""
    mask = [0, 0, 0, 0]
    for i in range(prefix):
        mask[i // 8] += (1 << (7 - (i % 8)))
    return ".".join(map(str, mask))


def generate_random_prefix():
    """Generate a random prefix with 100% chance for even octet boundaries."""
    return random.choice([8, 16, 24])
