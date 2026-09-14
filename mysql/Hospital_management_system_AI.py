# ```python
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
import os
from ai_chatbot import attach_floating_chatbot



# ============================================================
# DATABASE DETAILS
# ============================================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "123456"
DB_NAME = "hospital_management"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection(database=True):

    if database:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )


# ============================================================
# CREATE DATABASE AND TABLES
# ============================================================

def initialize_database():

    try:

        conn = get_connection(False)
        cursor = conn.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        )

        cursor.close()
        conn.close()

        conn = get_connection(True)
        cursor = conn.cursor()

        # ----------------------------------------------------
        # USERS TABLE
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                hospital_code VARCHAR(100) NOT NULL
            )
        """)

        # ----------------------------------------------------
        # PATIENTS TABLE
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                address VARCHAR(255),
                dob DATE NOT NULL,
                contact VARCHAR(30),
                admission_no VARCHAR(100)
            )
        """)

        # ----------------------------------------------------
        # STAFF TABLE
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                staff_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                specialist VARCHAR(100),
                address VARCHAR(255),
                doj DATE NOT NULL,
                weekday VARCHAR(50),
                salary DECIMAL(10,2),
                contact VARCHAR(30)
            )
        """)

        # ----------------------------------------------------
        # IF OLD STAFF TABLE DOES NOT HAVE CONTACT
        # ----------------------------------------------------

        try:
            cursor.execute(
                "ALTER TABLE staff ADD COLUMN contact VARCHAR(30)"
            )
        except mysql.connector.Error:
            pass

        conn.commit()

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to connect to MySQL.\n\n{e}"
        )

        exit()


# ============================================================
# MAIN APPLICATION
# ============================================================

class HospitalManagementSystem:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Hospital Management System"
        )

        self.root.geometry(
            "1100x750"
        )

        self.root.resizable(
            True,
            True
        )



        self.main_frame = None

        self.show_login()



    # ========================================================
    # CLEAR CURRENT FRAME
    # ========================================================

    def clear_frame(self):

        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(
            self.root,
            bg="#f4f6f7"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )


    # ========================================================
    # PAGE TITLE
    # ========================================================

    def create_title(self, title):

        tk.Label(
            self.main_frame,
            text=title,
            font=("Arial", 28, "bold"),
            bg="#f4f6f7",
            fg="#1f3c88"
        ).pack(
            pady=20
        )


    # ========================================================
    # LOGIN PAGE
    # ========================================================

    def show_login(self):

        self.clear_frame()

        self.create_title(
            "Hospital Management System"
        )

        login_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=2,
            relief="groove"
        )

        login_frame.place(
            relx=0.5,
            rely=0.52,
            anchor="center",
            width=450,
            height=360
        )

        tk.Label(
            login_frame,
            text="Login",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1f3c88"
        ).pack(
            pady=20
        )

        # Username
        tk.Label(
            login_frame,
            text="Username",
            font=("Arial", 12),
            bg="white"
        ).pack(
            anchor="w",
            padx=50
        )

        self.login_username = tk.Entry(
            login_frame,
            font=("Arial", 13),
            width=32
        )

        self.login_username.pack(
            padx=50,
            pady=8
        )

        # Password
        tk.Label(
            login_frame,
            text="Password",
            font=("Arial", 12),
            bg="white"
        ).pack(
            anchor="w",
            padx=50
        )

        self.login_password = tk.Entry(
            login_frame,
            font=("Arial", 13),
            width=32,
            show="*"
        )

        self.login_password.pack(
            padx=50,
            pady=8
        )

        # Buttons
        button_frame = tk.Frame(
            login_frame,
            bg="white"
        )

        button_frame.pack(
            pady=20
        )

        tk.Button(
            button_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#1f7a1f",
            fg="white",
            width=13,
            command=self.login
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        tk.Button(
            button_frame,
            text="Sign Up",
            font=("Arial", 12, "bold"),
            bg="#1f3c88",
            fg="white",
            width=13,
            command=self.show_signup
        ).grid(
            row=0,
            column=1,
            padx=10
        )

        attach_floating_chatbot(
            login_frame,  # Tk() or Toplevel() window, replace with the frame name you want to insert into
            db_configs={
                "employees": dict(host="localhost", user="root", password="123456",
                                  database="hospital_management"),
            },
            api_key=os.environ.get("Gemini _API "),
        )


    # ========================================================
    # SIGNUP PAGE
    # ========================================================

    def show_signup(self):

        self.clear_frame()

        self.create_title(
            "User Registration"
        )

        signup_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=2,
            relief="groove"
        )

        signup_frame.place(
            relx=0.5,
            rely=0.52,
            anchor="center",
            width=500,
            height=450
        )

        tk.Label(
            signup_frame,
            text="Sign Up",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1f3c88"
        ).pack(
            pady=20
        )

        # Username
        tk.Label(
            signup_frame,
            text="Username",
            font=("Arial", 12),
            bg="white"
        ).pack(
            anchor="w",
            padx=60
        )

        self.signup_username = tk.Entry(
            signup_frame,
            font=("Arial", 13),
            width=32
        )

        self.signup_username.pack(
            padx=60,
            pady=8
        )

        # Password
        tk.Label(
            signup_frame,
            text="Password",
            font=("Arial", 12),
            bg="white"
        ).pack(
            anchor="w",
            padx=60
        )

        self.signup_password = tk.Entry(
            signup_frame,
            font=("Arial", 13),
            width=32,
            show="*"
        )

        self.signup_password.pack(
            padx=60,
            pady=8
        )

        # Hospital Code
        tk.Label(
            signup_frame,
            text="Hospital Code",
            font=("Arial", 12),
            bg="white"
        ).pack(
            anchor="w",
            padx=60
        )

        self.signup_hospital_code = tk.Entry(
            signup_frame,
            font=("Arial", 13),
            width=32
        )

        self.signup_hospital_code.pack(
            padx=60,
            pady=8
        )

        tk.Button(
            signup_frame,
            text="Submit",
            font=("Arial", 12, "bold"),
            bg="#1f7a1f",
            fg="white",
            width=15,
            command=self.signup
        ).pack(
            pady=15
        )

        tk.Button(
            signup_frame,
            text="Back to Login",
            font=("Arial", 11),
            width=15,
            command=self.show_login
        ).pack()


    # ========================================================
    # SIGNUP
    # ========================================================

    def signup(self):

        username = self.signup_username.get().strip()
        password = self.signup_password.get().strip()
        hospital_code = self.signup_hospital_code.get().strip()

        if not username or not password or not hospital_code:

            messagebox.showwarning(
                "Warning",
                "Please enter all details."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE username=%s
                """,
                (username,)
            )

            if cursor.fetchone():

                messagebox.showerror(
                    "Error",
                    "Username already exists."
                )

                cursor.close()
                conn.close()

                return

            cursor.execute(
                """
                INSERT INTO users
                (username, password, hospital_code)
                VALUES (%s, %s, %s)
                """,
                (
                    username,
                    password,
                    hospital_code
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Successfully saved."
            )

            self.show_login()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if not username or not password:

            messagebox.showwarning(
                "Warning",
                "Please enter username and password."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE username=%s
                AND password=%s
                """,
                (
                    username,
                    password
                )
            )

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:

                self.show_dashboard()

            else:

                messagebox.showerror(
                    "Login Failed",
                    "No username or password exists."
                )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_frame()

        self.create_title(
            "Hospital Dashboard"
        )

        dashboard = tk.Frame(
            self.main_frame,
            bg="#f4f6f7"
        )

        dashboard.pack(
            pady=200
        )


        tk.Button(
            dashboard,
            text="Patient",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            command=self.show_patient
        ).grid(
            row=0,
            column=0,
            padx=25,
            pady=25
        )

        tk.Button(
            dashboard,
            text="Staff",
            font=("Arial", 16, "bold"),
            bg="#9b59b6",
            fg="white",
            width=20,
            height=2,
            command=self.show_staff
        ).grid(
            row=0,
            column=1,
            padx=25,
            pady=25
        )

        tk.Button(
            dashboard,
            text="Delete Details",
            font=("Arial", 16, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            height=2,
            command=self.show_delete
        ).grid(
            row=1,
            column=0,
            padx=25,
            pady=25
        )

        tk.Button(
            dashboard,
            text="Exit",
            font=("Arial", 16, "bold"),
            bg="#34495e",
            fg="white",
            width=20,
            height=2,
            command=self.exit_application
        ).grid(
            row=1,
            column=1,
            padx=25,
            pady=25
        )

        attach_floating_chatbot(
            self.root,  # Tk() or Toplevel() window, replace with the frame name you want to insert into
            db_configs={
                "employees": dict(host="localhost", user="root", password="123456",
                                  database="hospital_management"),
            },
            api_key=os.environ.get("Gemini _API "),
        )



    # ========================================================
    # PATIENT PAGE
    # ========================================================

    def show_patient(self):

        self.clear_frame()

        self.create_title(
            "Patient Management"
        )

        # Main area
        main_area = tk.Frame(
            self.main_frame,
            bg="#f4f6f7"
        )

        main_area.pack(
            fill="both",
            expand=True,
            padx=25
        )

        # ====================================================
        # LEFT SIDE - PATIENT FORM
        # ====================================================

        form = tk.Frame(
            main_area,
            bg="white",
            bd=2,
            relief="groove"
        )

        form.place(
            x=10,
            y=0,
            width=450,
            height=535
        )

        tk.Label(
            form,
            text="Patient Details",
            font=("Arial", 19, "bold"),
            bg="white",
            fg="#1f3c88"
        ).pack(
            pady=10
        )

        self.patient_id = self.create_entry(
            form,
            "Patient ID"
        )

        self.patient_name = self.create_entry(
            form,
            "Name"
        )

        self.patient_age = self.create_entry(
            form,
            "Age"
        )

        self.patient_address = self.create_entry(
            form,
            "Address"
        )

        # DOB
        tk.Label(
            form,
            text="DOB",
            font=("Arial", 11),
            bg="white"
        ).pack(
            anchor="w",
            padx=35
        )

        self.patient_dob = DateEntry(
            form,
            width=31,
            date_pattern="yyyy-mm-dd",
            font=("Arial", 11)
        )

        self.patient_dob.pack(
            padx=35,
            pady=5
        )

        self.patient_contact = self.create_entry(
            form,
            "Contact"
        )

        self.patient_admission = self.create_entry(
            form,
            "Admission No"
        )

        # Add button
        tk.Button(
            form,
            text="Add Patient",
            font=("Arial", 11, "bold"),
            bg="#1f7a1f",
            fg="white",
            width=18,
            command=self.add_patient
        ).pack(
            pady=10
        )

        # ====================================================
        # RIGHT SIDE - SEARCH
        # ====================================================

        search_box = tk.Frame(
            main_area,
            bg="white",
            bd=2,
            relief="groove"
        )

        search_box.place(
            x=485,
            y=0,
            width=570,
            height=535
        )

        tk.Label(
            search_box,
            text="Search Patient",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#1f3c88"
        ).pack(
            pady=15
        )

        tk.Label(
            search_box,
            text="Search ID",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.patient_search_id = tk.Entry(
            search_box,
            font=("Arial", 12),
            width=35
        )

        self.patient_search_id.pack(
            pady=8
        )

        # Search button below search ID
        tk.Button(
            search_box,
            text="Search Details",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            width=18,
            command=self.search_patient
        ).pack(
            pady=10
        )

        # ====================================================
        # SCROLLABLE RESULT AREA
        # ====================================================

        result_container = tk.Frame(
            search_box,
            bg="white"
        )

        result_container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )

        self.patient_canvas = tk.Canvas(
            result_container,
            bg="white",
            highlightthickness=0
        )

        patient_scrollbar = tk.Scrollbar(
            result_container,
            orient="vertical",
            command=self.patient_canvas.yview
        )

        self.patient_result_frame = tk.Frame(
            self.patient_canvas,
            bg="white"
        )

        self.patient_result_frame.bind(
            "<Configure>",
            lambda e:
            self.patient_canvas.configure(
                scrollregion=self.patient_canvas.bbox("all")
            )
        )

        self.patient_canvas.create_window(
            (0, 0),
            window=self.patient_result_frame,
            anchor="n",
            width=490
        )

        self.patient_canvas.configure(
            yscrollcommand=patient_scrollbar.set
        )

        self.patient_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        patient_scrollbar.pack(
            side="right",
            fill="y"
        )

        # Back button
        tk.Button(
            self.main_frame,
            text="Back to Dashboard",
            font=("Arial", 11, "bold"),
            command=self.show_dashboard
        ).pack(
            side="bottom",
            pady=12
        )


    # ========================================================
    # CREATE ENTRY
    # ========================================================

    def create_entry(self, parent, label):

        tk.Label(
            parent,
            text=label,
            font=("Arial", 11),
            bg="white"
        ).pack(
            anchor="w",
            padx=35
        )

        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            width=32
        )

        entry.pack(
            padx=35,
            pady=4
        )

        return entry


    # ========================================================
    # ADD PATIENT
    # ========================================================

    def add_patient(self):

        patient_id = self.patient_id.get().strip()
        name = self.patient_name.get().strip()
        age = self.patient_age.get().strip()
        address = self.patient_address.get().strip()
        dob = self.patient_dob.get_date()
        contact = self.patient_contact.get().strip()
        admission_no = self.patient_admission.get().strip()

        if not all([
            patient_id,
            name,
            age,
            address,
            contact,
            admission_no
        ]):

            messagebox.showwarning(
                "Warning",
                "Please enter all patient details."
            )

            return

        try:
            age = int(age)
        except ValueError:

            messagebox.showerror(
                "Error",
                "Age must be a number."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO patients
                (
                    patient_id,
                    name,
                    age,
                    address,
                    dob,
                    contact,
                    admission_no
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    patient_id,
                    name,
                    age,
                    address,
                    dob,
                    contact,
                    admission_no
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Patient added successfully."
            )

            self.clear_patient_form()

        except mysql.connector.Error as e:

            if e.errno == 1062:

                messagebox.showerror(
                    "Error",
                    "Patient ID already exists."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


    # ========================================================
    # CLEAR PATIENT FORM
    # ========================================================

    def clear_patient_form(self):

        self.patient_id.delete(
            0,
            tk.END
        )

        self.patient_name.delete(
            0,
            tk.END
        )

        self.patient_age.delete(
            0,
            tk.END
        )

        self.patient_address.delete(
            0,
            tk.END
        )

        self.patient_contact.delete(
            0,
            tk.END
        )

        self.patient_admission.delete(
            0,
            tk.END
        )


    # ========================================================
    # SEARCH PATIENT
    # ========================================================

    def search_patient(self):

        search_id = self.patient_search_id.get().strip()

        if not search_id:

            messagebox.showwarning(
                "Warning",
                "Please enter Search ID."
            )

            return

        # Remove previous results
        for widget in self.patient_result_frame.winfo_children():
            widget.destroy()

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    patient_id,
                    name,
                    age,
                    address,
                    dob,
                    contact,
                    admission_no
                FROM patients
                WHERE patient_id=%s
                """,
                (search_id,)
            )

            patient = cursor.fetchone()

            cursor.close()
            conn.close()

            if patient:

                labels = [
                    "Patient ID",
                    "Name",
                    "Age",
                    "Address",
                    "DOB",
                    "Contact",
                    "Admission No"
                ]

                # Centered result
                result_box = tk.Frame(
                    self.patient_result_frame,
                    bg="#f8f9fa",
                    bd=1,
                    relief="solid"
                )

                result_box.pack(
                    pady=10,
                    padx=15,
                    fill="x"
                )

                for label, value in zip(
                    labels,
                    patient
                ):

                    tk.Label(
                        result_box,
                        text=f"{label}: {value}",
                        font=("Arial", 11),
                        bg="#f8f9fa",
                        anchor="center",
                        justify="center"
                    ).pack(
                        fill="x",
                        pady=5
                    )

            else:

                tk.Label(
                    self.patient_result_frame,
                    text="No patient details found.",
                    font=("Arial", 13, "bold"),
                    fg="red",
                    bg="white"
                ).pack(
                    pady=25
                )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # STAFF PAGE
    # ========================================================

    def show_staff(self):

        self.clear_frame()

        self.create_title(
            "Staff Management"
        )

        main_area = tk.Frame(
            self.main_frame,
            bg="#f4f6f7"
        )

        main_area.pack(
            fill="both",
            expand=True,
            padx=25
        )

        # ====================================================
        # LEFT SIDE STAFF FORM
        # ====================================================

        form = tk.Frame(
            main_area,
            bg="white",
            bd=2,
            relief="groove"
        )

        form.place(
            x=10,
            y=0,
            width=450,
            height=555
        )

        tk.Label(
            form,
            text="Staff Details",
            font=("Arial", 19, "bold"),
            bg="white",
            fg="#1f3c88"
        ).pack(
            pady=10
        )

        # Staff ID
        tk.Label(
            form,
            text="Staff ID",
            font=("Arial", 11),
            bg="white"
        ).pack(
            anchor="w",
            padx=35
        )

        self.staff_id = tk.Entry(
            form,
            font=("Arial", 11),
            width=32
        )

        self.staff_id.pack(
            padx=35,
            pady=4
        )

        self.staff_name = self.create_entry(
            form,
            "Name"
        )

        self.staff_specialist = self.create_entry(
            form,
            "Specialist"
        )

        self.staff_address = self.create_entry(
            form,
            "Address"
        )

        # DOJ
        tk.Label(
            form,
            text="DOJ",
            font=("Arial", 11),
            bg="white"
        ).pack(
            anchor="w",
            padx=35
        )

        self.staff_doj = DateEntry(
            form,
            width=31,
            date_pattern="yyyy-mm-dd",
            font=("Arial", 11)
        )

        self.staff_doj.pack(
            padx=35,
            pady=5
        )

        self.staff_weekday = self.create_entry(
            form,
            "Weekday"
        )

        self.staff_salary = self.create_entry(
            form,
            "Salary"
        )

        # Contact
        self.staff_contact = self.create_entry(
            form,
            "Contact"
        )

        # Add Staff button
        tk.Button(
            form,
            text="Add Staff",
            font=("Arial", 11, "bold"),
            bg="#1f7a1f",
            fg="white",
            width=18,
            command=self.add_staff
        ).pack(
            pady=10
        )

        # ====================================================
        # RIGHT SIDE SEARCH
        # ====================================================

        search_box = tk.Frame(
            main_area,
            bg="white",
            bd=2,
            relief="groove"
        )

        search_box.place(
            x=485,
            y=0,
            width=570,
            height=555
        )

        tk.Label(
            search_box,
            text="Search Staff",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#1f3c88"
        ).pack(
            pady=15
        )

        tk.Label(
            search_box,
            text="Search Staff ID",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.staff_search_id = tk.Entry(
            search_box,
            font=("Arial", 12),
            width=35
        )

        self.staff_search_id.pack(
            pady=8
        )

        # Search button
        tk.Button(
            search_box,
            text="Search Details",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            width=18,
            command=self.search_staff
        ).pack(
            pady=10
        )

        # ====================================================
        # SCROLLABLE STAFF RESULT
        # ====================================================

        result_container = tk.Frame(
            search_box,
            bg="white"
        )

        result_container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )

        self.staff_canvas = tk.Canvas(
            result_container,
            bg="white",
            highlightthickness=0
        )

        staff_scrollbar = tk.Scrollbar(
            result_container,
            orient="vertical",
            command=self.staff_canvas.yview
        )

        self.staff_result_frame = tk.Frame(
            self.staff_canvas,
            bg="white"
        )

        self.staff_result_frame.bind(
            "<Configure>",
            lambda e:
            self.staff_canvas.configure(
                scrollregion=self.staff_canvas.bbox("all")
            )
        )

        self.staff_canvas.create_window(
            (0, 0),
            window=self.staff_result_frame,
            anchor="n",
            width=490
        )

        self.staff_canvas.configure(
            yscrollcommand=staff_scrollbar.set
        )

        self.staff_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        staff_scrollbar.pack(
            side="right",
            fill="y"
        )

        # Back
        tk.Button(
            self.main_frame,
            text="Back to Dashboard",
            font=("Arial", 11, "bold"),
            command=self.show_dashboard
        ).pack(
            side="bottom",
            pady=10
        )


    # ========================================================
    # ADD STAFF
    # ========================================================

    def add_staff(self):

        staff_id = self.staff_id.get().strip()
        name = self.staff_name.get().strip()
        specialist = self.staff_specialist.get().strip()
        address = self.staff_address.get().strip()
        doj = self.staff_doj.get_date()
        weekday = self.staff_weekday.get().strip()
        salary = self.staff_salary.get().strip()
        contact = self.staff_contact.get().strip()

        if not all([
            staff_id,
            name,
            specialist,
            address,
            weekday,
            salary,
            contact
        ]):

            messagebox.showwarning(
                "Warning",
                "Please enter all staff details."
            )

            return

        try:
            staff_id = int(staff_id)
            salary = float(salary)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Staff ID and Salary must be numbers."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO staff
                (
                    staff_id,
                    name,
                    specialist,
                    address,
                    doj,
                    weekday,
                    salary,
                    contact
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    staff_id,
                    name,
                    specialist,
                    address,
                    doj,
                    weekday,
                    salary,
                    contact
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Staff added successfully."
            )

            self.clear_staff_form()

        except mysql.connector.Error as e:

            if e.errno == 1062:

                messagebox.showerror(
                    "Error",
                    "Staff ID already exists."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )


    # ========================================================
    # CLEAR STAFF FORM
    # ========================================================

    def clear_staff_form(self):

        self.staff_id.delete(
            0,
            tk.END
        )

        self.staff_name.delete(
            0,
            tk.END
        )

        self.staff_specialist.delete(
            0,
            tk.END
        )

        self.staff_address.delete(
            0,
            tk.END
        )

        self.staff_weekday.delete(
            0,
            tk.END
        )

        self.staff_salary.delete(
            0,
            tk.END
        )

        self.staff_contact.delete(
            0,
            tk.END
        )


    # ========================================================
    # SEARCH STAFF
    # ========================================================

    def search_staff(self):

        search_id = self.staff_search_id.get().strip()

        if not search_id:

            messagebox.showwarning(
                "Warning",
                "Please enter Staff ID."
            )

            return

        for widget in self.staff_result_frame.winfo_children():
            widget.destroy()

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    staff_id,
                    name,
                    specialist,
                    address,
                    doj,
                    weekday,
                    salary,
                    contact
                FROM staff
                WHERE staff_id=%s
                """,
                (search_id,)
            )

            staff = cursor.fetchone()

            cursor.close()
            conn.close()

            if staff:

                labels = [
                    "Staff ID",
                    "Name",
                    "Specialist",
                    "Address",
                    "DOJ",
                    "Weekday",
                    "Salary",
                    "Contact"
                ]

                result_box = tk.Frame(
                    self.staff_result_frame,
                    bg="#f8f9fa",
                    bd=1,
                    relief="solid"
                )

                result_box.pack(
                    pady=10,
                    padx=15,
                    fill="x"
                )

                for label, value in zip(
                    labels,
                    staff
                ):

                    tk.Label(
                        result_box,
                        text=f"{label}: {value}",
                        font=("Arial", 11),
                        bg="#f8f9fa",
                        anchor="center",
                        justify="center"
                    ).pack(
                        fill="x",
                        pady=5
                    )

            else:

                tk.Label(
                    self.staff_result_frame,
                    text="No staff details found.",
                    font=("Arial", 13, "bold"),
                    fg="red",
                    bg="white"
                ).pack(
                    pady=25
                )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # DELETE PAGE
    # ========================================================

    def show_delete(self):

        self.clear_frame()

        self.create_title(
            "Delete Details"
        )

        main_delete = tk.Frame(
            self.main_frame,
            bg="#f4f6f7"
        )

        main_delete.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # DELETE PATIENT
        # ====================================================

        patient_box = tk.Frame(
            main_delete,
            bg="white",
            bd=2,
            relief="groove"
        )

        patient_box.place(
            x=70,
            y=10,
            width=450,
            height=400
        )

        tk.Label(
            patient_box,
            text="Delete Patient",
            font=("Arial", 21, "bold"),
            bg="white",
            fg="#e74c3c"
        ).pack(
            pady=25
        )

        tk.Label(
            patient_box,
            text="Patient ID",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.delete_patient_id = tk.Entry(
            patient_box,
            font=("Arial", 12),
            width=30
        )

        self.delete_patient_id.pack(
            pady=10
        )

        tk.Label(
            patient_box,
            text="Date of Birth",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.delete_patient_dob = DateEntry(
            patient_box,
            width=27,
            date_pattern="yyyy-mm-dd",
            font=("Arial", 11)
        )

        self.delete_patient_dob.pack(
            pady=10
        )

        tk.Button(
            patient_box,
            text="Delete Patient",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            command=self.delete_patient
        ).pack(
            pady=25
        )

        # ====================================================
        # DELETE STAFF
        # ====================================================

        staff_box = tk.Frame(
            main_delete,
            bg="white",
            bd=2,
            relief="groove"
        )

        staff_box.place(
            x=580,
            y=10,
            width=450,
            height=400
        )

        tk.Label(
            staff_box,
            text="Delete Staff",
            font=("Arial", 21, "bold"),
            bg="white",
            fg="#e74c3c"
        ).pack(
            pady=25
        )

        tk.Label(
            staff_box,
            text="Staff ID",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.delete_staff_id = tk.Entry(
            staff_box,
            font=("Arial", 12),
            width=30
        )

        self.delete_staff_id.pack(
            pady=10
        )

        tk.Label(
            staff_box,
            text="Date of Joining",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.delete_staff_doj = DateEntry(
            staff_box,
            width=27,
            date_pattern="yyyy-mm-dd",
            font=("Arial", 11)
        )

        self.delete_staff_doj.pack(
            pady=10
        )

        tk.Button(
            staff_box,
            text="Delete Staff",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            command=self.delete_staff
        ).pack(
            pady=25
        )

        tk.Button(
            self.main_frame,
            text="Back to Dashboard",
            font=("Arial", 11, "bold"),
            command=self.show_dashboard
        ).pack(
            side="bottom",
            pady=20
        )


    # ========================================================
    # DELETE PATIENT
    # ID + DOB MUST MATCH
    # ========================================================

    def delete_patient(self):

        patient_id = self.delete_patient_id.get().strip()

        patient_dob = self.delete_patient_dob.get_date()

        if not patient_id:

            messagebox.showwarning(
                "Warning",
                "Please enter Patient ID."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # IMPORTANT:
            # Both Patient ID AND DOB must match
            cursor.execute(
                """
                SELECT name
                FROM patients
                WHERE patient_id=%s
                AND dob=%s
                """,
                (
                    patient_id,
                    patient_dob
                )
            )

            patient = cursor.fetchone()

            cursor.close()
            conn.close()

            if not patient:

                messagebox.showerror(
                    "Delete Failed",
                    "Patient ID and Date of Birth do not match."
                )

                return

            patient_name = patient[0]

            # Confirmation
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete patient {patient_name}?"
            )

            if not confirm:
                return

            # Delete only matching ID + DOB
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM patients
                WHERE patient_id=%s
                AND dob=%s
                """,
                (
                    patient_id,
                    patient_dob
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                f"Patient {patient_name} deleted successfully."
            )

            self.delete_patient_id.delete(
                0,
                tk.END
            )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # DELETE STAFF
    # ID + DOJ MUST MATCH
    # ========================================================

    def delete_staff(self):

        staff_id = self.delete_staff_id.get().strip()

        staff_doj = self.delete_staff_doj.get_date()

        if not staff_id:

            messagebox.showwarning(
                "Warning",
                "Please enter Staff ID."
            )

            return

        try:

            staff_id = int(staff_id)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Staff ID must be a number."
            )

            return

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # IMPORTANT:
            # Both Staff ID AND DOJ must match
            cursor.execute(
                """
                SELECT name
                FROM staff
                WHERE staff_id=%s
                AND doj=%s
                """,
                (
                    staff_id,
                    staff_doj
                )
            )

            staff = cursor.fetchone()

            cursor.close()
            conn.close()

            if not staff:

                messagebox.showerror(
                    "Delete Failed",
                    "Staff ID and Date of Joining do not match."
                )

                return

            staff_name = staff[0]

            # Confirmation
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete staff {staff_name}?"
            )

            if not confirm:
                return

            # Delete only matching ID + DOJ
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM staff
                WHERE staff_id=%s
                AND doj=%s
                """,
                (
                    staff_id,
                    staff_doj
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                f"Staff {staff_name} deleted successfully."
            )

            self.delete_staff_id.delete(
                0,
                tk.END
            )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # EXIT
    # ========================================================

    def exit_application(self):

        confirm = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        )

        if confirm:

            self.root.destroy()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    initialize_database()

    root = tk.Tk()

    app = HospitalManagementSystem(root)

    root.mainloop()
# ```
#
# ### Important change in deletion
#
# The patient deletion now uses:
#
# ```python
# WHERE patient_id=%s
# AND dob=%s
# ```
#
# So if the ID is correct but DOB is wrong:
#
# ```text
# Delete Failed
# Patient ID and Date of Birth do not match.
# ```
#
# The patient will **not** be deleted.
#
# Staff deletion works the same way:
#
# ```python
# WHERE staff_id=%s
# AND doj=%s
# ```
#
# So **both Staff ID and DOJ must match** before the confirmation appears.
#
# Also, the Staff table now contains:
#
# ```text
# Staff ID
# Name
# Specialist
# Address
# DOJ
# Weekday
# Salary
# Contact
# ```
#
# and the Patient table contains:
#
# ```text
# Patient ID
# Name
# Age
# Address
# DOB
# Contact
# Admission No
# ```
#
# The search results are in a **scrollable middle/right section**, so even if more information is added later, the result area can be scrolled.
