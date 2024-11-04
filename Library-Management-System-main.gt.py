import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
from datetime import datetime


class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("The Book Worm Library Management System")
        self.root.geometry("1200x800")
        self.current_user = None

        # Increase default font size
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=14)

        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="vellore",
                database="Library"
            )
            self.mycursor = self.mydb.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"Failed to connect to database: {err}")
            root.destroy()
            return

        self.create_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="The Book Worm", font=("Arial", 36, "bold")).pack(pady=40)
        tk.Button(self.root, text="Login as Admin", command=self.admin_login, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Login as User", command=self.user_login, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def admin_login(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Login", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Admin ID:", font=("Arial", 18)).pack()
        self.admin_id = tk.Entry(self.root, font=("Arial", 18))
        self.admin_id.pack(pady=10)
        tk.Label(self.root, text="Password:", font=("Arial", 18)).pack()
        self.admin_password = tk.Entry(self.root, show="*", font=("Arial", 18))
        self.admin_password.pack(pady=10)
        tk.Button(self.root, text="Login", command=self.verify_admin, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Back", command=self.create_main_menu, font=("Arial", 18), padx=20, pady=10).pack()

    def verify_admin(self):
        admin_id = self.admin_id.get()
        password = self.admin_password.get()
        self.mycursor.execute("SELECT Password FROM AdminRecord WHERE AdminID=%s", (admin_id,))
        result = self.mycursor.fetchone()
        if result and result[0] == password:
            self.current_user = admin_id
            self.admin_menu()
        else:
            messagebox.showerror("Error", "Invalid Admin ID or Password")

    def user_login(self):
        self.clear_window()
        tk.Label(self.root, text="User Login", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Button(self.root, text="Create Account", command=self.create_user_account, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Login", command=self.existing_user_login, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Back", command=self.create_main_menu, font=("Arial", 18), padx=20, pady=10).pack()

    def create_user_account(self):
        self.clear_window()
        tk.Label(self.root, text="Create User Account", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="User ID:", font=("Arial", 18)).pack()
        self.new_user_id = tk.Entry(self.root, font=("Arial", 18))
        self.new_user_id.pack(pady=10)
        tk.Label(self.root, text="User Name:", font=("Arial", 18)).pack()
        self.new_user_name = tk.Entry(self.root, font=("Arial", 18))
        self.new_user_name.pack(pady=10)
        tk.Label(self.root, text="Password:", font=("Arial", 18)).pack()
        self.new_user_password = tk.Entry(self.root, show="*", font=("Arial", 18))
        self.new_user_password.pack(pady=10)
        tk.Button(self.root, text="Create Account", command=self.save_new_user, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.user_login, font=("Arial", 18), padx=20, pady=10).pack()

    def save_new_user(self):
        user_id = self.new_user_id.get()
        user_name = self.new_user_name.get()
        password = self.new_user_password.get()
        try:
            self.mycursor.execute("INSERT INTO UserRecord (UserID, UserName, Password) VALUES (%s, %s, %s)",
                                  (user_id, user_name, password))
            self.mydb.commit()
            messagebox.showinfo("Success", "Account created successfully")
            self.user_login()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to create account: {err}")

    def existing_user_login(self):
        self.clear_window()
        tk.Label(self.root, text="User Login", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="User ID:", font=("Arial", 18)).pack()
        self.user_id = tk.Entry(self.root, font=("Arial", 18))
        self.user_id.pack(pady=10)
        tk.Label(self.root, text="Password:", font=("Arial", 18)).pack()
        self.user_password = tk.Entry(self.root, show="*", font=("Arial", 18))
        self.user_password.pack(pady=10)
        tk.Button(self.root, text="Login", command=self.verify_user, font=("Arial", 18), padx=20, pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.user_login, font=("Arial", 18), padx=20, pady=10).pack()

    def verify_user(self):
        user_id = self.user_id.get()
        password = self.user_password.get()
        self.mycursor.execute("SELECT Password FROM UserRecord WHERE UserID=%s", (user_id,))
        result = self.mycursor.fetchone()
        if result and result[0] == password:
            self.current_user = user_id
            self.user_menu()
        else:
            messagebox.showerror("Error", "Invalid User ID or Password")

    def admin_menu(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome, Admin {self.current_user}", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Button(self.root, text="Book Management", command=self.book_management, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="User Management", command=self.user_management, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Admin Management", command=self.admin_management, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="View Feedback", command=self.view_feedback, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Logout", command=self.logout, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def user_menu(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome, User {self.current_user}", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Button(self.root, text="Book Centre", command=self.book_centre, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Give Feedback", command=self.give_feedback, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Logout", command=self.logout, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def logout(self):
        self.current_user = None
        self.create_main_menu()

    def book_management(self):
        self.clear_window()
        tk.Label(self.root, text="Book Management", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Button(self.root, text="Add Book", command=self.add_book, font=("Arial", 18), padx=20, pady=10).pack(pady=20)
        tk.Button(self.root, text="Display All Books", command=self.display_all_books, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Display Available Books", command=self.display_available_books, font=("Arial", 18),
                  padx=20, pady=10).pack(pady=20)
        tk.Button(self.root, text="Search Book", command=self.search_book, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Delete Book", command=self.delete_book, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Update Book", command=self.update_book, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Back", command=self.admin_menu, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def add_book(self):
        self.clear_window()
        tk.Label(self.root, text="Add Book", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Book ID:", font=("Arial", 18)).pack()
        self.book_id = tk.Entry(self.root, font=("Arial", 18))
        self.book_id.pack(pady=10)
        tk.Label(self.root, text="Book Name:", font=("Arial", 18)).pack()
        self.book_name = tk.Entry(self.root, font=("Arial", 18))
        self.book_name.pack(pady=10)
        tk.Label(self.root, text="Author:", font=("Arial", 18)).pack()
        self.author = tk.Entry(self.root, font=("Arial", 18))
        self.author.pack(pady=10)
        tk.Label(self.root, text="Publisher:", font=("Arial", 18)).pack()
        self.publisher = tk.Entry(self.root, font=("Arial", 18))
        self.publisher.pack(pady=10)
        tk.Button(self.root, text="Add Book", command=self.save_book, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Back", command=self.book_management, font=("Arial", 18), padx=20, pady=10).pack()

    def save_book(self):
        book_id = self.book_id.get()
        book_name = self.book_name.get()
        author = self.author.get()
        publisher = self.publisher.get()
        try:
            self.mycursor.execute("INSERT INTO BookRecord VALUES (%s, %s, %s, %s)",
                                  (book_id, book_name, author, publisher))
            self.mydb.commit()
            messagebox.showinfo("Success", "Book added successfully")
            self.book_management()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add book: {err}")

    def display_all_books(self):
        self.clear_window()
        tk.Label(self.root, text="All Books", font=("Arial", 32, "bold")).pack(pady=40)

        # Create a frame for the book entries
        book_frame = tk.Frame(self.root)
        book_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(book_frame)
        scrollbar = tk.Scrollbar(book_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.mycursor.execute("""
            SELECT BookRecord.*, 
                   CASE WHEN IssuedBooks.BookID IS NOT NULL THEN 'Issued' ELSE 'Available' END AS Status
            FROM BookRecord
            LEFT JOIN IssuedBooks ON BookRecord.BookID = IssuedBooks.BookID
        """)
        records = self.mycursor.fetchall()
        for i, (book_id, book_name, author, publisher, status) in enumerate(records, 1):
            tk.Label(scrollable_frame, text=f"Book {i}:", font=("Arial", 18, "bold")).pack(anchor="w", pady=(20, 0))
            tk.Label(scrollable_frame, text=f"ID: {book_id}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Name: {book_name}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Author: {author}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Publisher: {publisher}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Status: {status}", font=("Arial", 14)).pack(anchor="w")
            ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Back", command=self.book_management, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)

    def display_available_books(self):
        self.clear_window()
        tk.Label(self.root, text="Available Books", font=("Arial", 32, "bold")).pack(pady=40)

        # Create a frame for the book entries
        book_frame = tk.Frame(self.root)
        book_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(book_frame)
        scrollbar = tk.Scrollbar(book_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.mycursor.execute("""
            SELECT BookRecord.* 
            FROM BookRecord
            LEFT JOIN IssuedBooks ON BookRecord.BookID = IssuedBooks.BookID
            WHERE IssuedBooks.BookID IS NULL
        """)
        records = self.mycursor.fetchall()
        for i, (book_id, book_name, author, publisher) in enumerate(records, 1):
            tk.Label(scrollable_frame, text=f"Book {i}:", font=("Arial", 18, "bold")).pack(anchor="w", pady=(20, 0))
            tk.Label(scrollable_frame, text=f"ID: {book_id}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Name: {book_name}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Author: {author}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Publisher: {publisher}", font=("Arial", 14)).pack(anchor="w")
            ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Back", command=self.book_management, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)

    def search_book(self):
        self.clear_window()
        tk.Label(self.root, text="Search Book", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter Book ID:", font=("Arial", 18)).pack()
        self.search_book_id = tk.Entry(self.root, font=("Arial", 18))
        self.search_book_id.pack(pady=10)
        tk.Button(self.root, text="Search", command=self.perform_book_search, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.book_management, font=("Arial", 18), padx=20, pady=10).pack()

    def perform_book_search(self):
        book_id = self.search_book_id.get()
        self.mycursor.execute("SELECT * FROM BookRecord WHERE BookID=%s", (book_id,))
        result = self.mycursor.fetchone()
        if result:
            messagebox.showinfo("Book Found",
                                f"ID: {result[0]}\nName: {result[1]}\nAuthor: {result[2]}\nPublisher: {result[3]}")
        else:
            messagebox.showerror("Error", "Book not found")

    def delete_book(self):
        self.clear_window()
        tk.Label(self.root, text="Delete Book", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter Book ID:", font=("Arial", 18)).pack()
        self.delete_book_id = tk.Entry(self.root, font=("Arial", 18))
        self.delete_book_id.pack(pady=10)
        tk.Button(self.root, text="Delete", command=self.perform_book_delete, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.book_management, font=("Arial", 18), padx=20, pady=10).pack()

    def perform_book_delete(self):
        book_id = self.delete_book_id.get()
        try:
            self.mycursor.execute("DELETE FROM BookRecord WHERE BookID=%s", (book_id,))
            self.mydb.commit()
            messagebox.showinfo("Success", "Book deleted successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete book: {err}")

    def update_book(self):
        self.clear_window()
        tk.Label(self.root, text="Update Book", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter Book ID:", font=("Arial", 18)).pack()
        self.update_book_id = tk.Entry(self.root, font=("Arial", 18))
        self.update_book_id.pack(pady=10)
        tk.Button(self.root, text="Search", command=self.show_update_book_form, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.book_management, font=("Arial", 18), padx=20, pady=10).pack()

    def show_update_book_form(self):
        book_id = self.update_book_id.get()
        self.mycursor.execute("SELECT * FROM BookRecord WHERE BookID=%s", (book_id,))
        result = self.mycursor.fetchone()
        if result:
            self.clear_window()
            tk.Label(self.root, text="Update Book", font=("Arial", 32, "bold")).pack(pady=40)
            tk.Label(self.root, text="Book Name:", font=("Arial", 18)).pack()
            self.update_book_name = tk.Entry(self.root, font=("Arial", 18))
            self.update_book_name.insert(0, result[1])
            self.update_book_name.pack(pady=10)
            tk.Label(self.root, text="Author:", font=("Arial", 18)).pack()
            self.update_author = tk.Entry(self.root, font=("Arial", 18))
            self.update_author.insert(0, result[2])
            self.update_author.pack(pady=10)
            tk.Label(self.root, text="Publisher:", font=("Arial", 18)).pack()
            self.update_publisher = tk.Entry(self.root, font=("Arial", 18))
            self.update_publisher.insert(0, result[3])
            self.update_publisher.pack(pady=10)
            tk.Button(self.root, text="Update", command=lambda: self.perform_book_update(book_id), font=("Arial", 18),
                      padx=20, pady=10).pack(pady=20)
            tk.Button(self.root, text="Back", command=self.update_book, font=("Arial", 18), padx=20, pady=10).pack()
        else:
            messagebox.showerror("Error", "Book not found")

    def perform_book_update(self, book_id):
        book_name = self.update_book_name.get()
        author = self.update_author.get()
        publisher = self.update_publisher.get()
        try:
            self.mycursor.execute("UPDATE BookRecord SET BookName=%s, Author=%s, Publisher=%s WHERE BookID=%s",
                                  (book_name, author, publisher, book_id))
            self.mydb.commit()
            messagebox.showinfo("Success", "Book updated successfully")
            self.book_management()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update book: {err}")

    def user_management(self):
        self.clear_window()
        tk.Label(self.root, text="User Management", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Button(self.root, text="Display Users", command=self.display_users, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Search User", command=self.search_user, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Delete User", command=self.delete_user, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Update User", command=self.update_user, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Back", command=self.admin_menu, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def display_users(self):
        self.clear_window()
        tk.Label(self.root, text="User Records", font=("Arial", 32, "bold")).pack(pady=40)

        # Create a frame for the user entries
        user_frame = tk.Frame(self.root)
        user_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(user_frame)
        scrollbar = tk.Scrollbar(user_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.mycursor.execute("SELECT UserID, UserName FROM UserRecord")
        records = self.mycursor.fetchall()
        for i, (user_id, user_name) in enumerate(records, 1):
            tk.Label(scrollable_frame, text=f"User {i}:", font=("Arial", 18, "bold")).pack(anchor="w", pady=(20, 0))
            tk.Label(scrollable_frame, text=f"ID: {user_id}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Name: {user_name}", font=("Arial", 14)).pack(anchor="w")
            ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Back", command=self.user_management, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)

    def search_user(self):
        self.clear_window()
        tk.Label(self.root, text="Search User", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter User ID:", font=("Arial", 18)).pack()
        self.search_user_id = tk.Entry(self.root, font=("Arial", 18))
        self.search_user_id.pack(pady=10)
        tk.Button(self.root, text="Search", command=self.perform_user_search, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.user_management, font=("Arial", 18), padx=20, pady=10).pack()

    def perform_user_search(self):
        user_id = self.search_user_id.get()
        self.mycursor.execute("SELECT UserID, UserName FROM UserRecord WHERE UserID=%s", (user_id,))
        result = self.mycursor.fetchone()
        if result:
            messagebox.showinfo("User Found", f"ID: {result[0]}\nName: {result[1]}")
        else:
            messagebox.showerror("Error", "User not found")

    def delete_user(self):
        self.clear_window()
        tk.Label(self.root, text="Delete User", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter User ID:", font=("Arial", 18)).pack()
        self.delete_user_id = tk.Entry(self.root, font=("Arial", 18))
        self.delete_user_id.pack(pady=10)
        tk.Button(self.root, text="Delete", command=self.perform_user_delete, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.user_management, font=("Arial", 18), padx=20, pady=10).pack()

    def perform_user_delete(self):
        user_id = self.delete_user_id.get()
        try:
            self.mycursor.execute("DELETE FROM UserRecord WHERE UserID=%s", (user_id,))
            self.mydb.commit()
            messagebox.showinfo("Success", "User deleted successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete user: {err}")

    def update_user(self):
        self.clear_window()
        tk.Label(self.root, text="Update User", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter User ID:", font=("Arial", 18)).pack()
        self.update_user_id = tk.Entry(self.root, font=("Arial", 18))
        self.update_user_id.pack(pady=10)
        tk.Button(self.root, text="Search", command=self.show_update_user_form, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.user_management, font=("Arial", 18), padx=20, pady=10).pack()

    def show_update_user_form(self):
        user_id = self.update_user_id.get()
        self.mycursor.execute("SELECT UserID, UserName FROM UserRecord WHERE UserID=%s", (user_id,))
        result = self.mycursor.fetchone()
        if result:
            self.clear_window()
            tk.Label(self.root, text="Update User", font=("Arial", 32, "bold")).pack(pady=40)
            tk.Label(self.root, text="User Name:", font=("Arial", 18)).pack()
            self.update_user_name = tk.Entry(self.root, font=("Arial", 18))
            self.update_user_name.insert(0, result[1])
            self.update_user_name.pack(pady=10)
            tk.Label(self.root, text="New Password:", font=("Arial", 18)).pack()
            self.update_user_password = tk.Entry(self.root, show="*", font=("Arial", 18))
            self.update_user_password.pack(pady=10)
            tk.Button(self.root, text="Update", command=lambda: self.perform_user_update(user_id), font=("Arial", 18),
                      padx=20, pady=10).pack(pady=20)
            tk.Button(self.root, text="Back", command=self.update_user, font=("Arial", 18), padx=20, pady=10).pack()
        else:
            messagebox.showerror("Error", "User not found")

    def perform_user_update(self, user_id):
        user_name = self.update_user_name.get()
        password = self.update_user_password.get()
        try:
            if password:
                self.mycursor.execute("UPDATE UserRecord SET UserName=%s, Password=%s WHERE UserID=%s",
                                      (user_name, password, user_id))
            else:
                self.mycursor.execute("UPDATE UserRecord SET UserName=%s WHERE UserID=%s",
                                      (user_name, user_id))
            self.mydb.commit()
            messagebox.showinfo("Success", "User updated successfully")
            self.user_management()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update user: {err}")

    def admin_management(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Management", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Button(self.root, text="Add Admin", command=self.add_admin, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Display Admins", command=self.display_admins, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Delete Admin", command=self.delete_admin, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Update Admin", command=self.update_admin, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Back", command=self.admin_menu, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def add_admin(self):
        self.clear_window()
        tk.Label(self.root, text="Add Admin", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Admin ID:", font=("Arial", 18)).pack()
        self.new_admin_id = tk.Entry(self.root, font=("Arial", 18))
        self.new_admin_id.pack(pady=10)
        tk.Label(self.root, text="Password:", font=("Arial", 18)).pack()
        self.new_admin_password = tk.Entry(self.root, show="*", font=("Arial", 18))
        self.new_admin_password.pack(pady=10)
        tk.Button(self.root, text="Add Admin", command=self.save_new_admin, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Back", command=self.admin_management, font=("Arial", 18), padx=20, pady=10).pack()

    def save_new_admin(self):
        admin_id = self.new_admin_id.get()
        password = self.new_admin_password.get()
        try:
            self.mycursor.execute("INSERT INTO AdminRecord (AdminID, Password) VALUES (%s, %s)",
                                  (admin_id, password))
            self.mydb.commit()
            messagebox.showinfo("Success", "Admin added successfully")
            self.admin_management()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add admin: {err}")

    def display_admins(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Records", font=("Arial", 32, "bold")).pack(pady=40)

        # Create a frame for the admin entries
        admin_frame = tk.Frame(self.root)
        admin_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(admin_frame)
        scrollbar = tk.Scrollbar(admin_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        try:
            self.mycursor.execute("SELECT AdminID FROM AdminRecord")
            records = self.mycursor.fetchall()
            for i, (admin_id,) in enumerate(records, 1):
                tk.Label(scrollable_frame, text=f"Admin {i}:", font=("Arial", 18, "bold")).pack(anchor="w",
                                                                                                pady=(20, 0))
                tk.Label(scrollable_frame, text=f"ID: {admin_id}", font=("Arial", 14)).pack(anchor="w")
                ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)

            if not records:
                tk.Label(scrollable_frame, text="No admin records found.", font=("Arial", 14)).pack(pady=20)

        except mysql.connector.Error as err:
            tk.Label(scrollable_frame, text=f"Error: {err}", font=("Arial", 14, "bold"), fg="red").pack(pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Back", command=self.admin_management, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)

    def delete_admin(self):
        self.clear_window()
        tk.Label(self.root, text="Delete Admin", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter Admin ID:", font=("Arial", 18)).pack()
        self.delete_admin_id = tk.Entry(self.root, font=("Arial", 18))
        self.delete_admin_id.pack(pady=10)
        tk.Button(self.root, text="Delete", command=self.perform_admin_delete, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.admin_management, font=("Arial", 18), padx=20, pady=10).pack()

    def perform_admin_delete(self):
        admin_id = self.delete_admin_id.get()
        try:
            self.mycursor.execute("DELETE FROM AdminRecord WHERE AdminID=%s", (admin_id,))
            self.mydb.commit()
            messagebox.showinfo("Success", "Admin deleted successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete admin: {err}")

    def update_admin(self):
        self.clear_window()
        tk.Label(self.root, text="Update Admin", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Enter Admin ID:", font=("Arial", 18)).pack()
        self.update_admin_id = tk.Entry(self.root, font=("Arial", 18))
        self.update_admin_id.pack(pady=10)
        tk.Button(self.root, text="Search", command=self.show_update_admin_form, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.admin_management, font=("Arial", 18), padx=20, pady=10).pack()

    def show_update_admin_form(self):
        admin_id = self.update_admin_id.get()
        self.mycursor.execute("SELECT AdminID FROM AdminRecord WHERE AdminID=%s", (admin_id,))
        result = self.mycursor.fetchone()
        if result:
            self.clear_window()
            tk.Label(self.root, text="Update Admin", font=("Arial", 32, "bold")).pack(pady=40)
            tk.Label(self.root, text="New Password:", font=("Arial", 18)).pack()
            self.update_admin_password = tk.Entry(self.root, show="*", font=("Arial", 18))
            self.update_admin_password.pack(pady=10)
            tk.Button(self.root, text="Update", command=lambda: self.perform_admin_update(admin_id), font=("Arial", 18),
                      padx=20, pady=10).pack(pady=20)
            tk.Button(self.root, text="Back", command=self.update_admin, font=("Arial", 18), padx=20, pady=10).pack()
        else:
            messagebox.showerror("Error", "Admin not found")

    def perform_admin_update(self, admin_id):
        password = self.update_admin_password.get()
        try:
            self.mycursor.execute("UPDATE AdminRecord SET Password=%s WHERE AdminID=%s",
                                  (password, admin_id))
            self.mydb.commit()
            messagebox.showinfo("Success", "Admin updated successfully")
            self.admin_management()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update admin: {err}")

    def book_centre(self):
        self.clear_window()
        tk.Label(self.root, text="Book Centre", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Button(self.root, text="Issue Book", command=self.issue_book, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Return Book", command=self.return_book, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="View Issued Books", command=self.view_issued_books, font=("Arial", 18), padx=20,
                  pady=10).pack(pady=20)
        tk.Button(self.root, text="View Available Books", command=self.view_available_books, font=("Arial", 18),
                  padx=20, pady=10).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.user_menu, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def view_available_books(self):
        self.clear_window()
        tk.Label(self.root, text="Available Books", font=("Arial", 32, "bold")).pack(pady=40)

        # Create a frame for the book entries
        book_frame = tk.Frame(self.root)
        book_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(book_frame)
        scrollbar = tk.Scrollbar(book_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        try:
            self.mycursor.execute("""
                SELECT BookRecord.* 
                FROM BookRecord
                LEFT JOIN IssuedBooks ON BookRecord.BookID = IssuedBooks.BookID
                WHERE IssuedBooks.BookID IS NULL
            """)
            records = self.mycursor.fetchall()

            if records:
                for i, (book_id, book_name, author, publisher) in enumerate(records, 1):
                    tk.Label(scrollable_frame, text=f"Book {i}:", font=("Arial", 18, "bold")).pack(anchor="w",
                                                                                                   pady=(20, 0))
                    tk.Label(scrollable_frame, text=f"ID: {book_id}", font=("Arial", 14)).pack(anchor="w")
                    tk.Label(scrollable_frame, text=f"Name: {book_name}", font=("Arial", 14)).pack(anchor="w")
                    tk.Label(scrollable_frame, text=f"Author: {author}", font=("Arial", 14)).pack(anchor="w")
                    tk.Label(scrollable_frame, text=f"Publisher: {publisher}", font=("Arial", 14)).pack(anchor="w")
                    ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
            else:
                tk.Label(scrollable_frame, text="No available books at the moment.", font=("Arial", 14)).pack(pady=20)

        except mysql.connector.Error as err:
            tk.Label(scrollable_frame, text=f"Error: {err}", font=("Arial", 14, "bold"), fg="red").pack(pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Back", command=self.book_centre, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def issue_book(self):
        self.clear_window()
        tk.Label(self.root, text="Issue Book", font=("Arial", 32, "bold")).pack(pady=40)

        # Check if the user already has an issued book
        self.mycursor.execute("SELECT COUNT(*) FROM IssuedBooks WHERE UserID = %s", (self.current_user,))
        issued_count = self.mycursor.fetchone()[0]

        if issued_count > 0:
            tk.Label(self.root, text="You already have a book issued. Please return it before issuing another.",
                     font=("Arial", 18), wraplength=800).pack(pady=20)
        else:
            tk.Label(self.root, text="Enter Book ID:", font=("Arial", 18)).pack()
            self.issue_book_id = tk.Entry(self.root, font=("Arial", 18))
            self.issue_book_id.pack(pady=10)
            tk.Button(self.root, text="Issue", command=self.perform_book_issue, font=("Arial", 18), padx=20,
                      pady=10).pack(pady=20)

        tk.Button(self.root, text="Back", command=self.book_centre, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def perform_book_issue(self):
        book_id = self.issue_book_id.get()
        try:
            # Check if the user already has an issued book
            self.mycursor.execute("SELECT COUNT(*) FROM IssuedBooks WHERE UserID = %s", (self.current_user,))
            issued_count = self.mycursor.fetchone()[0]

            if issued_count > 0:
                messagebox.showerror("Error",
                                     "You already have a book issued. Please return it before issuing another.")
                return

            # Check if the book exists and is available
            self.mycursor.execute("SELECT * FROM BookRecord WHERE BookID = %s", (book_id,))
            book = self.mycursor.fetchone()
            if book:
                self.mycursor.execute("SELECT * FROM IssuedBooks WHERE BookID = %s", (book_id,))
                if self.mycursor.fetchone():
                    messagebox.showerror("Error", "This book is already issued to someone else")
                else:
                    self.mycursor.execute("INSERT INTO IssuedBooks (BookID, UserID, IssueDate) VALUES (%s, %s, %s)",
                                          (book_id, self.current_user, datetime.now().date()))
                    self.mydb.commit()
                    messagebox.showinfo("Success", "Book issued successfully")
                    self.book_centre()
            else:
                messagebox.showerror("Error", "Book not found")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to issue book: {err}")

    def return_book(self):
        self.clear_window()
        tk.Label(self.root, text="Return Book", font=("Arial", 32, "bold")).pack(pady=40)

        # Check if the user has any issued books
        self.mycursor.execute("SELECT BookID FROM IssuedBooks WHERE UserID = %s", (self.current_user,))
        issued_book = self.mycursor.fetchone()

        if issued_book:
            book_id = issued_book[0]
            self.mycursor.execute("SELECT BookName FROM BookRecord WHERE BookID = %s", (book_id,))
            book_name = self.mycursor.fetchone()[0]
            tk.Label(self.root, text=f"You have issued: {book_name} (ID: {book_id})", font=("Arial", 18),
                     wraplength=800).pack(pady=20)
            tk.Button(self.root, text="Return Book", command=self.perform_book_return, font=("Arial", 18), padx=20,
                      pady=10).pack(pady=20)
        else:
            tk.Label(self.root, text="You don't have any books issued.", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Back", command=self.book_centre, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def perform_book_return(self):
        try:
            self.mycursor.execute("SELECT BookID FROM IssuedBooks WHERE UserID = %s", (self.current_user,))
            issued_book = self.mycursor.fetchone()
            if issued_book:
                book_id = issued_book[0]
                self.mycursor.execute("DELETE FROM IssuedBooks WHERE BookID = %s AND UserID = %s",
                                      (book_id, self.current_user))
                self.mydb.commit()
                messagebox.showinfo("Success", "Book returned successfully")
            else:
                messagebox.showerror("Error", "You don't have any books issued")
            self.book_centre()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to return book: {err}")

    def view_issued_books(self):
        self.clear_window()
        tk.Label(self.root, text="Your Issued Books", font=("Arial", 32, "bold")).pack(pady=40)

        # Create a frame for the book entries
        book_frame = tk.Frame(self.root)
        book_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(book_frame)
        scrollbar = tk.Scrollbar(book_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        try:
            self.mycursor.execute("""
                SELECT BookRecord.BookID, BookRecord.BookName, BookRecord.Author, IssuedBooks.IssueDate
                FROM IssuedBooks
                JOIN BookRecord ON IssuedBooks.BookID = BookRecord.BookID
                WHERE IssuedBooks.UserID = %s
            """, (self.current_user,))
            records = self.mycursor.fetchall()

            if records:
                for i, (book_id, book_name, author, issue_date) in enumerate(records, 1):
                    tk.Label(scrollable_frame, text=f"Book {i}:", font=("Arial", 18, "bold")).pack(anchor="w",
                                                                                                   pady=(20, 0))
                    tk.Label(scrollable_frame, text=f"ID: {book_id}", font=("Arial", 14)).pack(anchor="w")
                    tk.Label(scrollable_frame, text=f"Name: {book_name}", font=("Arial", 14)).pack(anchor="w")
                    tk.Label(scrollable_frame, text=f"Author: {author}", font=("Arial", 14)).pack(anchor="w")
                    tk.Label(scrollable_frame, text=f"Issue Date: {issue_date}", font=("Arial", 14)).pack(anchor="w")
                    ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
            else:
                tk.Label(scrollable_frame, text="You have no books issued at the moment.", font=("Arial", 14)).pack(
                    pady=20)

        except mysql.connector.Error as err:
            tk.Label(scrollable_frame, text=f"Error: {err}", font=("Arial", 14, "bold"), fg="red").pack(pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Back", command=self.book_centre, font=("Arial", 18), padx=20, pady=10).pack(pady=20)

    def give_feedback(self):
        self.clear_window()
        tk.Label(self.root, text="Give Feedback", font=("Arial", 32, "bold")).pack(pady=40)
        tk.Label(self.root, text="Your feedback:", font=("Arial", 18)).pack()
        self.feedback_text = tk.Text(self.root, height=10, width=60, font=("Arial", 14))
        self.feedback_text.pack(pady=20)
        tk.Button(self.root, text="Submit", command=self.submit_feedback, font=("Arial", 18), padx=20, pady=10).pack(
            pady=20)
        tk.Button(self.root, text="Back", command=self.user_menu, font=("Arial", 18), padx=20, pady=10).pack()

    def submit_feedback(self):
        feedback = self.feedback_text.get("1.0", "end-1c")
        try:
            self.mycursor.execute("INSERT INTO Feedback (FeedbackText, SubmissionDate) VALUES (%s, %s)",
                                  (feedback, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.mydb.commit()
            messagebox.showinfo("Success", "Thank you for your feedback!")
            self.user_menu()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to submit feedback: {err}")

    def view_feedback(self):
        self.clear_window()
        tk.Label(self.root, text="View Feedback", font=("Arial", 32, "bold")).pack(pady=40)

        # Create a frame for the feedback entries
        feedback_frame = tk.Frame(self.root)
        feedback_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(feedback_frame)
        scrollbar = tk.Scrollbar(feedback_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.mycursor.execute("SELECT FeedbackText, SubmissionDate FROM Feedback ORDER BY SubmissionDate DESC")
        records = self.mycursor.fetchall()
        for i, (feedback_text, submission_date) in enumerate(records, 1):
            tk.Label(scrollable_frame, text=f"Feedback {i}:", font=("Arial", 18, "bold")).pack(anchor="w", pady=(20, 0))
            tk.Label(scrollable_frame, text=f"Date: {submission_date}", font=("Arial", 14)).pack(anchor="w")
            tk.Label(scrollable_frame, text=f"Feedback: {feedback_text}", font=("Arial", 14), wraplength=500).pack(
                anchor="w")
            ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Back", command=self.admin_menu, font=("Arial", 18), padx=20, pady=10).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()