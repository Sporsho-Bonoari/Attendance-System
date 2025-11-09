import tkinter as tk
from tkinter import ttk, messagebox
import os
import csv
from datetime import datetime
import glob

class AttendanceViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Attendance Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.all_records = []
        self.filtered_records = []
        
        # Create UI
        self.create_widgets()
        self.load_all_attendance()
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🎓 Face Recognition Attendance System", 
                              font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(pady=20)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg="#ecf0f1", height=100)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Search Section
        search_label = tk.Label(control_frame, text="🔍 Search Name:", 
                               font=("Arial", 11), bg="#ecf0f1")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_records)
        search_entry = tk.Entry(control_frame, textvariable=self.search_var, 
                               font=("Arial", 11), width=20)
        search_entry.grid(row=0, column=1, padx=5, pady=10)
        
        # Date Filter Section
        date_label = tk.Label(control_frame, text="📅 Filter Date:", 
                             font=("Arial", 11), bg="#ecf0f1")
        date_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        self.date_var = tk.StringVar()
        self.date_var.set("All Dates")
        self.date_combo = ttk.Combobox(control_frame, textvariable=self.date_var, 
                                       font=("Arial", 10), width=15, state="readonly")
        self.date_combo.grid(row=0, column=3, padx=5, pady=10)
        self.date_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_records())
        
        # Buttons
        refresh_btn = tk.Button(control_frame, text="🔄 Refresh", 
                               font=("Arial", 10, "bold"), bg="#3498db", fg="white",
                               command=self.load_all_attendance, padx=15, pady=5,
                               relief=tk.FLAT, cursor="hand2")
        refresh_btn.grid(row=0, column=4, padx=10, pady=10)
        
        clear_btn = tk.Button(control_frame, text="✖ Clear Filter", 
                             font=("Arial", 10, "bold"), bg="#e74c3c", fg="white",
                             command=self.clear_filters, padx=15, pady=5,
                             relief=tk.FLAT, cursor="hand2")
        clear_btn.grid(row=0, column=5, padx=10, pady=10)
        
        export_btn = tk.Button(control_frame, text="💾 Export CSV", 
                              font=("Arial", 10, "bold"), bg="#27ae60", fg="white",
                              command=self.export_to_csv, padx=15, pady=5,
                              relief=tk.FLAT, cursor="hand2")
        export_btn.grid(row=0, column=6, padx=10, pady=10)
        
        # Statistics Frame
        stats_frame = tk.Frame(self.root, bg="#ecf0f1", height=60)
        stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.stats_label = tk.Label(stats_frame, text="", 
                                    font=("Arial", 11, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.stats_label.pack(pady=10)
        
        # Table Frame
        table_frame = tk.Frame(self.root, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview (Table)
        self.tree = ttk.Treeview(table_frame, columns=("No", "Name", "Date", "Time"), 
                                show="headings", height=15,
                                yscrollcommand=v_scrollbar.set,
                                xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Define columns
        self.tree.heading("No", text="#")
        self.tree.heading("Name", text="👤 Name")
        self.tree.heading("Date", text="📅 Date")
        self.tree.heading("Time", text="⏰ Time")
        
        self.tree.column("No", width=50, anchor="center")
        self.tree.column("Name", width=300, anchor="w")
        self.tree.column("Date", width=200, anchor="center")
        self.tree.column("Time", width=150, anchor="center")
        
        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", 
                       rowheight=30, fieldbackground="white", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), 
                       background="#34495e", foreground="white")
        style.map("Treeview", background=[("selected", "#3498db")])
        
        # Pack scrollbars and tree
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#2c3e50", height=40)
        footer_frame.pack(fill=tk.X, padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(footer_frame, 
                               text="Developed with ❤️ | Face Recognition Attendance System", 
                               font=("Arial", 9), fg="white", bg="#2c3e50")
        footer_label.pack(pady=10)
    
    def load_all_attendance(self):
        """Load all attendance records from CSV files"""
        self.all_records = []
        dates = ["All Dates"]
        
        # Check if Attendance folder exists
        if not os.path.exists('Attendance'):
            messagebox.showwarning("Warning", "No attendance records found!\n\nAttendance folder doesn't exist.")
            self.update_statistics()
            return
        
        # Get all CSV files
        csv_files = glob.glob('Attendance/Attendance_*.csv')
        
        if not csv_files:
            messagebox.showinfo("Info", "No attendance records found!\n\nPlease take some attendance first using test.py")
            self.update_statistics()
            return
        
        # Load each CSV file
        for csv_file in csv_files:
            try:
                # Extract date from filename
                filename = os.path.basename(csv_file)
                date = filename.replace("Attendance_", "").replace(".csv", "")
                dates.append(date)
                
                # Read CSV
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header
                    for row in reader:
                        if len(row) >= 2:
                            self.all_records.append({
                                'name': row[0],
                                'date': date,
                                'time': row[1]
                            })
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
        
        # Update date combobox
        self.date_combo['values'] = sorted(dates, reverse=True)
        
        # Sort records by date and time (newest first)
        self.all_records.sort(key=lambda x: (x['date'], x['time']), reverse=True)
        
        # Display all records
        self.filtered_records = self.all_records.copy()
        self.display_records()
        self.update_statistics()
    
    def filter_records(self, *args):
        """Filter records based on search and date filter"""
        search_text = self.search_var.get().lower()
        selected_date = self.date_var.get()
        
        self.filtered_records = []
        
        for record in self.all_records:
            # Check name filter
            if search_text and search_text not in record['name'].lower():
                continue
            
            # Check date filter
            if selected_date != "All Dates" and record['date'] != selected_date:
                continue
            
            self.filtered_records.append(record)
        
        self.display_records()
        self.update_statistics()
    
    def display_records(self):
        """Display records in the table"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert filtered records
        for idx, record in enumerate(self.filtered_records, 1):
            self.tree.insert("", tk.END, values=(
                idx,
                record['name'],
                record['date'],
                record['time']
            ))
    
    def update_statistics(self):
        """Update statistics display"""
        total_records = len(self.filtered_records)
        
        # Count unique names
        unique_names = set(record['name'] for record in self.filtered_records)
        unique_count = len(unique_names)
        
        # Count unique dates
        unique_dates = set(record['date'] for record in self.filtered_records)
        date_count = len(unique_dates)
        
        stats_text = f"📊 Total Records: {total_records} | 👥 Unique People: {unique_count} | 📅 Days: {date_count}"
        self.stats_label.config(text=stats_text)
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_var.set("")
        self.date_var.set("All Dates")
        self.filtered_records = self.all_records.copy()
        self.display_records()
        self.update_statistics()
    
    def export_to_csv(self):
        """Export filtered records to a single CSV file"""
        if not self.filtered_records:
            messagebox.showwarning("Warning", "No records to export!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Attendance_Export_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["#", "Name", "Date", "Time"])
                
                for idx, record in enumerate(self.filtered_records, 1):
                    writer.writerow([idx, record['name'], record['date'], record['time']])
            
            messagebox.showinfo("Success", f"✅ Records exported successfully!\n\nFile: {filename}\nRecords: {len(self.filtered_records)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export records:\n{e}")

def main():
    root = tk.Tk()
    app = AttendanceViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

