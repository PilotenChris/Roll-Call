import os.path
import re
import sqlite3
import tkinter as tk
from tkinter import ttk
import bcrypt
from validator_collection import checkers
from Person import Person
from Student import Student
from Teacher import Teacher
from Admin import Admin
from Course import Course
from Grade import Grade
from typing import Union

# Constant for database file path
DBFILE: str = "roll_call.db"

# Font style for labels in application
custom_font1: tuple = ("Helvetica", 15)
custom_font2: tuple = ("Helvetica", 13)

# Current logged-in user, instance of type Person (Student, Teacher, Admin)
user: Union[Person, Student, Teacher, Admin]


def main() -> None:
    # Check if database file exists, if not create new database
    if not os.path.isfile(DBFILE):
        create_database()

    # Login or Create account
    start()


# Function to create the database with the required Tables and Fields
# And inserts the required starting data
def create_database() -> None:
    con = sqlite3.connect(DBFILE)
    cur = con.cursor()

    # Create the table Account in the Database with required fields
    cur.execute("CREATE TABLE Account(AccountId INTEGER NOT NULL UNIQUE," +
                "AccountType TEXT NOT NULL UNIQUE," +
                "PRIMARY KEY(AccountId AUTOINCREMENT))")

    # Create the table User in the Database with required fields
    cur.execute("CREATE TABLE User(Id INTEGER UNIQUE," +
                "FirstName TEXT NOT NULL, Surname TEXT NOT NULL, Birth TEXT NOT NULL," +
                "Email TEXT NOT NULL UNIQUE, UniEmail TEXT," +
                "Password TEXT NOT NULL, Account INTEGER," +
                "PRIMARY KEY(Id AUTOINCREMENT)," +
                "FOREIGN KEY(Account) REFERENCES Account(AccountId))")

    # Create the table Degrees in the Database with required fields
    cur.execute("CREATE TABLE Degrees(DegreeId INTEGER NOT NULL UNIQUE," +
                "DegreeName TEXT NOT NULL," +
                "PRIMARY KEY(DegreeId AUTOINCREMENT))")

    # Create the table Degree in the Database with required fields
    cur.execute("CREATE TABLE Degree(UserId INTEGER NOT NULL," +
                "DegreeId INTEGER NOT NULL," +
                "FOREIGN KEY(UserId) REFERENCES User(Id)," +
                "FOREIGN KEY(DegreeId) REFERENCES Degrees(DegreeId)," +
                "PRIMARY KEY(UserId))")

    # Create the table Course in the Database with required fields
    cur.execute("CREATE TABLE Course(CourseId INTEGER NOT NULL UNIQUE," +
                "CourseName TEXT NOT NULL," +
                "PassingGrade INTEGER NOT NULL," +
                "PRIMARY KEY(CourseId AUTOINCREMENT))")

    # Create the table Grade in the Database with required fields
    cur.execute("CREATE TABLE Grade(UserId INTEGER NOT NULL," +
                "CourseId INTEGER NOT NULL," +
                "Task INTEGER NOT NULL," +
                "Grade INTEGER NOT NULL," +
                "FOREIGN KEY(CourseId) REFERENCES Course(CourseId)," +
                "FOREIGN KEY(UserId) REFERENCES User(Id)," +
                "PRIMARY KEY(UserId, CourseId, Task))")

    # Create the table Classes in the Database with required fields
    cur.execute("CREATE TABLE Classes(UserId INTEGER NOT NULL," +
                "Course INTEGER NOT NULL," +
                "FOREIGN KEY(Course) REFERENCES Course(CourseId)," +
                "FOREIGN KEY(UserId) REFERENCES User(Id)," +
                "PRIMARY KEY(UserId, Course))")

    # Triggers to automatically set the UniEmail and Account field upon new user insertion
    cur.execute("CREATE TRIGGER CreateUniEmail AFTER INSERT ON User " + "\n" +
                "BEGIN " + "\n" +
                "UPDATE User SET UniEmail = NEW.Id || '@idkUniversity.com' WHERE Id = NEW.Id;" + "\n" +
                "END;")

    # Trigger to automatically assign the default account type to new users
    cur.execute("CREATE TRIGGER AssignUser AFTER INSERT ON User " + "\n" +
                "BEGIN " + "\n" +
                "UPDATE User SET Account = 1 WHERE Id = NEW.Id;" + "\n" +
                "END;")

    # Insert the default data into table Account
    cur.execute("INSERT INTO Account (AccountType) VALUES ('Student')," +
                "('Teacher'), ('Admin')")

    # Commit changes and close the database connection
    con.commit()
    con.close()


# Checks the login credentials, retrieves user details from the database and initializes the global user object based on the role (Student, Teacher, Admin)
def check_login(email: str, password: bytes) -> bool:
    # Connect to the database and go through User to find password by email
    with sqlite3.connect(DBFILE) as db:
        cur = db.cursor()
        cur.execute("SELECT Password, id FROM User WHERE Email = ?", (email,))
        # If you found the Email, put password in the result, else put None in the result
        result = cur.fetchone()

        # If the result is None, then the Email was wrong, and return False
        if result is None:
            return False

        # Extract stored password and user ID from the result
        stored_hash_password = result[0]
        stored_id = result[1]

        # Retrieve additional user details based on the user ID
        cur.execute("SELECT FirstName, Surname, Birth, Email, UniEmail, Account FROM User WHERE Id = ?", (stored_id,))
        person_result = cur.fetchone()
        global user

        # Check the user's account type and initialize the corresponding object
        if person_result[5] == 1:
            print("1")
            user = Student(stored_id, person_result[0], person_result[1], person_result[2], person_result[3],
                           person_result[4], "", [], [])
            print(user)
        elif person_result[5] == 2:
            print("2")
            user = Teacher(stored_id, person_result[0], person_result[1], person_result[2], person_result[3],
                           person_result[4], [])
        elif person_result[5] == 3:
            print("3")
            user = Admin(stored_id, person_result[0], person_result[1], person_result[2], person_result[3],
                         person_result[4])

        # Check and return true if the password is correct, else return false
        return bcrypt.checkpw(password, stored_hash_password)


# Check if provided str is valid date format
def validate_date(date_b: str) -> bool:
    return checkers.is_date(date_b)


# Check if provided str is valid email format
def validate_email(email_u: str) -> bool:
    return checkers.is_email(email_u)


# Compare 2 hashed passwords to check if they are the same
def validate_password(hash_pass1: bytes, hash_pass2: bytes) -> bool:
    return bcrypt.checkpw(hash_pass1, hash_pass2)


# Insert new user into 'User' database table with given personal and authentication details
def create_new_user(firstname: str, surname: str, birth: str, email: str, password: bytes) -> None:
    with sqlite3.connect(DBFILE) as db:
        cur = db.cursor()
        cur.execute("INSERT INTO User VALUES (null, ?, ?, ?, ?, null, ?, null)", (firstname, surname,
                                                                                  birth, email, password))


# Set up initial GUI components and allow user to login or register
def start() -> None:
    window = tk.Tk()
    window.geometry("700x400")

    # Create frames and store them in a dictionary for easy access
    frames = {
        "main": ttk.Frame(window),
        "create_user": ttk.Frame(window),
        "login": ttk.Frame(window),
        "portal": ttk.Frame(window),
    }

    # Setup each frame
    main_frame(frames["main"], frames)
    create_user(frames["create_user"], frames)
    login(frames["login"], frames)

    # Place all frames in the same location
    for frame in frames.values():
        frame.grid(row=0, column=0, sticky='nsew')
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

    # Show the main frame initially
    frames["main"].tkraise()
    window.mainloop()


# Configure main frame of application, providing options for user account creation or login
def main_frame(frame, frames):
    ttk.Label(frame, text="Create account or login", font=custom_font1, padding=(0, 20)).pack()
    createb = ttk.Button(frame, text="Create", style="alt.TButton", command=lambda: frames["create_user"].tkraise())
    createb.pack(pady=5)
    loginb = ttk.Button(frame, text="Login", style="alt.TButton", command=lambda: frames["login"].tkraise())
    loginb.pack(pady=5)


# Sets up GUI for creating new user account, including entry fields for personal and login information
def create_user(frame, frames) -> None:
    ttk.Label(frame, text="Create a New User", font=custom_font1).pack(pady=(10, 10))

    ttk.Label(frame, text="First name").pack()
    first_name = ttk.Entry(frame)
    first_name.pack(pady=(0, 5))

    ttk.Label(frame, text="Surname").pack()
    surname = ttk.Entry(frame)
    surname.pack(pady=(0, 5))

    ttk.Label(frame, text="Birthdate (YYYY-MM-DD)").pack()
    birthdate = ttk.Entry(frame)
    birthdate.pack(pady=(0, 5))

    ttk.Label(frame, text="Email").pack()
    email = ttk.Entry(frame)
    email.pack(pady=(0, 5))

    ttk.Label(frame, text="Password").pack()
    password1 = ttk.Entry(frame, show="*")
    password2 = ttk.Entry(frame, show="*")
    password1.pack(pady=(0, 5))
    password2.pack(pady=(0, 5))

    # Button to submit entered information, with validation checks
    ttk.Button(frame, text="Create user", command=lambda: validate_create(first_name.get().strip(),
                                                                          surname.get().strip(),
                                                                          birthdate.get().strip(), email.get().strip(),
                                                                          password1.get().strip(),
                                                                          password2.get().strip())).pack()
    # Button to return to main menu
    ttk.Button(frame, text="Back", command=lambda: frames["main"].tkraise()).pack(pady=5)

    # Message label for user feedback on actions
    user_message = ttk.Label(frame, text="")
    user_message.pack()

    # Validate data entered by user when creating new account
    def validate_create(f_name: str, s_name: str, date_b: str, email_u: str, pass1: str, pass2: str) -> None:
        if (f_name.isalpha() and f_name != "" and s_name.isalpha() and s_name != "" and validate_date(date_b) and
                validate_email(email_u) and pass1 != "" and pass2 != ""):
            salt = bcrypt.gensalt()
            hash_pass: bytes = bcrypt.hashpw(pass2.encode("utf-8"), salt)
            if validate_password(pass1.encode("utf-8"), hash_pass):
                create_new_user(f_name, s_name, date_b, email_u, hash_pass)
                # Clear fields after successful account creation
                first_name.delete(0, "end")
                surname.delete(0, "end")
                birthdate.delete(0, "end")
                email.delete(0, "end")
                password1.delete(0, "end")
                password2.delete(0, "end")
                # Switch to login frame
                frames["login"].tkraise()
            else:
                user_message.config(text="Wrong password")
        elif not f_name.isalpha() or f_name == "" or not s_name.isalpha() or s_name == "":
            user_message.config(text="Missing name")
        elif not validate_date(date_b):
            user_message.config(text="Incorrect date/format")
        elif not validate_email(email_u):
            user_message.config(text="Invalid email")
        elif pass1 == "" or pass2 == "":
            user_message.config(text="Missing password")
        else:
            user_message.config(text="Please enter required information")


# Handle user login with email and password, including validation and session handling
def login(frame, frames) -> None:
    ttk.Label(frame, text="User Login", font=custom_font1).pack(pady=(10, 10))

    ttk.Label(frame, text="Email").pack()
    email = ttk.Entry(frame)
    email.pack(pady=(0, 5))

    ttk.Label(frame, text="Password").pack()
    password = ttk.Entry(frame, show="*")
    password.pack(pady=(0, 5))

    # Button to submit login information, with validation checks
    ttk.Button(frame, text="Login", command=lambda: validate_login(email.get().strip(), password.get().strip())).pack()
    # Button to return to the main menu
    ttk.Button(frame, text="Back", command=lambda: frames["main"].tkraise()).pack(pady=5)

    # Message label for user feedback on login actions
    user_message = ttk.Label(frame, text="")
    user_message.pack()

    # Validate provided email and password against database records
    def validate_login(email_u: str, passw: str) -> None:
        if validate_email(email_u) and passw != "":
            if check_login(email_u, passw.encode("utf-8")):
                # Clear entry fields on successful login
                email.delete(0, "end")
                password.delete(0, "end")
                # Setup portal frame
                user_portal(frames["portal"], frames)
                # Switch to portal frame
                frames["portal"].tkraise()
            else:
                user_message.config(text="Invalid email and/or password")
        elif not validate_email(email_u):
            user_message.config(text="Invalid email and/or password")
        else:
            user_message.config(text="Please enter required information")


def user_portal(frame, frames) -> None:
    sidebar = tk.Frame(frames["portal"], bg="#C9C9C9")
    sidebar.pack(ipadx=20, fill=tk.Y, side=tk.LEFT)

    content_frame = tk.Frame(frames["portal"])
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    account = tk.Button(sidebar, text="Account", bg="#C9C9C9", font=custom_font1,
                        command=lambda: update_content("account"))
    account.pack(pady=(15, 0))

    courses = tk.Button(sidebar, text="Courses", bg="#C9C9C9", font=custom_font1,
                        command=lambda: update_content("courses"))
    courses.pack(pady=(15, 0))

    grades = tk.Button(sidebar, text="Grades", bg="#C9C9C9", font=custom_font1,
                       command=lambda: update_content("grades"))
    grades.pack(pady=(15, 0))

    sign_out = tk.Button(sidebar, text="Sign Out", bg="#C9C9C9", font=custom_font1)
    sign_out.pack(pady=15, side=tk.BOTTOM)

    def update_content(context) -> None:
        for widget in content_frame.winfo_children():
            widget.destroy()

        if context == "account":
            frame0 = tk.Frame(content_frame, bg="red")
            frame0.pack(pady=(15, 15), side=tk.TOP, fill=tk.X, expand=True, anchor="nw")
            frame1 = tk.Frame(frame0)
            frame1.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")
            frame2 = tk.Frame(frame0)
            frame2.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")
            frame3 = tk.Frame(content_frame, bg="red")
            frame3.pack(side=tk.TOP, fill=tk.X, expand=True, anchor="nw")

            tk.Label(frame1, text=f"ID: {user.id}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")
            tk.Label(frame1, text=f"Name: {user.name} {user.surname}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")
            tk.Label(frame1, text=f"Birthdate: {user.birthdate}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")
            tk.Label(frame2, text=f"Email: {user.email}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")
            tk.Label(frame2, text=f"University Email: {user.uniEmail}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")
            tk.Label(frame2, text=f"Degree:", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")
            tk.Label(frame3, text="Settings:", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")

        elif context == "courses":
            tk.Label(content_frame, text="Courses enrolled:").pack(pady=(15, 0))
            tk.Label(content_frame, text="Calculus, Physics, Literature").pack(pady=(15, 0))

        elif context == "grades":
            tk.Label(content_frame, text="Recent Grades:").pack(pady=(15, 0))
            tk.Label(content_frame, text="Calculus: A, Physics: B, Literature: A").pack(pady=(15, 0))

    update_content("account")


if __name__ == "__main__":
    main()
