# Traffic Data Analysis and Visualization System 🚦📊

A Python based software development project that processes, analyzes, and visualizes urban traffic datasets through interactive command line input and graphical histograms using Tkinter.

---

## 📌 Introduction

This project was developed as part of the Python Software Development module during my first year at the University of Westminster. It allows users to:

- Validate user input dates
- Load corresponding traffic CSV files
- Process key traffic insights
- Visualize hourly vehicle data on two junctions using a Tkinter based histogram
- Save results for multiple datasets in a single session

The program simulates a real world traffic data processor, allowing multi-date input and presenting detailed statistical outcomes, making it both educational and practical.

---

## 🚀 Features

- 🔍 **Date Input Validation** (with range and format checking)
- 📥 **CSV Traffic Data Processing**
  - Vehicle counts (total, trucks, electric, 2-wheelers)
  - Speeding, turning behavior, and junction specific stats
  - Rain hour detection and peak hour analysis
- 📈 **Tkinter Histogram Visualizer** (Elm Avenue vs Hanley Highway)
- 📝 **Results Saved** to `results.txt`
- 🔄 **Multiple Dataset Handling**
- ❌ **Robust Error Handling** (e.g., invalid dates, missing files)

---

## 🧰 Technologies Used

- Python 3.12.3
- Tkinter (GUI)
- CSV Module
- File I/O
- Exception Handling
- Object-Oriented Programming

---

## 🛠️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/traffic-data-analysis.git
   cd traffic-data-analysis
   
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate    # Windows
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Ensure your CSV files are named in the format:
   ```bash
   traffic_dataDDMMYYYY.csv

---

## ▶️ How to Run

  ```bash
  python main.py
  ```

You will be prompted to enter a date (DD MM YYYY), and if a matching CSV file is found, the program will analyze the data and show insights. A graphical histogram will be displayed afterward.

---

## 🖼️ Screenshots

📌 Histogram Example
  - https://github.com/dulan-nimnaka/traffic-data-analysis/blob/main/screenshots/histogram_sample1.png
  - https://github.com/dulan-nimnaka/traffic-data-analysis/blob/main/screenshots/histogram_sample2.jpeg
  - https://github.com/dulan-nimnaka/traffic-data-analysis/blob/main/screenshots/histogram_sample3.jpeg

📌 CLI Input Example


---

## 📁 Project Structure

  ```bash
  traffic-data-analysis/
  │
  ├── main.py                                   # Main application script
  ├── Test_results_for_Task_ABCDE.pdf           # Test cases
  ├── results.txt                               # Output file (generated after run)
  ├── /screenshots                              # Screenshots folder (optional)
  └── README.md
  ```


---

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.











   

