import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import os
from ai_chatbot import attach_floating_chatbot



# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "123456"
DB_NAME = "library_management_system"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_database():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        )

        cursor.close()
        connection.close()

    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to create database:\n{e}"
        )


def get_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to connect to database:\n{e}"
        )
        return None


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():

    connection = get_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # BOOK TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                edition VARCHAR(100),
                author VARCHAR(255),
                category VARCHAR(50),
                price DECIMAL(10,2)
            )
        """)

        # STUDENT TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                class_name VARCHAR(100),
                section VARCHAR(50),
                book_id INT,
                FOREIGN KEY (book_id)
                REFERENCES books(book_id)
                ON DELETE SET NULL
            )
        """)

        connection.commit()

        cursor.close()
        connection.close()

    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to create tables:\n{e}"
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

class LibraryManagementSystem:

    def __init__(self, root):

        self.root = root

        self.root.title("Library Management System")

        self.root.geometry("900x600")

        # Allow window to be resized so maximize symbol appears and frames can expand
        self.root.resizable(True, True)
        # Start the application maximized on Windows
        try:
            self.root.state('zoomed')
        except Exception:
            pass

        self.root.configure(bg="#f2f2f2")

        self.create_dashboard()

        attach_floating_chatbot(
            root,  # Tk() or Toplevel() window, replace with the frame name you want to insert into
            db_configs={
                "employees": dict(host="localhost", user="root", password="123456",
                                  database="library_management_system"),
            },
            api_key=os.environ.get("Gemini API Key"),
        )

    # ========================================================
    # CLEAR WINDOW
    # ========================================================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()


    # ========================================================
    # COMMON TITLE
    # ========================================================

    def create_title(self, title):

        title_label = tk.Label(
            self.root,
            text=title,
            font=("Arial", 24, "bold"),
            bg="#f2f2f2",
            fg="#222222"
        )

        title_label.pack(pady=25)


    # ========================================================
    # DASHBOARD
    # ========================================================

    def create_dashboard(self):

        self.clear_window()

        title = tk.Label(
            self.root,
            text="LIBRARY MANAGEMENT SYSTEM",
            font=("Arial", 28, "bold"),
            bg="#f2f2f2",
            fg="#1f1f1f"
        )

        title.pack(pady=35)

        subtitle = tk.Label(
            self.root,
            text="Library Dashboard",
            font=("Arial", 16),
            bg="#f2f2f2"
        )

        subtitle.pack(pady=5)

        button_frame = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        button_frame.pack(pady=35)

        button_style = {
            "font": ("Arial", 14, "bold"),
            "width": 22,
            "height": 2,
            "cursor": "hand2"
        }

        tk.Button(
            button_frame,
            text="1. Add Book",
            command=self.add_book,
            **button_style
        ).grid(row=0, column=0, padx=15, pady=15)

        tk.Button(
            button_frame,
            text="2. Modify Book",
            command=self.modify_book,
            **button_style
        ).grid(row=0, column=1, padx=15, pady=15)

        tk.Button(
            button_frame,
            text="3. Delete Book",
            command=self.delete_book,
            **button_style
        ).grid(row=1, column=0, padx=15, pady=15)

        tk.Button(
            button_frame,
            text="4. Student",
            command=self.student_page,
            **button_style
        ).grid(row=1, column=1, padx=15, pady=15)

        tk.Button(
            button_frame,
            text="5. Search Book",
            command=self.search_book,
            **button_style
        ).grid(row=2, column=0, columnspan=2, pady=15)


    # ========================================================
    # ADD BOOK
    # ========================================================

    def add_book(self):

        self.clear_window()

        self.create_title("ADD BOOK")

        form = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        form.pack(pady=10)

        # Variables
        book_id = tk.StringVar()
        title = tk.StringVar()
        edition = tk.StringVar()
        author = tk.StringVar()
        category = tk.StringVar()
        price = tk.StringVar()

        fields = [
            ("Book ID", book_id),
            ("Title", title),
            ("Edition", edition),
            ("Author", author),
            ("Price", price)
        ]

        entries = {}

        for row, (label_text, variable) in enumerate(fields):

            tk.Label(
                form,
                text=label_text,
                font=("Arial", 13),
                bg="#f2f2f2"
            ).grid(
                row=row,
                column=0,
                padx=15,
                pady=10,
                sticky="w"
            )

            entry = tk.Entry(
                form,
                textvariable=variable,
                font=("Arial", 13),
                width=30
            )

            entry.grid(
                row=row,
                column=1,
                padx=15,
                pady=10
            )

            entries[label_text] = entry

        # Category
        tk.Label(
            form,
            text="Category",
            font=("Arial", 13),
            bg="#f2f2f2"
        ).grid(
            row=5,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        category_box = ttk.Combobox(
            form,
            textvariable=category,
            values=[
                "CSE",
                "ECE",
                "MECH",
                "DevOps"
            ],
            state="readonly",
            font=("Arial", 13),
            width=28
        )

        category_box.grid(
            row=5,
            column=1,
            padx=15,
            pady=10
        )

        # Add Book
        tk.Button(
            self.root,
            text="Add Book",
            font=("Arial", 13, "bold"),
            width=15,
            command=lambda: self.save_book(
                book_id,
                title,
                edition,
                author,
                category,
                price
            )
        ).pack(pady=15)

        # Back
        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12),
            width=15,
            command=self.create_dashboard
        ).pack()


    def save_book(
        self,
        book_id,
        title,
        edition,
        author,
        category,
        price
    ):

        if not book_id.get().strip():
            messagebox.showwarning(
                "Validation",
                "Please enter Book ID"
            )
            return

        if not title.get().strip():
            messagebox.showwarning(
                "Validation",
                "Please enter Book Title"
            )
            return

        if not category.get().strip():
            messagebox.showwarning(
                "Validation",
                "Please select Category"
            )
            return

        try:
            book_id_value = int(book_id.get())
            price_value = float(price.get()) if price.get() else 0

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Book ID must be an integer and Price must be a number."
            )
            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                INSERT INTO books
                (book_id, title, edition, author, category, price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                book_id_value,
                title.get(),
                edition.get(),
                author.get(),
                category.get(),
                price_value
            )

            cursor.execute(query, values)

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Book added successfully!"
            )

            self.add_book()

        except mysql.connector.IntegrityError:

            messagebox.showerror(
                "Error",
                "Book ID already exists."
            )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # MODIFY BOOK
    # ========================================================

    def modify_book(self):

        self.clear_window()

        self.create_title("MODIFY BOOK")

        frame = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Enter Book ID",
            font=("Arial", 14),
            bg="#f2f2f2"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        book_id_entry = tk.Entry(
            frame,
            font=("Arial", 14),
            width=25
        )

        book_id_entry.grid(
            row=0,
            column=1,
            padx=10
        )

        details_frame = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        details_frame.pack(pady=10)

        self.modify_details_frame = details_frame

        tk.Button(
            frame,
            text="Find",
            font=("Arial", 12, "bold"),
            command=lambda: self.find_book_for_modify(
                book_id_entry,
                details_frame
            )
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12),
            width=15,
            command=self.create_dashboard
        ).pack(pady=20)


    def find_book_for_modify(
        self,
        book_id_entry,
        details_frame
    ):

        for widget in details_frame.winfo_children():
            widget.destroy()

        if not book_id_entry.get().strip():

            messagebox.showwarning(
                "Validation",
                "Please enter Book ID."
            )

            return

        try:
            book_id = int(book_id_entry.get())

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Book ID must be an integer."
            )

            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT title, edition, author, category, price
                FROM books
                WHERE book_id = %s
                """,
                (book_id,)
            )

            book = cursor.fetchone()

            cursor.close()
            connection.close()

            if book is None:

                messagebox.showerror(
                    "Not Found",
                    "Book not found."
                )

                return

            title, old_edition, old_author, old_category, old_price = book

            edition = tk.StringVar(
                value=old_edition or ""
            )

            author = tk.StringVar(
                value=old_author or ""
            )

            category = tk.StringVar(
                value=old_category or ""
            )

            price = tk.StringVar(
                value=str(old_price or "")
            )

            tk.Label(
                details_frame,
                text=f"Book ID: {book_id}",
                font=("Arial", 14, "bold"),
                bg="#f2f2f2"
            ).grid(
                row=0,
                column=0,
                columnspan=2,
                pady=10
            )

            tk.Label(
                details_frame,
                text=f"Title: {title}",
                font=("Arial", 13),
                bg="#f2f2f2"
            ).grid(
                row=1,
                column=0,
                columnspan=2,
                pady=5
            )

            fields = [
                ("Edition", edition),
                ("Author", author),
                ("Price", price)
            ]

            for row, (label, variable) in enumerate(
                fields,
                start=2
            ):

                tk.Label(
                    details_frame,
                    text=label,
                    font=("Arial", 13),
                    bg="#f2f2f2"
                ).grid(
                    row=row,
                    column=0,
                    padx=10,
                    pady=8,
                    sticky="w"
                )

                tk.Entry(
                    details_frame,
                    textvariable=variable,
                    font=("Arial", 13),
                    width=25
                ).grid(
                    row=row,
                    column=1,
                    padx=10,
                    pady=8
                )

            # Category
            tk.Label(
                details_frame,
                text="Category",
                font=("Arial", 13),
                bg="#f2f2f2"
            ).grid(
                row=5,
                column=0,
                padx=10,
                pady=8,
                sticky="w"
            )

            ttk.Combobox(
                details_frame,
                textvariable=category,
                values=[
                    "CSE",
                    "ECE",
                    "MECH",
                    "DevOps"
                ],
                state="readonly",
                font=("Arial", 13),
                width=23
            ).grid(
                row=5,
                column=1,
                padx=10,
                pady=8
            )

            tk.Button(
                details_frame,
                text="Modify",
                font=("Arial", 12, "bold"),
                width=15,
                command=lambda: self.update_book(
                    book_id,
                    edition,
                    author,
                    category,
                    price
                )
            ).grid(
                row=6,
                column=0,
                columnspan=2,
                pady=15
            )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    def update_book(
        self,
        book_id,
        edition,
        author,
        category,
        price
    ):

        try:
            price_value = float(price.get())

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Price must be a number."
            )

            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE books
                SET edition = %s,
                    author = %s,
                    category = %s,
                    price = %s
                WHERE book_id = %s
            """

            values = (
                edition.get(),
                author.get(),
                category.get(),
                price_value,
                book_id
            )

            cursor.execute(query, values)

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Book modified successfully!"
            )

            self.modify_book()

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # DELETE BOOK
    # ========================================================

    def delete_book(self):

        self.clear_window()

        self.create_title("DELETE BOOK")

        frame = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Enter Book ID",
            font=("Arial", 14),
            bg="#f2f2f2"
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        book_id_entry = tk.Entry(
            frame,
            font=("Arial", 14),
            width=25
        )

        book_id_entry.grid(
            row=0,
            column=1,
            padx=10
        )

        details_frame = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        details_frame.pack(pady=20)

        tk.Button(
            frame,
            text="Find",
            font=("Arial", 12, "bold"),
            command=lambda: self.find_book_for_delete(
                book_id_entry,
                details_frame
            )
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12),
            width=15,
            command=self.create_dashboard
        ).pack(pady=20)


    def find_book_for_delete(
        self,
        book_id_entry,
        details_frame
    ):

        for widget in details_frame.winfo_children():
            widget.destroy()

        if not book_id_entry.get().strip():

            messagebox.showwarning(
                "Validation",
                "Please enter Book ID."
            )

            return

        try:
            book_id = int(book_id_entry.get())

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Book ID must be an integer."
            )

            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT book_id, title
                FROM books
                WHERE book_id = %s
                """,
                (book_id,)
            )

            book = cursor.fetchone()

            cursor.close()
            connection.close()

            if book is None:

                messagebox.showerror(
                    "Not Found",
                    "Book not found."
                )

                return

            found_id, title = book

            tk.Label(
                details_frame,
                text=f"Book ID: {found_id}",
                font=("Arial", 14, "bold"),
                bg="#f2f2f2"
            ).pack(pady=5)

            tk.Label(
                details_frame,
                text=f"Title: {title}",
                font=("Arial", 14),
                bg="#f2f2f2"
            ).pack(pady=5)

            tk.Label(
                details_frame,
                text="Do you want to delete this book?",
                font=("Arial", 14, "bold"),
                bg="#f2f2f2"
            ).pack(pady=15)

            button_frame = tk.Frame(
                details_frame,
                bg="#f2f2f2"
            )

            button_frame.pack()

            tk.Button(
                button_frame,
                text="Yes",
                font=("Arial", 12, "bold"),
                width=10,
                command=lambda: self.confirm_delete(
                    book_id
                )
            ).grid(
                row=0,
                column=0,
                padx=10
            )

            tk.Button(
                button_frame,
                text="No",
                font=("Arial", 12, "bold"),
                width=10,
                command=self.delete_book
            ).grid(
                row=0,
                column=1,
                padx=10
            )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    def confirm_delete(self, book_id):

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM books
                WHERE book_id = %s
                """,
                (book_id,)
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Book deleted successfully!"
            )

            self.delete_book()

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # STUDENT
    # ========================================================

    def student_page(self):

        self.clear_window()

        self.create_title("STUDENT")

        form = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        form.pack(pady=10)

        student_id = tk.StringVar()
        name = tk.StringVar()
        class_name = tk.StringVar()
        section = tk.StringVar()
        book_id = tk.StringVar()

        fields = [
            ("Student ID", student_id),
            ("Name", name),
            ("Class", class_name),
            ("Section", section),
            ("Book ID", book_id)
        ]

        for row, (label, variable) in enumerate(fields):

            tk.Label(
                form,
                text=label,
                font=("Arial", 13),
                bg="#f2f2f2"
            ).grid(
                row=row,
                column=0,
                padx=15,
                pady=8,
                sticky="w"
            )

            tk.Entry(
                form,
                textvariable=variable,
                font=("Arial", 13),
                width=30
            ).grid(
                row=row,
                column=1,
                padx=15,
                pady=8
            )

        tk.Button(
            self.root,
            text="Save",
            font=("Arial", 13, "bold"),
            width=15,
            command=lambda: self.save_student(
                student_id,
                name,
                class_name,
                section,
                book_id
            )
        ).pack(pady=10)

        # Search by title
        search_frame = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        search_frame.pack(pady=15)

        tk.Label(
            search_frame,
            text="Search Book Title",
            font=("Arial", 13),
            bg="#f2f2f2"
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        title_search = tk.Entry(
            search_frame,
            font=("Arial", 13),
            width=25
        )

        title_search.grid(
            row=0,
            column=1,
            padx=10
        )

        # Result area for title search (scrollable)
        title_result_container = tk.Frame(self.root, bg="#f2f2f2")
        title_result_container.pack(fill="both", expand=True, pady=10)

        title_result_canvas = tk.Canvas(title_result_container, bg="#f2f2f2", highlightthickness=0)
        title_result_scrollbar = tk.Scrollbar(title_result_container, orient="vertical", command=title_result_canvas.yview)
        title_result_canvas.configure(yscrollcommand=title_result_scrollbar.set)

        title_result_scrollbar.pack(side="right", fill="y")
        title_result_canvas.pack(side="left", fill="both", expand=True)

        title_result_frame = tk.Frame(title_result_canvas, bg="#f2f2f2")
        _title_result_window = title_result_canvas.create_window((0, 0), window=title_result_frame, anchor="nw")

        def _on_title_frame_config(event):
            title_result_canvas.configure(scrollregion=title_result_canvas.bbox("all"))
            title_result_canvas.itemconfig(_title_result_window, width=event.width)

        title_result_frame.bind("<Configure>", _on_title_frame_config)
        title_result_canvas.bind("<Configure>", lambda e: title_result_canvas.itemconfig(_title_result_window, width=e.width))

        # Allow inner grid column to expand
        title_result_frame.columnconfigure(1, weight=1)

        # Enable mousewheel scrolling on Windows and other platforms
        def _on_mousewheel(event):
            delta = 0
            try:
                delta = int(-1*(event.delta/120))
            except Exception:
                try:
                    delta = 1 if event.num == 5 else -1
                except Exception:
                    delta = 0
            title_result_canvas.yview_scroll(delta, "units")

        title_result_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        title_result_canvas.bind_all("<Button-4>", _on_mousewheel)
        title_result_canvas.bind_all("<Button-5>", _on_mousewheel)

        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 12, "bold"),
            command=lambda: self.search_title(
                title_search,
                title_result_frame
            )
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12),
            width=15,
            command=self.create_dashboard
        ).pack(pady=10)


    def save_student(
        self,
        student_id,
        name,
        class_name,
        section,
        book_id
    ):

        if not student_id.get().strip():
            messagebox.showwarning(
                "Validation",
                "Please enter Student ID."
            )
            return

        if not name.get().strip():
            messagebox.showwarning(
                "Validation",
                "Please enter Student Name."
            )
            return

        try:
            student_id_value = int(student_id.get())

            book_id_value = (
                int(book_id.get())
                if book_id.get().strip()
                else None
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Student ID and Book ID must be integers."
            )

            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            # Check book exists if Book ID entered
            if book_id_value is not None:

                cursor.execute(
                    """
                    SELECT book_id
                    FROM books
                    WHERE book_id = %s
                    """,
                    (book_id_value,)
                )

                if cursor.fetchone() is None:

                    messagebox.showerror(
                        "Error",
                        "Book ID does not exist."
                    )

                    cursor.close()
                    connection.close()

                    return

            query = """
                INSERT INTO students
                (student_id, name, class_name, section, book_id)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                student_id_value,
                name.get(),
                class_name.get(),
                section.get(),
                book_id_value
            )

            cursor.execute(query, values)

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Student saved successfully!"
            )

            self.student_page()

        except mysql.connector.IntegrityError:

            messagebox.showerror(
                "Error",
                "Student ID already exists."
            )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # SEARCH BOOK BY TITLE
    # ========================================================

    def search_title(self, title_search, result_frame):

        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()

        title = title_search.get().strip()

        if not title:

            messagebox.showwarning(
                "Validation",
                "Please enter book title."
            )

            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    b.book_id,
                    b.title,
                    b.edition,
                    b.author,
                    b.category,
                    b.price,
                    s.student_id
                FROM books b
                LEFT JOIN students s
                    ON b.book_id = s.book_id
                WHERE b.title LIKE %s
                """,
                (f"%{title}%",)
            )

            books = cursor.fetchall()

            cursor.close()
            connection.close()

            if not books:

                messagebox.showwarning(
                    "Book Availability",
                    "Book is not available in the database."
                )

                return

            # Display full details for each matching book
            for idx, book in enumerate(books):

                (
                    book_id,
                    found_title,
                    edition,
                    author,
                    category,
                    price,
                    student_id
                ) = book

                # Create a centered container for this result
                item_frame = tk.Frame(result_frame, bg="#f2f2f2")
                item_frame.pack(pady=10, anchor="center")

                tk.Label(
                    item_frame,
                    text=f"Result {idx+1}",
                    font=("Arial", 14, "bold"),
                    bg="#f2f2f2"
                ).grid(row=0, column=0, columnspan=2, pady=(0, 5))

                details = [
                    ("Book ID", book_id),
                    ("Title", found_title),
                    ("Edition", edition),
                    ("Author", author),
                    ("Category", category),
                    ("Price", price),
                    (
                        "Student ID",
                        student_id if student_id is not None else "Not Issued"
                    )
                ]

                for r, (label, value) in enumerate(details, start=1):

                    tk.Label(
                        item_frame,
                        text=f"{label}:",
                        font=("Arial", 13, "bold"),
                        bg="#f2f2f2",
                        anchor="e"
                    ).grid(row=r, column=0, padx=6, pady=2, sticky="e")

                    tk.Label(
                        item_frame,
                        text=str(value),
                        font=("Arial", 13),
                        bg="#f2f2f2",
                        anchor="w"
                    ).grid(row=r, column=1, padx=6, pady=2, sticky="w")

                # Let the value column expand a bit inside the item frame
                item_frame.columnconfigure(1, weight=1)

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    # ========================================================
    # SEARCH BOOK BY ID
    # ========================================================

    def search_book(self):

        self.clear_window()

        self.create_title("SEARCH BOOK")

        frame = tk.Frame(
            self.root,
            bg="#f2f2f2"
        )

        frame.pack(pady=20)

        tk.Label(
            frame,
            text="Enter Book ID",
            font=("Arial", 14),
            bg="#f2f2f2"
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        book_id_entry = tk.Entry(
            frame,
            font=("Arial", 14),
            width=25
        )

        book_id_entry.grid(
            row=0,
            column=1,
            padx=10
        )

        # Result area for search by ID (scrollable)
        result_container = tk.Frame(self.root, bg="#f2f2f2")
        result_container.pack(fill="both", expand=True, pady=20)

        result_canvas = tk.Canvas(result_container, bg="#f2f2f2", highlightthickness=0)
        result_scrollbar = tk.Scrollbar(result_container, orient="vertical", command=result_canvas.yview)
        result_canvas.configure(yscrollcommand=result_scrollbar.set)

        result_scrollbar.pack(side="right", fill="y")
        result_canvas.pack(side="left", fill="both", expand=True)

        result_frame = tk.Frame(result_canvas, bg="#f2f2f2")
        _result_window = result_canvas.create_window((0, 0), window=result_frame, anchor="nw")

        def _on_result_frame_config(event):
            result_canvas.configure(scrollregion=result_canvas.bbox("all"))
            result_canvas.itemconfig(_result_window, width=event.width)

        result_frame.bind("<Configure>", _on_result_frame_config)
        result_canvas.bind("<Configure>", lambda e: result_canvas.itemconfig(_result_window, width=e.width))

        def _on_mousewheel(event):
            delta = 0
            try:
                delta = int(-1*(event.delta/120))
            except Exception:
                try:
                    delta = 1 if event.num == 5 else -1
                except Exception:
                    delta = 0
            result_canvas.yview_scroll(delta, "units")

        result_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        result_canvas.bind_all("<Button-4>", _on_mousewheel)
        result_canvas.bind_all("<Button-5>", _on_mousewheel)

        # Allow inner grid column to expand
        result_frame.columnconfigure(1, weight=1)

        tk.Button(
            frame,
            text="Search",
            font=("Arial", 12, "bold"),
            command=lambda: self.search_book_by_id(
                book_id_entry,
                result_frame
            )
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        tk.Button(
            self.root,
            text="Back",
            font=("Arial", 12),
            width=15,
            command=self.create_dashboard
        ).pack(pady=20)


    def search_book_by_id(
        self,
        book_id_entry,
        result_frame
    ):

        for widget in result_frame.winfo_children():
            widget.destroy()

        if not book_id_entry.get().strip():

            messagebox.showwarning(
                "Validation",
                "Please enter Book ID."
            )

            return

        try:
            book_id = int(book_id_entry.get())

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Book ID must be an integer."
            )

            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    b.book_id,
                    b.title,
                    b.edition,
                    b.author,
                    b.category,
                    b.price,
                    s.student_id
                FROM books b
                LEFT JOIN students s
                    ON b.book_id = s.book_id
                WHERE b.book_id = %s
            """

            cursor.execute(
                query,
                (book_id,)
            )

            book = cursor.fetchone()

            cursor.close()
            connection.close()

            if book is None:

                messagebox.showwarning(
                    "Not Found",
                    "Book not found."
                )

                return

            (
                found_book_id,
                title,
                edition,
                author,
                category,
                price,
                student_id
            ) = book

            details = [
                ("Book ID", found_book_id),
                ("Title", title),
                ("Edition", edition),
                ("Author", author),
                ("Category", category),
                ("Price", price),
                (
                    "Student ID",
                    student_id
                    if student_id is not None
                    else "Not Issued"
                )
            ]

            for row, (label, value) in enumerate(details):

                tk.Label(
                    result_frame,
                    text=f"{label}:",
                    font=("Arial", 13, "bold"),
                    bg="#f2f2f2",
                    width=15,
                    anchor="w"
                ).grid(
                    row=row,
                    column=0,
                    padx=10,
                    pady=5
                )

                tk.Label(
                    result_frame,
                    text=str(value),
                    font=("Arial", 13),
                    bg="#f2f2f2",
                    width=30,
                    anchor="w"
                ).grid(
                    row=row,
                    column=1,
                    padx=10,
                    pady=5
                )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    # Create database
    create_database()

    # Create tables
    create_tables()

    # Start Tkinter
    root = tk.Tk()

    app = LibraryManagementSystem(root)

    root.mainloop()









