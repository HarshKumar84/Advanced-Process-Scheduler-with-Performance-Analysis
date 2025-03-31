import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Scheduler")
        self.root.geometry("900x800")  # Increased window height
        self.root.configure(bg="white")

        # Main container frame
        main_frame = tk.Frame(root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top section - Title and input
        top_frame = tk.Frame(main_frame, bg="white")
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        title_label = tk.Label(
            top_frame,
            text="Process Scheduler",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="black"
        )
        title_label.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(main_frame, bg="black")
        input_frame.pack(pady=10)

        headers = ["Process", "Arrival Time", "Burst Time", "Priority"]
        for i, header in enumerate(headers):
            tk.Label(input_frame, text=header, font=("Arial", 12, "bold"), fg="white", bg="black").grid(row=0, column=i, padx=5, pady=5)

        self.entries = []
        for i in range(5):  # For 5 processes
            tk.Label(input_frame, text=f"P{i+1}", font=("Arial", 12, "bold"), fg="white", bg="black").grid(row=i+1, column=0, padx=5, pady=5)
            row_entries = []
            for j in range(3):  # Arrival, Burst, Priority
                entry = tk.Entry(input_frame, width=10)
                entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

        tk.Label(input_frame, text="Algorithm:", font=("Arial", 12, "bold"), fg="white", bg="black").grid(row=6, column=0, pady=10)
        self.algo_var = ttk.Combobox(input_frame, values=["FCFS", "SJF", "Priority", "Round Robin"], width=10)
        self.algo_var.grid(row=6, column=1)
        self.algo_var.current(0)

        tk.Label(input_frame, text="Time Quantum:", font=("Arial", 12, "bold"), fg="white", bg="black").grid(row=6, column=2, pady=10)
        self.time_quantum_entry = tk.Entry(input_frame, width=5)
        self.time_quantum_entry.grid(row=6, column=3)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(pady=10)

        run_button = tk.Button(button_frame, text="Run Scheduler", command=self.run_scheduler, font=("Arial", 12, "bold"), bg="green", fg="white")
        run_button.grid(row=0, column=0, padx=10)

        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_entries, font=("Arial", 12, "bold"), bg="red", fg="white")
        clear_button.grid(row=0, column=1, padx=10)

        # Output and metrics frame
        output_frame = tk.Frame(main_frame, bg="white")
        output_frame.pack(fill=tk.X, padx=10, pady=10)

        self.output_text = tk.Text(output_frame, height=4, width=80, bg="black", fg="lime", font=("Arial", 12))
        self.output_text.pack()

        # Metrics frame
        self.metrics_frame = tk.Frame(main_frame, bg="white")
        self.metrics_frame.pack(fill=tk.X, padx=10, pady=10)

        # Gantt chart frame - placed lower in the window
        self.chart_frame = tk.Frame(main_frame, bg="white")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add some padding at the bottom
        tk.Frame(main_frame, height=10, bg="white").pack()

    def clear_entries(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def run_scheduler(self):
        algorithm = self.algo_var.get()
        time_quantum = self.time_quantum_entry.get()
        
        processes = []
        for i, row in enumerate(self.entries):
            arrival = int(row[0].get() or 0)
            burst = int(row[1].get() or 0)
            priority = int(row[2].get() or 0)
            processes.append({"pid": f"P{i+1}", "arrival": arrival, "burst": burst, "priority": priority, "remaining": burst})

        if algorithm == "FCFS":
            schedule, waiting_times, turnaround_times = self.fcfs(processes)
        elif algorithm == "SJF":
            schedule, waiting_times, turnaround_times = self.sjf(processes)
        elif algorithm == "Priority":
            schedule, waiting_times, turnaround_times = self.priority_scheduling(processes)
        elif algorithm == "Round Robin":
            if not time_quantum.isdigit():
                self.output_text.insert(tk.END, "Invalid Time Quantum\n")
                return
            schedule, waiting_times, turnaround_times = self.round_robin(processes, int(time_quantum))
        else:
            self.output_text.insert(tk.END, "Invalid Algorithm Selected\n")
            return

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Scheduling Result:\n")
        
        # Calculate metrics
        total_burst = sum(p["burst"] for p in processes)
        total_time = sum(item[1] for item in schedule)
        cpu_utilization = (total_burst / total_time) * 100 if total_time > 0 else 0
        
        avg_waiting = sum(waiting_times.values()) / len(waiting_times)
        avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)
        
        # Display metrics
        self.display_metrics(avg_waiting, avg_turnaround, cpu_utilization)
        
        self.draw_gantt_chart(schedule)

    def display_metrics(self, avg_waiting, avg_turnaround, cpu_utilization):
        # Clear previous metrics
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
            
        # Create labels for metrics
        metrics_title = tk.Label(self.metrics_frame, text="Performance Metrics", font=("Arial", 14, "bold"), bg="white")
        metrics_title.pack()
        
        metrics_grid = tk.Frame(self.metrics_frame, bg="white")
        metrics_grid.pack(pady=5)
        
        tk.Label(metrics_grid, text="Average Waiting Time:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="e", padx=5)
        tk.Label(metrics_grid, text=f"{avg_waiting:.2f}", font=("Arial", 12), bg="white").grid(row=0, column=1, sticky="w")
        
        tk.Label(metrics_grid, text="Average Turnaround Time:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="e", padx=5)
        tk.Label(metrics_grid, text=f"{avg_turnaround:.2f}", font=("Arial", 12), bg="white").grid(row=1, column=1, sticky="w")
        
        tk.Label(metrics_grid, text="CPU Utilization:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="e", padx=5)
        tk.Label(metrics_grid, text=f"{cpu_utilization:.2f}%", font=("Arial", 12), bg="white").grid(row=2, column=1, sticky="w")

    def draw_gantt_chart(self, schedule):
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # Create a larger figure for better visibility
        fig, ax = plt.subplots(figsize=(10, 3))
        
        # Calculate chart dimensions based on schedule
        total_time = sum(item[1] for item in schedule)
        bar_height = 0.6
        
        # Create Gantt chart
        start_time = 0
        for i, (process, duration) in enumerate(schedule):
            ax.broken_barh([(start_time, duration)], (i, bar_height), 
                          facecolors=('tab:blue'), edgecolor=('black'), linewidth=1)
            # Add process label in the middle of the bar
            ax.text(start_time + duration/2, i + bar_height/2, process, 
                   ha='center', va='center', color='white', fontweight='bold')
            start_time += duration
        
        # Format the chart
        ax.set_xlim(0, total_time)
        ax.set_ylim(0, len(schedule))
        ax.set_xlabel('Time Units')
        ax.set_ylabel('Processes')
        ax.set_title('Gantt Chart - Process Execution Timeline')
        ax.set_yticks([i + bar_height/2 for i in range(len(schedule))])
        ax.set_yticklabels([f'Step {i+1}' for i in range(len(schedule))])
        ax.grid(True, which='both', axis='x', linestyle='--', alpha=0.7)
        
        # Embed the chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def fcfs(self, processes):
        processes_sorted = sorted(processes, key=lambda x: x["arrival"])
        
        schedule = []
        waiting_times = {}
        turnaround_times = {}
        
        current_time = 0
        for p in processes_sorted:
            if current_time < p["arrival"]:
                current_time = p["arrival"]
            
            waiting_times[p["pid"]] = current_time - p["arrival"]
            schedule.append((p["pid"], p["burst"]))
            current_time += p["burst"]
            turnaround_times[p["pid"]] = current_time - p["arrival"]
            
        return schedule, waiting_times, turnaround_times

    def sjf(self, processes):
        processes_sorted = sorted(processes, key=lambda x: x["arrival"])
        
        schedule = []
        waiting_times = {}
        turnaround_times = {}
        
        current_time = 0
        ready_queue = []
        completed = 0
        n = len(processes_sorted)
        
        while completed != n:
            for p in processes_sorted:
                if p["arrival"] <= current_time and "remaining" in p and p["remaining"] > 0 and p not in ready_queue:
                    ready_queue.append(p)
            
            if not ready_queue:
                current_time += 1
                continue
                
            ready_queue.sort(key=lambda x: x["burst"])
            
            current_process = ready_queue.pop(0)
            burst = current_process["burst"]
            
            schedule.append((current_process["pid"], burst))
            waiting_times[current_process["pid"]] = current_time - current_process["arrival"]
            current_time += burst
            turnaround_times[current_process["pid"]] = current_time - current_process["arrival"]
            completed += 1
            
        return schedule, waiting_times, turnaround_times

    def priority_scheduling(self, processes):
        processes_sorted = sorted(processes, key=lambda x: x["arrival"])
        
        schedule = []
        waiting_times = {}
        turnaround_times = {}
        
        current_time = 0
        ready_queue = []
        completed = 0
        n = len(processes_sorted)
        
        while completed != n:
            for p in processes_sorted:
                if p["arrival"] <= current_time and "remaining" in p and p["remaining"] > 0 and p not in ready_queue:
                    ready_queue.append(p)
            
            if not ready_queue:
                current_time += 1
                continue
                
            ready_queue.sort(key=lambda x: x["priority"])
            
            current_process = ready_queue.pop(0)
            burst = current_process["burst"]
            
            schedule.append((current_process["pid"], burst))
            waiting_times[current_process["pid"]] = current_time - current_process["arrival"]
            current_time += burst
            turnaround_times[current_process["pid"]] = current_time - current_process["arrival"]
            completed += 1
            
        return schedule, waiting_times, turnaround_times

    def round_robin(self, processes, quantum):
        processes_sorted = sorted(processes, key=lambda x: x["arrival"])
        
        schedule = []
        waiting_times = {p["pid"]: 0 for p in processes_sorted}
        turnaround_times = {}
        
        current_time = 0
        ready_queue = []
        remaining_processes = len(processes_sorted)
        
        for p in processes_sorted:
            p["remaining"] = p["burst"]
        
        while remaining_processes > 0:
            for p in processes_sorted:
                if p["arrival"] <= current_time and p["remaining"] > 0 and p not in ready_queue:
                    ready_queue.append(p)
            
            if not ready_queue:
                current_time += 1
                continue
                
            current_process = ready_queue.pop(0)
            exec_time = min(quantum, current_process["remaining"])
            
            schedule.append((current_process["pid"], exec_time))
            current_time += exec_time
            current_process["remaining"] -= exec_time
            
            for p in ready_queue:
                waiting_times[p["pid"]] += exec_time
                
            if current_process["remaining"] > 0:
                ready_queue.append(current_process)
            else:
                remaining_processes -= 1
                turnaround_times[current_process["pid"]] = current_time - current_process["arrival"]
        
        for p in processes_sorted:
            waiting_times[p["pid"]] = turnaround_times[p["pid"]] - p["burst"]
            
        return schedule, waiting_times, turnaround_times


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()