import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import pickle
import numpy as np
import os
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from PIL import Image, ImageTk
from attendance_db import AttendanceDatabase
import threading

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1400x800")
        self.root.configure(bg="#ecf0f1")
        
        # Initialize variables
        self.db = AttendanceDatabase()
        self.video = None
        self.is_running = False
        self.current_mode = "home"  
        self.facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        
        # Registration variables
        self.reg_name = ""
        self.reg_faces = []
        self.reg_counter = 0
        
        # Attendance variables
        self.knn_model = None
        self.labels = []
        self.faces_data = []
        
        # Create data directory
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Create UI
        self.create_home_screen()
        
        # Load existing model
        self.load_model()
        
        # Bind keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.back_to_home())
        self.root.bind('<F1>', lambda e: self.show_help())
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_home_screen(self):
        """Create main home screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_mode = "home"
        
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=120)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🎓 Face Recognition Attendance System", 
                font=("Arial", 32, "bold"), fg="white", bg="#2c3e50").pack(pady=15)
        
        tk.Label(header, text="AI-Powered Attendance Management", 
                font=("Arial", 14), fg="#bdc3c7", bg="#2c3e50").pack()
        
        # Main content
        content = tk.Frame(self.root, bg="#ecf0f1")
        content.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        # Welcome message
        tk.Label(content, text="Welcome! Choose an option:", 
                font=("Arial", 20, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=30)
        
        # Buttons container
        btn_container = tk.Frame(content, bg="#ecf0f1")
        btn_container.pack(expand=True)
        
        # Register button
        register_btn = tk.Button(btn_container, text="👤 Register New Face", 
                                font=("Arial", 18, "bold"), bg="#3498db", fg="white",
                                padx=40, pady=20, relief=tk.FLAT, cursor="hand2",
                                command=self.show_register_screen)
        register_btn.grid(row=0, column=0, padx=20, pady=20)
        
        # Attendance button
        attendance_btn = tk.Button(btn_container, text="📸 Take Attendance", 
                                   font=("Arial", 18, "bold"), bg="#27ae60", fg="white",
                                   padx=40, pady=20, relief=tk.FLAT, cursor="hand2",
                                   command=self.show_attendance_screen)
        attendance_btn.grid(row=0, column=1, padx=20, pady=20)
        
        # View records button
        view_btn = tk.Button(btn_container, text="📊 View Records", 
                            font=("Arial", 18, "bold"), bg="#9b59b6", fg="white",
                            padx=40, pady=20, relief=tk.FLAT, cursor="hand2",
                            command=self.show_records_screen)
        view_btn.grid(row=1, column=0, padx=20, pady=20)
        
        # Exit button
        exit_btn = tk.Button(btn_container, text="❌ Exit", 
                            font=("Arial", 18, "bold"), bg="#e74c3c", fg="white",
                            padx=40, pady=20, relief=tk.FLAT, cursor="hand2",
                            command=self.on_closing)
        exit_btn.grid(row=1, column=1, padx=20, pady=20)
        
        # Statistics and help at bottom
        bottom_frame = tk.Frame(content, bg="#ecf0f1")
        bottom_frame.pack(side=tk.BOTTOM, pady=20)
        
        stats = self.db.get_statistics()
        stats_text = f"📊 Total Records: {stats['total_records']} | 👥 Registered People: {stats['unique_people']} | 📅 Days: {stats['unique_dates']}"
        tk.Label(bottom_frame, text=stats_text, font=("Arial", 12), 
                bg="#ecf0f1", fg="#7f8c8d").pack()
        
        # Help button
        tk.Button(bottom_frame, text="❓ Help & Shortcuts (F1)", 
                 font=("Arial", 10), bg="#95a5a6", fg="white",
                 padx=15, pady=5, relief=tk.FLAT, cursor="hand2",
                 command=self.show_help, borderwidth=0).pack(pady=10)
    
    def show_register_screen(self):
        """Show face registration screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_mode = "register"
        
        # Header with Back button
        header = tk.Frame(self.root, bg="#3498db", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Back button on left
        tk.Button(header, text="← Back", font=("Arial", 12, "bold"), 
                 bg="#2980b9", fg="white", padx=20, pady=5, relief=tk.FLAT,
                 cursor="hand2", command=self.back_to_home).place(x=20, y=25)
        
        tk.Label(header, text="👤 Register New Face", 
                font=("Arial", 24, "bold"), fg="white", bg="#3498db").pack(pady=20)
        
        # Main container
        container = tk.Frame(self.root, bg="#ecf0f1")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Input form
        left_panel = tk.Frame(container, bg="white", padx=30, pady=30)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        tk.Label(left_panel, text="Enter Your Information", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        
        tk.Label(left_panel, text="Full Name:", font=("Arial", 12), bg="white").pack(anchor="w", pady=(20, 5))
        self.name_entry = tk.Entry(left_panel, font=("Arial", 14), width=25)
        self.name_entry.pack(pady=5)
        
        tk.Label(left_panel, text="Instructions:", 
                font=("Arial", 12, "bold"), bg="white", fg="#e74c3c").pack(anchor="w", pady=(30, 10))
        
        instructions = [
            "✓ Look directly at the camera",
            "✓ Ensure good lighting",
            "✓ Move your face slightly for different angles",
            "✓ 100 samples will be collected automatically",
            "✓ Press 'Start Registration' to begin"
        ]
        
        for instruction in instructions:
            tk.Label(left_panel, text=instruction, font=("Arial", 11), 
                    bg="white", fg="#34495e").pack(anchor="w", pady=3)
        
        # Progress
        tk.Label(left_panel, text="Progress:", font=("Arial", 12, "bold"), 
                bg="white").pack(anchor="w", pady=(20, 5))
        
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(left_panel, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.pack(pady=5)
        
        self.progress_label = tk.Label(left_panel, text="0/100 samples", 
                                       font=("Arial", 11), bg="white", fg="#3498db")
        self.progress_label.pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(pady=30)
        
        self.start_reg_btn = tk.Button(btn_frame, text="▶ Start Registration", 
                                       font=("Arial", 12, "bold"), bg="#27ae60", fg="white",
                                       padx=20, pady=10, relief=tk.FLAT, cursor="hand2",
                                       command=self.start_registration)
        self.start_reg_btn.pack(pady=5)
        
        self.stop_reg_btn = tk.Button(btn_frame, text="⏹ Stop & Save", 
                                      font=("Arial", 12, "bold"), bg="#e67e22", fg="white",
                                      padx=20, pady=10, relief=tk.FLAT, cursor="hand2",
                                      command=self.stop_registration, state=tk.DISABLED,
                                      borderwidth=0)
        self.stop_reg_btn.pack(pady=5)
        
        tk.Button(btn_frame, text="🏠 Back to Home", 
                 font=("Arial", 12, "bold"), bg="#e74c3c", fg="white",
                 padx=20, pady=10, relief=tk.FLAT, cursor="hand2",
                 command=self.back_to_home, borderwidth=0,
                 activebackground="#c0392b", activeforeground="white").pack(pady=5)
        
        # Keyboard shortcut hint
        tk.Label(btn_frame, text="Tip: Press ESC to go back", 
                font=("Arial", 10, "italic"), bg="white", fg="#7f8c8d").pack(pady=5)
        
        # Right panel - Camera feed
        right_panel = tk.Frame(container, bg="white")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right_panel, text="Camera Preview", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        self.camera_label = tk.Label(right_panel, bg="black")
        self.camera_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Label(right_panel, text="Ready to start registration", 
                                     font=("Arial", 12), bg="white", fg="#7f8c8d")
        self.status_label.pack(pady=10)
    
    def show_attendance_screen(self):
        """Show attendance taking screen"""
        # Check if there are registered faces
        if not os.path.exists('data/faces_data.pkl') or not os.path.exists('data/names.pkl'):
            messagebox.showwarning("No Data", "No registered faces found!\n\nPlease register faces first.")
            return
        
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_mode = "attendance"
        
        # Header with Back button
        header = tk.Frame(self.root, bg="#27ae60", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Back button on left
        tk.Button(header, text="← Back", font=("Arial", 12, "bold"), 
                 bg="#229954", fg="white", padx=20, pady=5, relief=tk.FLAT,
                 cursor="hand2", command=self.back_to_home).place(x=20, y=25)
        
        tk.Label(header, text="📸 Take Attendance", 
                font=("Arial", 24, "bold"), fg="white", bg="#27ae60").pack(pady=20)
        
        # Main container
        container = tk.Frame(self.root, bg="#ecf0f1")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Camera
        left_panel = tk.Frame(container, bg="white")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left_panel, text="Live Camera Feed", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        self.camera_label = tk.Label(left_panel, bg="black")
        self.camera_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Controls
        control_frame = tk.Frame(left_panel, bg="white")
        control_frame.pack(pady=10)
        
        self.detect_status = tk.Label(control_frame, text=" No face detected", 
                                      font=("Arial", 14, "bold"), bg="white", fg="#e74c3c")
        self.detect_status.pack(pady=15)
        
        # Mark Attendance Button - Large and prominent
        tk.Button(control_frame, text="Mark Attendance", 
                 font=("Arial", 16, "bold"), bg="#27ae60", fg="white",
                 padx=40, pady=20, relief=tk.FLAT, cursor="hand2",
                 command=self.mark_attendance, borderwidth=0,
                 activebackground="#229954", activeforeground="white").pack(pady=10)
        
        # Back to Home Button - Large and clear
        tk.Button(control_frame, text="🏠 Back to Home", 
                 font=("Arial", 14, "bold"), bg="#e74c3c", fg="white",
                 padx=35, pady=15, relief=tk.FLAT, cursor="hand2",
                 command=self.back_to_home, borderwidth=0,
                 activebackground="#c0392b", activeforeground="white").pack(pady=10)
        
        # Keyboard shortcut hint
        tk.Label(control_frame, text="Tip: Press ESC to go back", 
                font=("Arial", 10, "italic"), bg="white", fg="#7f8c8d").pack(pady=5)
        
        # Right panel - Recent attendance
        right_panel = tk.Frame(container, bg="white", width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        tk.Label(right_panel, text="📋 Today's Attendance", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        # Table
        table_frame = tk.Frame(right_panel, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.attendance_tree = ttk.Treeview(table_frame, columns=("Name", "Time"), 
                                           show="headings", height=20,
                                           yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.attendance_tree.yview)
        
        self.attendance_tree.heading("Name", text="👤 Name")
        self.attendance_tree.heading("Time", text="⏰ Time")
        
        self.attendance_tree.column("Name", width=180)
        self.attendance_tree.column("Time", width=120)
        
        self.attendance_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load today's attendance
        self.load_today_attendance()
        
        # Start camera
        self.start_attendance_camera()
    
    def show_records_screen(self):
        """Show attendance records screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_mode = "records"
        
        # Header with Back button
        header = tk.Frame(self.root, bg="#9b59b6", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Back button on left
        tk.Button(header, text="← Back", font=("Arial", 12, "bold"), 
                 bg="#8e44ad", fg="white", padx=20, pady=5, relief=tk.FLAT,
                 cursor="hand2", command=self.back_to_home).place(x=20, y=25)
        
        tk.Label(header, text="📊 Attendance Records", 
                font=("Arial", 24, "bold"), fg="white", bg="#9b59b6").pack(pady=20)
        
        # Main container
        container = tk.Frame(self.root, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Controls
        control_frame = tk.Frame(container, bg="white")
        control_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(control_frame, text="🔍 Search Name:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_records())
        search_entry = tk.Entry(control_frame, textvariable=self.search_var, font=("Arial", 11), width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="📅 Date:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=10)
        
        self.date_filter_var = tk.StringVar()
        self.date_filter_var.set("All Dates")
        self.date_filter_combo = ttk.Combobox(control_frame, textvariable=self.date_filter_var, 
                                             font=("Arial", 10), width=15, state="readonly")
        self.date_filter_combo.pack(side=tk.LEFT, padx=5)
        self.date_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_records())
        
        # Update dates
        dates = ["All Dates"] + self.db.get_unique_dates()
        self.date_filter_combo['values'] = dates
        
        tk.Button(control_frame, text="🔄 Refresh", font=("Arial", 11, "bold"), 
                 bg="#3498db", fg="white", padx=20, pady=8, relief=tk.FLAT,
                 command=self.load_all_records, cursor="hand2", borderwidth=0).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="🏠 Back to Home", font=("Arial", 11, "bold"), 
                 bg="#e74c3c", fg="white", padx=20, pady=8, relief=tk.FLAT,
                 command=self.back_to_home, cursor="hand2", borderwidth=0,
                 activebackground="#c0392b", activeforeground="white").pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="(Press ESC to go back)", 
                font=("Arial", 9, "italic"), bg="white", fg="#7f8c8d").pack(side=tk.LEFT, padx=10)
        
        # Stats
        stats = self.db.get_statistics()
        stats_text = f"📊 Total: {stats['total_records']} | 👥 People: {stats['unique_people']} | 📅 Days: {stats['unique_dates']}"
        tk.Label(container, text=stats_text, font=("Arial", 12, "bold"), 
                bg="white", fg="#34495e").pack(pady=10)
        
        # Table
        table_frame = tk.Frame(container, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.records_tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Date", "Time"), 
                                        show="headings", height=20,
                                        yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.records_tree.yview)
        
        self.records_tree.heading("ID", text="ID")
        self.records_tree.heading("Name", text="👤 Name")
        self.records_tree.heading("Date", text="📅 Date")
        self.records_tree.heading("Time", text="⏰ Time")
        
        self.records_tree.column("ID", width=50, anchor="center")
        self.records_tree.column("Name", width=250)
        self.records_tree.column("Date", width=150, anchor="center")
        self.records_tree.column("Time", width=150, anchor="center")
        
        self.records_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load records
        self.load_all_records()
    
    def start_registration(self):
        """Start face registration process"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Invalid Input", "Please enter your name!")
            return
        
        self.reg_name = name
        self.reg_faces = []
        self.reg_counter = 0
        
        self.start_reg_btn.config(state=tk.DISABLED)
        self.stop_reg_btn.config(state=tk.NORMAL)
        self.name_entry.config(state=tk.DISABLED)
        
        self.is_running = True
        threading.Thread(target=self.registration_loop, daemon=True).start()
    
    def registration_loop(self):
        """Registration camera loop"""
        # Try DirectShow backend first (Windows), then default
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.video.isOpened():
            self.video = cv2.VideoCapture(0)
        
        # Set camera properties for better performance
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.video.set(cv2.CAP_PROP_FPS, 30)
        
        frame_count = 0
        
        while self.is_running and len(self.reg_faces) < 100:
            ret, frame = self.video.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(60, 60))
            
            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w, :]
                resized_img = cv2.resize(crop_img, (50, 50))
                
                if frame_count % 10 == 0 and len(self.reg_faces) < 100:
                    self.reg_faces.append(resized_img)
                    self.progress_var.set(len(self.reg_faces))
                    self.progress_label.config(text=f"{len(self.reg_faces)}/100 samples")
                
                frame_count += 1
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
                cv2.putText(frame, f"Samples: {len(self.reg_faces)}/100", (50, 50), 
                           cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
            
            # Update camera display
            self.update_camera_display(frame)
            
            if len(self.reg_faces) >= 100:
                self.root.after(0, self.complete_registration)
                break
        
        if self.video:
            self.video.release()
    
    def stop_registration(self):
        """Stop registration and save data"""
        if len(self.reg_faces) < 10:
            messagebox.showwarning("Insufficient Data", "Please collect at least 10 face samples!")
            return
        
        self.is_running = False
        self.complete_registration()
    
    def complete_registration(self):
        """Complete registration and save data"""
        if len(self.reg_faces) == 0:
            messagebox.showerror("Error", "No face data collected!")
            self.back_to_home()
            return
        
        self.status_label.config(text="Saving data...", fg="#e67e22")
        
        # Process face data
        faces_data = np.asarray(self.reg_faces)
        faces_data = faces_data.reshape(len(self.reg_faces), -1)
        
        num_samples = len(faces_data)
        
        # Save names
        if os.path.exists('data/names.pkl'):
            with open('data/names.pkl', 'rb') as f:
                names = pickle.load(f)
            names = names + [self.reg_name] * num_samples
        else:
            names = [self.reg_name] * num_samples
        
        with open('data/names.pkl', 'wb') as f:
            pickle.dump(names, f)
        
        # Save face data
        if os.path.exists('data/faces_data.pkl'):
            with open('data/faces_data.pkl', 'rb') as f:
                faces = pickle.load(f)
            faces = np.append(faces, faces_data, axis=0)
        else:
            faces = faces_data
        
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces, f)
        
        messagebox.showinfo("Success", f"✅ Registration completed!\n\n"
                                      f"Name: {self.reg_name}\n"
                                      f"Samples: {num_samples}")
        
        # Reload model
        self.load_model()
        
        self.back_to_home()
    
    def start_attendance_camera(self):
        """Start attendance camera"""
        self.is_running = True
        self.detected_name = ""
        threading.Thread(target=self.attendance_loop, daemon=True).start()
    
    def attendance_loop(self):
        """Attendance camera loop"""
        # Try DirectShow backend first (Windows), then default
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.video.isOpened():
            self.video = cv2.VideoCapture(0)
        
        # Set camera properties for better performance
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.video.set(cv2.CAP_PROP_FPS, 30)
        
        while self.is_running and self.current_mode == "attendance":
            ret, frame = self.video.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(60, 60))
            
            self.detected_name = ""
            
            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w, :]
                resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                
                if self.knn_model:
                    output = self.knn_model.predict(resized_img)
                    self.detected_name = output[0]
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
                    cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
                    cv2.putText(frame, str(output[0]), (x, y-15), 
                               cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    
                    self.root.after(0, lambda: self.detect_status.config(
                        text=f"🟢 Detected: {output[0]}", fg="#27ae60"))
            
            if not faces:
                self.root.after(0, lambda: self.detect_status.config(
                    text="🔴 No face detected", fg="#e74c3c"))
            
            self.update_camera_display(frame)
        
        if self.video:
            self.video.release()
    
    def mark_attendance(self):
        """Mark attendance for detected person"""
        if not self.detected_name:
            messagebox.showwarning("No Face", "No face detected!\n\nPlease ensure a face is visible to the camera.")
            return
        
        # Get current time
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")
        
        # Save to database
        self.db.add_attendance(self.detected_name, date, time)
        
        # Update today's list
        self.load_today_attendance()
        
        messagebox.showinfo("Success", f"✅ Attendance marked!\n\n"
                                      f"Name: {self.detected_name}\n"
                                      f"Time: {time}")
    
    def load_today_attendance(self):
        """Load today's attendance records"""
        today = datetime.now().strftime("%d-%m-%Y")
        records = self.db.get_records_by_date(today)
        
        # Clear tree
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        # Insert records
        for record in records:
            self.attendance_tree.insert("", 0, values=(record[1], record[3]))
    
    def load_all_records(self):
        """Load all attendance records"""
        self.all_records = self.db.get_all_records()
        self.display_filtered_records(self.all_records)
    
    def filter_records(self):
        """Filter records based on search criteria"""
        search_text = self.search_var.get().strip().lower()
        selected_date = self.date_filter_var.get()
        
        filtered = []
        for record in self.all_records:
            # Check name
            if search_text and search_text not in record[1].lower():
                continue
            # Check date
            if selected_date != "All Dates" and record[2] != selected_date:
                continue
            filtered.append(record)
        
        self.display_filtered_records(filtered)
    
    def display_filtered_records(self, records):
        """Display filtered records in tree"""
        # Clear tree
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        # Insert records
        for record in records:
            self.records_tree.insert("", tk.END, values=(record[0], record[1], record[2], record[3]))
    
    def load_model(self):
        """Load trained KNN model"""
        try:
            if os.path.exists('data/faces_data.pkl') and os.path.exists('data/names.pkl'):
                with open('data/names.pkl', 'rb') as f:
                    self.labels = pickle.load(f)
                with open('data/faces_data.pkl', 'rb') as f:
                    self.faces_data = pickle.load(f)
                
                self.knn_model = KNeighborsClassifier(n_neighbors=5)
                self.knn_model.fit(self.faces_data, self.labels)
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def update_camera_display(self, frame):
        """Update camera display in GUI"""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        if hasattr(self, 'camera_label'):
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
    
    def back_to_home(self):
        """Go back to home screen"""
        self.is_running = False
        if self.video:
            self.video.release()
        self.create_home_screen()
    
    def show_help(self):
        """Show help dialog with keyboard shortcuts"""
        help_text = """
🎯 Keyboard Shortcuts:

ESC      - Go back to home screen
F1       - Go to home screen (from anywhere)

📋 Quick Tips:

• All screens have a "← Back" button at top-left corner
• Large "Back to Home" buttons are available on all screens
• Red buttons = Go back / Exit
• Green buttons = Confirm / Save
• Blue buttons = Actions

🔍 Navigation:

Home Screen:
  - Click on any option to proceed
  
Registration:
  - Enter name → Start → Wait for 100 samples
  - ESC to cancel and go back
  
Attendance:
  - Wait for face detection (🟢 Green status)
  - Click "Mark Attendance" to save
  - ESC to go back to home
  
View Records:
  - Search by name or filter by date
  - ESC to go back to home
        """
        
        messagebox.showinfo("Help & Shortcuts", help_text)
    
    def on_closing(self):
        """Handle window closing"""
        self.is_running = False
        if self.video:
            self.video.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

