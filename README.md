# Process Scheduling Application

This project is a Process Scheduling application built using Python's Tkinter library for the graphical user interface (GUI) and Matplotlib for visualizing scheduling results. The application allows users to input process details and select scheduling algorithms to simulate process scheduling.

## Features

- Supports multiple scheduling algorithms:
  - First-Come, First-Served (FCFS)
  - Shortest Job First (SJF)
  - Priority Scheduling
  - Round Robin
- Displays scheduling results and performance metrics, including average waiting time, average turnaround time, and CPU utilization.
- Visualizes the scheduling process with a Gantt chart.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/process-scheduling.git
   ```
2. Navigate to the project directory:
   ```
   cd process-scheduling
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/process-scheduler.py
   ```
2. Enter the process details (Process Name, Arrival Time, Burst Time, Priority) in the provided fields.
3. Select the desired scheduling algorithm from the dropdown menu.
4. If using Round Robin, specify the time quantum.
5. Click on "Run Scheduler" to see the scheduling results and Gantt chart.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.