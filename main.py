import tkinter as tk
from tkinter import ttk
from subnet_design import SubnetDesignTab
from subnet_analysis import SubnetAnalysisTab

# Create the main GUI
root = tk.Tk()
root.geometry("800x600")
root.title("Subnetting Practice Tool")

# Create tabs using ttk.Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Add Subnet Design Practice Tab
design_tab = ttk.Frame(notebook)
notebook.add(design_tab, text="Subnet Design Practice")
SubnetDesignTab(design_tab)

# Add Subnet Analysis Practice Tab
analysis_tab = ttk.Frame(notebook)
notebook.add(analysis_tab, text="Subnet Analysis Practice")
SubnetAnalysisTab(analysis_tab)

# Start the GUI
root.mainloop()
