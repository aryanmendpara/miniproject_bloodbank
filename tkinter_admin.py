import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

class BloodBankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management System - Desktop Admin")
        self.root.geometry("1000x650")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f8f9fa")
        
        # DB connection
        self.db_path = os.path.join(os.path.dirname(__file__), "db.sqlite3")
        
        # Header
        header = tk.Frame(root, bg="#dc2626", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Blood Bank Admin Panel", 
                        font=("Arial", 18, "bold"), 
                        bg="#dc2626", fg="white")
        title.pack(side="left", padx=30, pady=15)
        
        subtitle = tk.Label(header, text="Desktop Utility", 
                           font=("Arial", 9), 
                           bg="#dc2626", fg="#fecaca")
        subtitle.pack(side="left", pady=20)
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create tabs
        self.dashboard_tab = tk.Frame(self.notebook, bg="white")
        self.donors_tab = tk.Frame(self.notebook, bg="white")
        self.inventory_tab = tk.Frame(self.notebook, bg="white")
        self.requests_tab = tk.Frame(self.notebook, bg="white")
        
        self.notebook.add(self.dashboard_tab, text="  Dashboard  ")
        self.notebook.add(self.donors_tab, text="  Donors  ")
        self.notebook.add(self.inventory_tab, text="  Inventory  ")
        self.notebook.add(self.requests_tab, text="  Blood Requests  ")
        
        self.setup_dashboard()
        self.setup_donors()
        self.setup_inventory()
        self.setup_requests()
        
        # Status bar
        self.status_bar = tk.Label(root, text="Connected to: db.sqlite3", 
                                   bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                   bg="#e9ecef", font=("Arial", 8))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def setup_dashboard(self):
        # Stats frame
        stats_frame = tk.Frame(self.dashboard_tab, bg="white")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        self.stats = {}
        cards = [
            ("Total Donors", "donors_donor", "#dc2626"),
            ("Total Donations", "donations_donation WHERE donation_status='Confirmed'", "#10b981"),
            ("Available Units", None, "#3b82f6"),
            ("Pending Requests", "requests_app_bloodrequest WHERE status='Pending'", "#f59e0b")
        ]
        
        for i, (title, table, color) in enumerate(cards):
            card = tk.Frame(stats_frame, bg=color, width=220, height=90)
            card.pack(side="left", padx=10)
            card.pack_propagate(False)
            
            count = tk.Label(card, text="0", font=("Arial", 28, "bold"), 
                           bg=color, fg="white")
            count.pack(pady=(15,0))
            
            lbl = tk.Label(card, text=title, font=("Arial", 9), 
                          bg=color, fg="white")
            lbl.pack()
            
            self.stats[title] = count
        
        # Refresh button
        btn_frame = tk.Frame(self.dashboard_tab, bg="white")
        btn_frame.pack(fill="x", padx=30)
        refresh_btn = tk.Button(btn_frame, text="Refresh Dashboard", 
                               command=self.refresh_dashboard,
                               bg="#dc2626", fg="white", 
                               font=("Arial", 9, "bold"),
                               relief=tk.FLAT, padx=15, pady=5)
        refresh_btn.pack(side="right")
        
        self.refresh_dashboard()
    
    def refresh_dashboard(self):
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            # Total donors
            cur.execute("SELECT COUNT(*) FROM donors_donor")
            self.stats["Total Donors"].config(text=str(cur.fetchone()[0]))
            
            # Confirmed donations
            cur.execute("SELECT COUNT(*) FROM donations_donation WHERE donation_status='Confirmed'")
            self.stats["Total Donations"].config(text=str(cur.fetchone()[0]))
            
            # Available units
            cur.execute("SELECT COALESCE(SUM(units_available), 0) FROM inventory_bloodinventory")
            self.stats["Available Units"].config(text=str(cur.fetchone()[0]))
            
            # Pending requests
            cur.execute("SELECT COUNT(*) FROM requests_app_bloodrequest WHERE status='Pending'")
            self.stats["Pending Requests"].config(text=str(cur.fetchone()[0]))
            
            self.status_bar.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            conn.close()
    
    def setup_donors(self):
        top = tk.Frame(self.donors_tab, bg="white")
        top.pack(fill="x", padx=20, pady=(20,10))
        
        tk.Label(top, text="Registered Donors", font=("Arial", 14, "bold"), 
                bg="white").pack(side="left")
        
        tk.Button(top, text="Refresh", command=self.load_donors,
                 bg="#f8f9fa", relief=tk.GROOVE).pack(side="right")
        
        # Table
        cols = ("ID", "Name", "Age", "Gender", "Blood Group", "Phone", "City", "Eligible")
        self.donors_tree = ttk.Treeview(self.donors_tab, columns=cols, show="headings", height=18)
        
        for col in cols:
            self.donors_tree.heading(col, text=col)
            self.donors_tree.column(col, width=110)
        
        self.donors_tree.column("Name", width=150)
        self.donors_tree.column("Phone", width=120)
        self.donors_tree.column("City", width=110)
        
        scrollbar = ttk.Scrollbar(self.donors_tab, orient="vertical", command=self.donors_tree.yview)
        self.donors_tree.configure(yscrollcommand=scrollbar.set)
        
        self.donors_tree.pack(side="left", fill="both", expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side="right", fill="y", padx=(0,20), pady=(0,20))
        
        self.load_donors()
    
    def load_donors(self):
        for item in self.donors_tree.get_children():
            self.donors_tree.delete(item)
        
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT donor_id, full_name, age, gender, blood_group, phone_number, city, donation_eligibility_status FROM donors_donor ORDER BY donor_id")
            for row in cur.fetchall():
                eligible = "Yes" if row[7] else "No"
                self.donors_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], eligible))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
    
    def setup_inventory(self):
        top = tk.Frame(self.inventory_tab, bg="white")
        top.pack(fill="x", padx=20, pady=(20,10))
        
        tk.Label(top, text="Blood Inventory Status", font=("Arial", 14, "bold"), 
                bg="white").pack(side="left")
        
        tk.Button(top, text="Refresh", command=self.load_inventory,
                 bg="#f8f9fa", relief=tk.GROOVE).pack(side="right")
        
        self.inv_frame = tk.Frame(self.inventory_tab, bg="white")
        self.inv_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        self.load_inventory()
    
    def load_inventory(self):
        for widget in self.inv_frame.winfo_children():
            widget.destroy()
        
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT blood_group, units_available, minimum_threshold FROM inventory_bloodinventory ORDER BY blood_group")
            rows = cur.fetchall()
            
            for i, (bg, units, threshold) in enumerate(rows):
                card = tk.Frame(self.inv_frame, bg="#fef2f2" if units < threshold else "#f0fdf4", 
                               width=200, height=110, relief=tk.RIDGE, bd=1)
                card.grid(row=i//4, column=i%4, padx=10, pady=10)
                card.pack_propagate(False)
                
                tk.Label(card, text=bg, font=("Arial", 24, "bold"), 
                        bg=card["bg"], fg="#dc2626").pack(pady=(10,0))
                tk.Label(card, text=f"{units} Units", font=("Arial", 12, "bold"),
                        bg=card["bg"]).pack()
                status = "LOW STOCK" if units < threshold else "OK"
                color = "#dc2626" if units < threshold else "#10b981"
                tk.Label(card, text=status, font=("Arial", 8, "bold"),
                        bg=card["bg"], fg=color).pack()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
    
    def setup_requests(self):
        top = tk.Frame(self.requests_tab, bg="white")
        top.pack(fill="x", padx=20, pady=(20,10))
        
        tk.Label(top, text="Blood Requests", font=("Arial", 14, "bold"), 
                bg="white").pack(side="left")
        
        tk.Button(top, text="Refresh", command=self.load_requests,
                 bg="#f8f9fa", relief=tk.GROOVE).pack(side="right")
        
        cols = ("Request ID", "Hospital", "Blood Group", "Units", "Date", "Priority", "Status")
        self.req_tree = ttk.Treeview(self.requests_tab, columns=cols, show="headings", height=18)
        
        for col in cols:
            self.req_tree.heading(col, text=col)
            self.req_tree.column(col, width=130)
        
        self.req_tree.column("Hospital", width=180)
        
        scrollbar = ttk.Scrollbar(self.requests_tab, orient="vertical", command=self.req_tree.yview)
        self.req_tree.configure(yscrollcommand=scrollbar.set)
        
        self.req_tree.pack(side="left", fill="both", expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side="right", fill="y", padx=(0,20), pady=(0,20))
        
        self.load_requests()
    
    def load_requests(self):
        for item in self.req_tree.get_children():
            self.req_tree.delete(item)
        
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT request_id, hospital_name, blood_group, units_requested, request_date, priority, status FROM requests_app_bloodrequest ORDER BY request_date DESC")
            for row in cur.fetchall():
                self.req_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = BloodBankGUI(root)
    root.mainloop()
