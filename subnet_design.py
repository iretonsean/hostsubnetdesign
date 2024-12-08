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

    # Generate problem button
    generate_button = tk.Button(main_frame, text="Generate Problem", command=lambda: generate_problem(main_frame, scenario_var))
    generate_button.pack(pady=10)

    # Question label
    question_label = tk.Label(main_frame, text="", wraplength=550, justify="left")
    question_label.pack(pady=10)

    # Input for subnet mask
    mask_entry = tk.Entry(main_frame, fg="white", bg="black")
    mask_entry.pack_forget()

    # Check answer button
    check_button = tk.Button(main_frame, text="Check Answer", command=lambda: check_answer(mask_entry, question_label))
    check_button.pack_forget()

    # Bind Enter key for checking answers
    parent.bind('<Return>', lambda event: check_answer(mask_entry, question_label))
    parent.bind('<KP_Enter>', lambda event: check_answer(mask_entry, question_label))

    # Store references for later access
    parent.mask_entry = mask_entry
    parent.check_button = check_button
    parent.question_label = question_label


def generate_problem(frame, scenario_var):
    """Generate a subnetting problem."""
    scenario = scenario_var.get()
    # Logic for problem generation based on scenario
    # Example: Randomly set a question to question_label
    frame.question_label.config(text="Example question text")


def check_answer(mask_entry, question_label):
    """Check the answer provided by the user."""
    user_answer = mask_entry.get()
    if not user_answer:
        messagebox.showerror("Error", "Please enter a subnet mask before submitting.")
        return
    # Example answer checking logic
    correct_answer = "255.255.255.0"  # Example
    if user_answer == correct_answer:
        messagebox.showinfo("Result", "You are correct!")
        mask_entry.config(fg="green")
    else:
        messagebox.showinfo("Result", "Sorry, incorrect.")
        mask_entry.config(fg="red")
