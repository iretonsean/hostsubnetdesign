import tkinter as tk
from tkinter import ttk
from subnet_design import SubnetDesignTab
from subnet_analysis import SubnetAnalysisTab

# Create the main window
root = tk.Tk()
root.geometry("800x600")
root.title("Subnetting Practice Tool")

# Create a tabbed interface
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Subnet Design Tab
design_tab = ttk.Frame(notebook)
notebook.add(design_tab, text="Subnet Design Practice")
SubnetDesignTab(design_tab)

# Subnet Analysis Tab
analysis_tab = ttk.Frame(notebook)
notebook.add(analysis_tab, text="Subnet Analysis Practice")
SubnetAnalysisTab(analysis_tab)

# Start the GUI
root.mainloop()
