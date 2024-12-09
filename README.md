
# Subnet Design and Analysis Practice Tool

This is a Python-based GUI program designed to help users practice subnetting through two primary modes: 
- **Subnet Design Practice** 
- **Subnet Analysis Practice**.

The tool dynamically generates subnetting problems and validates the user's answers. It is designed for educational purposes and supports both even and uneven octet boundaries.

---

## Features

### Subnet Design Practice
- Choose between **Host Design** or **Subnet Design** scenarios.
- Randomly generates a problem based on the selected scenario:
  - **Host Design**: Calculates the new subnet mask based on the required number of hosts per subnet.
  - **Subnet Design**: Calculates the new subnet mask based on the required number of subnets.
- Allows users to input a subnet mask and validates the answer.
- Highlights the answer in green (correct) or red (incorrect) and provides feedback.

### Subnet Analysis Practice
- Generates a random IP address with a given prefix length.
- Displays a table with fields to analyze the subnet (e.g., Net ID, Broadcast Address, Subnet Bits).
- Dynamically validates answers and provides feedback.

---

## Installation

1. **Clone or Download the Repository**:
   ```bash
   git clone <repository_url>
   cd subnetting-practice-tool
   ```

2. **Install Dependencies**:
   Ensure you have Python 3 installed. Install required libraries using pip:
   ```bash
   pip install tkinter ipcalc
   ```

3. **Run the Program**:
   ```bash
   python main.py
   ```

---

## How to Use

### Subnet Design Practice
1. Select a scenario: **Host Design** or **Subnet Design**.
2. Click **Generate Problem** to create a new problem.
3. Input your subnet mask answer and press **Check Answer** to validate.
4. The program will provide feedback and highlight your input.

### Subnet Analysis Practice
1. A random IP address and prefix length will be generated upon opening the tab.
2. Fill out the fields in the table (e.g., Class, Default Subnet Mask, Net ID).
3. Click **Check Answers** to validate your inputs.
4. The program will highlight correct and incorrect fields.

---

## Requirements
- Python 3.x
- Libraries: `tkinter`, `ipcalc`

---

## License
This project is open-source and available for educational purposes.
