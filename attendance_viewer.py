import tkinter as tk
from tkinter import ttk, messagebox
from attendance_db import AttendanceDatabase
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

class AttendanceViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Attendance Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Initialize database
        self.db = AttendanceDatabase()
        
        # Create UI
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🎓 Face Recognition Attendance System", 
                        font=("Arial", 28, "bold"), fg="white", bg="#2c3e50")
        title.pack(pady=10)
        
        subtitle = tk.Label(header, text="Modern Attendance Management Dashboard", 
                           font=("Arial", 12), fg="#bdc3c7", bg="#2c3e50")
        subtitle.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg="#ecf0f1")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel (controls and table)
        left_panel = tk.Frame(main_container, bg="#ecf0f1")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Control panel
        control_frame = tk.LabelFrame(left_panel, text="🔍 Search & Filter", 
                                      font=("Arial", 12, "bold"), bg="white", 
                                      fg="#2c3e50", padx=15, pady=15)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search by name
        tk.Label(control_frame, text="Name:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_data())
        search_entry = tk.Entry(control_frame, textvariable=self.search_var, 
                               font=("Arial", 10), width=20)
        search_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Filter by date
        tk.Label(control_frame, text="Date:", font=("Arial", 10), bg="white").grid(row=0, column=2, sticky="w", pady=5)
        self.date_var = tk.StringVar()
        self.date_var.set("All Dates")
        self.date_combo = ttk.Combobox(control_frame, textvariable=self.date_var, 
                                       font=("Arial", 10), width=15, state="readonly")
        self.date_combo.grid(row=0, column=3, padx=10, pady=5)
        self.date_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_data())
        
        # Buttons
        btn_frame = tk.Frame(control_frame, bg="white")
        btn_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        tk.Button(btn_frame, text="🔄 Refresh", command=self.load_data, 
                 font=("Arial", 10, "bold"), bg="#3498db", fg="white", 
                 padx=15, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="✖ Clear", command=self.clear_filters, 
                 font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", 
                 padx=15, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📊 Statistics", command=self.show_statistics, 
                 font=("Arial", 10, "bold"), bg="#9b59b6", fg="white", 
                 padx=15, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Delete Selected", command=self.delete_selected, 
                 font=("Arial", 10, "bold"), bg="#e67e22", fg="white", 
                 padx=15, pady=5, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        stats_frame = tk.LabelFrame(left_panel, text="📈 Quick Stats", 
                                    font=("Arial", 12, "bold"), bg="white", 
                                    fg="#2c3e50", padx=15, pady=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_text = tk.Label(stats_frame, text="", font=("Arial", 11), 
                                   bg="white", fg="#34495e", justify=tk.LEFT)
        self.stats_text.pack()
        
        # Table frame
        table_frame = tk.LabelFrame(left_panel, text="📋 Attendance Records", 
                                    font=("Arial", 12, "bold"), bg="white", 
                                    fg="#2c3e50", padx=5, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Date", "Time"), 
                                show="headings", height=15,
                                yscrollcommand=v_scroll.set,
                                xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)
        
        # Column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="👤 Name")
        self.tree.heading("Date", text="📅 Date")
        self.tree.heading("Time", text="⏰ Time")
        
        # Column widths
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Time", width=120, anchor="center")
        
        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", 
                       rowheight=28, fieldbackground="white", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), 
                       background="#34495e", foreground="white")
        style.map("Treeview", background=[("selected", "#3498db")])
        
        # Pack
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Right panel (visualization)
        right_panel = tk.Frame(main_container, bg="#ecf0f1", width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        viz_frame = tk.LabelFrame(right_panel, text="📊 Data Visualization", 
                                 font=("Arial", 12, "bold"), bg="white", 
                                 fg="#2c3e50", padx=10, pady=10)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        self.viz_container = tk.Frame(viz_frame, bg="white")
        self.viz_container.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        footer = tk.Frame(self.root, bg="#2c3e50", height=35)
        footer.pack(fill=tk.X)
        footer.pack_propagate(False)
        
        tk.Label(footer, text="Developed with ❤️ | Powered by Python & Tkinter", 
                font=("Arial", 9), fg="white", bg="#2c3e50").pack(pady=8)
    
    def load_data(self):
        """Load all data from database"""
        # Get all records
        self.all_records = self.db.get_all_records()
        
        # Update date filter options
        dates = ["All Dates"] + self.db.get_unique_dates()
        self.date_combo['values'] = dates
        
        # Display records
        self.display_records(self.all_records)
        
        # Update stats
        self.update_stats()
        
        # Update visualization
        self.update_visualization()
    
    def filter_data(self):
        """Filter records based on search criteria"""
        search_text = self.search_var.get().strip()
        selected_date = self.date_var.get()
        
        if search_text and selected_date != "All Dates":
            # Filter by both
            records = [r for r in self.all_records if search_text.lower() in r[1].lower() and r[2] == selected_date]
        elif search_text:
            # Filter by name only
            records = self.db.get_records_by_name(search_text)
        elif selected_date != "All Dates":
            # Filter by date only
            records = self.db.get_records_by_date(selected_date)
        else:
            # Show all
            records = self.all_records
        
        self.display_records(records)
        self.update_stats(records)
    
    def display_records(self, records):
        """Display records in table"""
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert new
        for record in records:
            self.tree.insert("", tk.END, values=(record[0], record[1], record[2], record[3]))
    
    def update_stats(self, records=None):
        """Update statistics display"""
        if records is None:
            stats = self.db.get_statistics()
            total = stats['total_records']
            people = stats['unique_people']
            days = stats['unique_dates']
        else:
            total = len(records)
            people = len(set(r[1] for r in records))
            days = len(set(r[2] for r in records))
        
        stats_text = f"📊 Total Records: {total}\n👥 Unique People: {people}\n📅 Total Days: {days}"
        self.stats_text.config(text=stats_text)
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_var.set("")
        self.date_var.set("All Dates")
        self.display_records(self.all_records)
        self.update_stats()
    
    def delete_selected(self):
        """Delete selected record"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete!")
            return
        
        record_id = self.tree.item(selected[0])['values'][0]
        name = self.tree.item(selected[0])['values'][1]
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete attendance record for '{name}'?")
        if confirm:
            self.db.delete_record(record_id)
            messagebox.showinfo("Success", "Record deleted successfully!")
            self.load_data()
    
    def show_statistics(self):
        """Show detailed statistics in a popup"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Detailed Statistics")
        stats_window.geometry("600x400")
        stats_window.configure(bg="#ecf0f1")
        
        # Get statistics
        all_records = self.db.get_all_records()
        names = [r[1] for r in all_records]
        dates = [r[2] for r in all_records]
        
        name_counts = Counter(names)
        date_counts = Counter(dates)
        
        # Create frame
        frame = tk.Frame(stats_window, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(frame, text="📊 Attendance Statistics", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        # By person
        tk.Label(frame, text="👥 Attendance by Person:", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=(10, 5))
        
        person_text = tk.Text(frame, height=8, font=("Arial", 10), bg="#ecf0f1")
        person_text.pack(fill=tk.X, pady=5)
        
        for name, count in name_counts.most_common():
            person_text.insert(tk.END, f"{name}: {count} times\n")
        person_text.config(state=tk.DISABLED)
        
        # By date
        tk.Label(frame, text="📅 Attendance by Date:", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=(10, 5))
        
        date_text = tk.Text(frame, height=8, font=("Arial", 10), bg="#ecf0f1")
        date_text.pack(fill=tk.X, pady=5)
        
        for date, count in sorted(date_counts.items(), reverse=True):
            date_text.insert(tk.END, f"{date}: {count} records\n")
        date_text.config(state=tk.DISABLED)
    
    def update_visualization(self):
        """Update the visualization chart"""
        # Clear previous chart
        for widget in self.viz_container.winfo_children():
            widget.destroy()
        
        # Get data
        all_records = self.db.get_all_records()
        if not all_records:
            tk.Label(self.viz_container, text="No data to visualize", 
                    font=("Arial", 12), bg="white").pack(expand=True)
            return
        
        names = [r[1] for r in all_records]
        name_counts = Counter(names)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='white')
        
        # Plot
        if len(name_counts) <= 10:
            # Bar chart for few people
            names_list = list(name_counts.keys())
            counts_list = list(name_counts.values())
            
            ax.bar(range(len(names_list)), counts_list, color='#3498db')
            ax.set_xticks(range(len(names_list)))
            ax.set_xticklabels(names_list, rotation=45, ha='right')
            ax.set_ylabel('Attendance Count')
            ax.set_title('Attendance by Person')
        else:
            # Pie chart for many people
            top_5 = dict(name_counts.most_common(5))
            others_count = sum(name_counts.values()) - sum(top_5.values())
            
            if others_count > 0:
                top_5['Others'] = others_count
            
            ax.pie(top_5.values(), labels=top_5.keys(), autopct='%1.1f%%', startangle=90)
            ax.set_title('Top 5 Attendance')
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.viz_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = AttendanceViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

