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
import copy

# Constant for database file path
DBFILE: str = "roll_call.db"

# Font style for labels in application
custom_font1: tuple = ("Helvetica", 15)
custom_font2: tuple = ("Helvetica", 13)

# Current logged-in user, instance of type Person (Student, Teacher, Admin)
user: Union[Person, Student, Teacher, Admin]

# Defining list of filter options for courses
FILTER_OPTIONS: list[str] = ["", "All courses", "Courses for degree", "Courses I am taking"]

# Initialising lists to hold filtered courses, all courses and courses for a degree
courses_filter_list: list[Course] = []
all_courses_list: list[Course] = []
all_courses_for_degree_list: list[Course] = []

# Variable to keep track of selected filter option
select_filter_value: int = 0

# Setting up main window for Tkinter GUI application
window = tk.Tk()
window.geometry("1000x500")


def main() -> None:
    # Check if database file exists, if not create new database
    if not os.path.isfile(DBFILE):
        create_database()

    # Login or Create account
    start()


# Function to create the database with the required Tables and Fields
# And inserts the required starting data
def create_database() -> None:
    with sqlite3.connect(DBFILE) as db:
        cur = db.cursor()

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

        #
        cur.execute("CREATE TABLE DegreeBase(BaseId INTEGER NOT NULL," +
                    "BaseName TEXT NOT NULL UNIQUE," +
                    "PRIMARY KEY(BaseId AUTOINCREMENT))")

        #
        cur.execute("CREATE TABLE DegreeBaseName(DegreeBNId INTEGER NOT NULL," +
                    "DegreeBName TEXT NOT NULL UNIQUE," +
                    "PRIMARY KEY(DegreeBNId AUTOINCREMENT))")

        #
        cur.execute("CREATE TABLE DegreeType(TypeId INTEGER NOT NULL," +
                    "TypeName TEXT NOT NULL UNIQUE," +
                    "PRIMARY KEY(TypeId AUTOINCREMENT))")

        # Create the table Degree in the Database with required fields
        cur.execute("CREATE TABLE Degrees(BaseId INTEGER NOT NULL," +
                    "DegreeBNId INTEGER NOT NULL," +
                    "TypeId INTEGER NOT NULL," +
                    "PRIMARY KEY(BaseId, DegreeBNId, TypeId)," +
                    "FOREIGN KEY(BaseId) REFERENCES DegreeBase(BaseId)" +
                    "FOREIGN KEY(TypeId) REFERENCES DegreeType(TypeId)" +
                    "FOREIGN KEY(DegreeBNId) REFERENCES DegreeBaseName(DegreeBNId))")

        #
        cur.execute("CREATE TABLE Degree(UserId INTEGER NOT NULL," +
                    "BaseId INTEGER NOT NULL," +
                    "DegreeBNId INTEGER NOT NULL," +
                    "TypeId INTEGER NOT NULL," +
                    "PRIMARY KEY(UserId, BaseId, DegreeBNId, TypeId)," +
                    "FOREIGN KEY(UserId) REFERENCES User(Id)," +
                    "FOREIGN KEY(BaseId, DegreeBNId, TypeId) REFERENCES Degrees(BaseId, DegreeBNId, TypeId))")

        # Create the table Course in the Database with required fields
        cur.execute("CREATE TABLE Course(CourseId INTEGER NOT NULL," +
                    "CourseName TEXT NOT NULL," +
                    "PassingGrade INTEGER NOT NULL," +
                    "Active INTEGER NOT NULL," +
                    "PRIMARY KEY(CourseId AUTOINCREMENT))")

        # Create the table Grade in the Database with required fields
        cur.execute("CREATE TABLE Grade(UserId INTEGER NOT NULL," +
                    "CourseId INTEGER NOT NULL," +
                    "Grade INTEGER NOT NULL," +
                    "FOREIGN KEY(CourseId) REFERENCES Course(CourseId)," +
                    "FOREIGN KEY(UserId) REFERENCES User(Id)," +
                    "PRIMARY KEY(UserId, CourseId))")

        # Create the table Classes in the Database with required fields
        cur.execute("CREATE TABLE CourseEnrollments(UserId INTEGER NOT NULL," +
                    "CourseId INTEGER NOT NULL," +
                    "StartDate TEXT NOT NULL," +
                    "Assigned INTEGER NOT NULL," +
                    "PRIMARY KEY(UserId, CourseId, StartDate)," +
                    "FOREIGN KEY(UserId) REFERENCES User(Id)," +
                    "FOREIGN KEY(CourseId) REFERENCES Course(CourseId))")

        #
        cur.execute("CREATE TABLE Connection(CourseId INTEGER NOT NULL," +
                    "BaseId INTEGER NOT NULL," +
                    "DegreeBNId INTEGER NOT NULL," +
                    "TypeId INTEGER NOT NULL," +
                    "PRIMARY KEY(CourseId, BaseId, DegreeBNId, TypeId)," +
                    "FOREIGN KEY(CourseId) REFERENCES Course(CourseId)," +
                    "FOREIGN KEY(BaseId, DegreeBNId, TypeId) REFERENCES Degrees(BaseId, DegreeBNId, TypeId))")

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

        # Insert the default data into table DegreeBase
        cur.execute("INSERT INTO DegreeBase (BaseName) VALUES ('Bachelors')," +
                    "('Masters'), ('Doctor of Philosophy')")

        # Insert the default data into table DegreeBaseName
        cur.execute("INSERT INTO DegreeBaseName (DegreeBName) VALUES ('Science')")

        # Insert the default data into table DegreeType
        cur.execute("INSERT INTO DegreeType (TypeName) VALUES ('Zoology'), " +
                    "('Wildlife Management'), ('Entomology'), ('IT and IS')")

        # Insert the degrees build on DegreeBase, DegreeBaseName
        # and DegreeType into Degrees
        cur.execute("INSERT INTO Degrees VALUES (1,1,1), (1,1,2), (1,1,3), " +
                    "(2,1,1), (2,1,2), (2,1,3), (3,1,1), (3,1,2), (3,1,3), " +
                    "(1,1,4)")

        # Dummy data
        cur.execute("INSERT INTO Degree VALUES (1,3,1,1)")

        cur.execute("INSERT INTO Course VALUES (null, 'Zoology', 50, 1), " +
                    "(null, 'Botany', 50, 1), (null, 'Genetics', 50, 1), " +
                    "(null, 'Biochemistry', 50, 1), (null, 'Entomology', 50, 1), " +
                    "(null, 'Geography', 50, 1), (null, 'Mathematics', 50, 1), " +
                    "(null, 'Physics ', 50, 1), (null, 'Chemistry', 50, 1), " +
                    "(null, 'Biostatistics', 50, 1), (null, 'Thesis Zoology', 50, 1), " +
                    "(null, 'Dissertation Zoology', 50, 1), (null, 'Geographic Information System', 50, 1), " +
                    "(null, 'Object-Oriented Programming', 50, 1), (null, 'Application Development', 50, 1)")

        cur.execute("INSERT INTO Connection VALUES (1, 1,1,1)," +
                    "(2, 1,1,1), (3, 1,1,1), (4, 1,1,1), (5, 1,1,1)," +
                    "(6, 1,1,1), (7, 1,1,1), (8, 1,1,1), (9, 1,1,1)," +
                    "(10, 1,1,1), (11, 3,1,1), (12, 2,1,1), " +
                    "(13, 1,1,4), (14, 1,1,4), (15, 1,1,4)")

        cur.execute("INSERT INTO CourseEnrollments VALUES (1, 11, 2024-05-23, 1)," +
                    "(1, 1, 2020-05-23, 1), (1, 2, 2020-05-23, 1), " +
                    "(1, 3, 2020-05-23, 1), (1, 4, 2020-05-23, 1), " +
                    "(1, 5, 2020-05-23, 1), (1, 6, 2020-05-23, 1), " +
                    "(1, 7, 2020-05-23, 1), (1, 8, 2020-05-23, 1), " +
                    "(1, 9, 2020-05-23, 1), (1, 10, 2020-05-23, 1), " +
                    "(1, 12, 2023-05-23, 1)")

        cur.execute("INSERT INTO Grade VALUES (1,1,63), (1,2,71), " +
                    "(1,3,65), (1,4,74), (1,5,77), (1,6,79), " +
                    "(1,7,60), (1,8,78), (1,9,72), (1,10,68), " +
                    "(1,12,76)")

        # Commit changes
        db.commit()


def insert_course(course_name: str, passing_grade: int) -> None:
    with sqlite3.connect(DBFILE) as conn:
        cur = conn.cursor()

        # Insert a course into the database
        cur.execute("INSERT INTO Course (CourseName, PassingGrade) VALUES (?, ?)",
                    (course_name, passing_grade))
        conn.commit()


def get_all_courses() -> None:
    with sqlite3.connect(DBFILE) as conn:
        cur = conn.cursor()

        # Retrieve all the courses from the database
        cur.execute("SELECT CourseId, CourseName, PassingGrade, Active FROM Course")
        all_courses_from_database = cur.fetchall()

        global all_courses_list

        if all_courses_from_database:
            all_courses_list.clear()
            for course_tuple in all_courses_from_database:
                course_id = course_tuple[0]
                course_name = course_tuple[1]
                course_pass_grade = course_tuple[2]
                course_active = course_tuple[3]
                all_courses_list.append(Course(course_id, course_name, course_pass_grade, course_active))


def get_all_courses_for_degree(user_id: int) -> None:
    with sqlite3.connect(DBFILE) as conn:
        cur = conn.cursor()

        #
        cur.execute("SELECT c.CourseId, c.CourseName, c.PassingGrade, c.Active FROM User AS u, Degree AS d, " +
                    "Degrees AS deg, Connection AS con, Course AS c WHERE u.Id = d.UserId " +
                    "AND d.DegreeBNId = deg.DegreeBNId AND deg.BaseId = con.BaseId " +
                    "AND deg.DegreeBNId = con.DegreeBNId AND deg.TypeId = con.TypeId " +
                    "AND con.CourseId = c.CourseId AND u.Id = ?", (user_id,))
        all_courses_for_degree_from_database = cur.fetchall()

        global all_courses_for_degree_list

        if all_courses_for_degree_from_database:
            all_courses_for_degree_list.clear()
            for course_tuple in all_courses_for_degree_from_database:
                course_id = course_tuple[0]
                course_name = course_tuple[1]
                course_pass_grade = course_tuple[2]
                course_active = course_tuple[3]
                all_courses_for_degree_list.append(Course(course_id, course_name, course_pass_grade, course_active))


# Checks the login credentials, retrieves user details from the database and initializes the global user object based
# on the role (Student, Teacher, Admin)
def check_login(email: str, password: bytes) -> bool:
    # Connect to the database and go through User to find password by email
    with sqlite3.connect(DBFILE) as conn:
        cur = conn.cursor()
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

        # Retrieve degree of user based on the user ID
        cur.execute("SELECT BaseId, DegreeBNId, TypeId FROM Degree WHERE UserId = ?", (stored_id,))
        degree_list = cur.fetchone()

        # Empty string of the full degree of the user
        full_degree: str = ""

        # Retrieve the name for DegreeBase, DegreeBaseName and DegreeType
        # to get the full name of the degree of the user
        if degree_list:
            cur.execute(
                "SELECT BaseName, DegreeBName, TypeName FROM DegreeBase, DegreeBaseName, DegreeType " +
                "WHERE BaseId = ? AND DegreeBNId = ? AND TypeId = ?",
                (degree_list[0], degree_list[1], degree_list[2]))
            degree_for_user = cur.fetchone()
            full_degree += f"{degree_for_user[0]} of {degree_for_user[1]} {degree_for_user[2]}"

        # Retrieve the courses ids the user is enrolled into based on the user ID
        cur.execute("SELECT CourseId FROM CourseEnrollments WHERE Assigned = 1 AND UserId = ?", (stored_id,))
        enrolld_courses = cur.fetchall()

        # Empty list of courses
        list_of_courses: list[Course] = []

        # Retrieve the course details for each course the user has based on the course ID
        if enrolld_courses:
            for course_tuple in enrolld_courses:
                course_id = course_tuple[0]
                cur.execute("SELECT CourseName, PassingGrade, Active FROM Course WHERE CourseId = ?", (course_id,))
                enrolld_course = cur.fetchone()
                list_of_courses.append(Course(course_id, enrolld_course[0], enrolld_course[1], enrolld_course[2]))

        # Retrieve the course and grade for each graded course for the user
        cur.execute("SELECT c.CourseId, c.CourseName, c.PassingGrade, c.Active, g.Grade FROM " +
                    "Course AS c, Grade AS g WHERE c.CourseId = g.CourseId AND g.UserId = ?", (stored_id,))
        graded_courses = cur.fetchall()

        list_of_graded_courses: list[Grade] = []

        if graded_courses:
            for course_tuple in graded_courses:
                list_of_graded_courses.append(Grade(Course(course_tuple[0], course_tuple[1], course_tuple[2],
                                                           course_tuple[3]), course_tuple[4]))

        # Check the user's account type and initialize the corresponding object
        if person_result[5] == 1:
            user = Student(stored_id, person_result[0], person_result[1], person_result[2], person_result[3],
                           person_result[4], full_degree, list_of_courses, list_of_graded_courses)
        elif person_result[5] == 2:
            user = Teacher(stored_id, person_result[0], person_result[1], person_result[2], person_result[3],
                           person_result[4], [])
        elif person_result[5] == 3:
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
    with sqlite3.connect(DBFILE) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO User VALUES (null, ?, ?, ?, ?, null, ?, null)", (firstname, surname,
                                                                                  birth, email, password))
        conn.commit()


# Set up initial GUI components and allow user to login or register
def start() -> None:
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

    ttk.Label(frame, text="Birthdate").pack()
    birthdate = ttk.Entry(frame, foreground="gray")
    birthdate.insert(0, "YYYY-MM-DD")
    birthdate.pack(pady=(0, 5))

    def on_entry_click(event) -> None:
        if birthdate.get() == "YYYY-MM-DD":
            birthdate.delete(0, tk.END)
            birthdate.configure(foreground="black")

    def on_focus_out(event) -> None:
        if birthdate.get() == "":
            birthdate.insert(0, "YYYY-MM-DD")
            birthdate.configure(foreground="gray")

    birthdate.bind("<FocusIn>", on_entry_click)
    birthdate.bind("<FocusOut>", on_focus_out)

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

                # Call on getting all the courses
                get_all_courses()
                get_all_courses_for_degree(user.id)
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


# Creating scrollbar and sidebar buttons for different sections of application
def user_portal(frame, frames) -> None:
    # Creating sidebar frame to hold navigation buttons
    sidebar = tk.Frame(frames["portal"], bg="#C9C9C9")
    sidebar.pack(ipadx=20, fill=tk.Y, side=tk.LEFT)

    # Creating canvas widget within "portal" frame
    canvas = tk.Canvas(frames["portal"])
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Adding vertical scrollbar to "portal" frame and linking it to canvas
    scrollbar = tk.Scrollbar(frames["portal"], orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Creating wrapper frame inside canvas
    wrapper_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=wrapper_frame, anchor="n")

    # Creating content frame inside wrapper frame to hold main content
    content_frame = tk.Frame(wrapper_frame)
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configuring canvas to update its scroll region whenever wrapper frame is resized
    wrapper_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.configure(yscrollcommand=scrollbar.set)

    # "Account" button to update content frame with account-related information
    account = tk.Button(sidebar, text="Account", bg="#C9C9C9", font=custom_font1,
                        command=lambda: update_content(content_frame, "account"))
    account.pack(pady=(15, 0))

    # "Courses" button to update content frame with course-related information
    courses = tk.Button(sidebar, text="Courses", bg="#C9C9C9", font=custom_font1,
                        command=lambda: update_content(content_frame, "courses"))
    courses.pack(pady=(15, 0))

    # "Grades" button to update content frame with grades-related information
    grades = tk.Button(sidebar, text="Grades", bg="#C9C9C9", font=custom_font1,
                       command=lambda: update_content(content_frame, "grades"))
    grades.pack(pady=(15, 0))

    # "Sign Out" button to quit application
    sign_out = tk.Button(sidebar, text="Sign Out", bg="#C9C9C9", font=custom_font1, command=lambda: window.quit())
    sign_out.pack(pady=15, side=tk.BOTTOM)

    # Initial call to update content frame with account-related information
    update_content(content_frame, "account")


def update_content(content_frame: tk.Frame, context: str) -> None:
    # Clearing all existing widgets from content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Update content frame based on given context
    if context == "account":
        # Load user account details into content frame
        user_account(content_frame)

    elif context == "courses":
        # Load user courses information into content frame
        user_courses(content_frame)

    elif context == "grades":
        # Load user grades information into content frame
        user_grades(content_frame)


# Function to display user account in content frame
def user_account(content_frame: tk.Frame) -> None:
    # Creating frame to hold user account details in content frame
    frame00 = tk.Frame(content_frame)
    frame00.pack(pady=(15, 15), side=tk.TOP, fill=tk.X, anchor="nw")

    # Displaying user account details in frame
    user_account_detail(frame00)

    # Creating frames for account setting
    frame10 = tk.Frame(content_frame)
    frame10.pack(side=tk.TOP, fill=tk.X, anchor="n")
    frame20 = tk.Frame(content_frame)
    frame20.pack(side=tk.TOP, fill=tk.X, anchor="n")

    # Displaying user account settings in frames
    user_account_setting(frame10, frame20, content_frame)


def user_account_detail(frame00: tk.Frame) -> None:
    # Creating frame for first column of user details
    frame01 = tk.Frame(frame00)
    frame01.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")

    # Displaying user ID, name and birthdate
    tk.Label(frame01, text=f"ID: {user.id}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")
    tk.Label(frame01, text=f"Name: {user.name} {user.surname}", font=custom_font2).pack(pady=(15, 0), padx=15,
                                                                                        anchor="nw")
    tk.Label(frame01, text=f"Birthdate: {user.birthdate}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")

    # Creating frame for second column of user details
    frame02 = tk.Frame(frame00)
    frame02.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")

    # Displaying user email, university email and degree
    tk.Label(frame02, text=f"Email: {user.email}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")
    tk.Label(frame02, text=f"University Email: {user.uniEmail}", font=custom_font2).pack(pady=(15, 0), padx=15,
                                                                                         anchor="nw")
    tk.Label(frame02, text=f"Degree: {user.degree}", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")


def user_account_setting(frame10: tk.Frame, frame20: tk.Frame, content_frame: tk.Frame) -> None:
    # Displaying settings label
    tk.Label(frame10, text="Settings:", font=custom_font2).pack(pady=(15, 0), padx=15, anchor="nw")

    # Creating frame for email settings
    frame21 = tk.Frame(frame20)
    frame21.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")
    tk.Label(frame21, text="Email:", font=custom_font2).pack(padx=15, anchor="nw")
    email = ttk.Entry(frame21)
    email.pack(pady=(15, 0), padx=15, anchor="nw")

    # Creating frame for password settings
    frame22 = tk.Frame(frame20)
    frame22.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")
    tk.Label(frame22, text="Password:", font=custom_font2).pack(padx=15, anchor="nw")
    password1 = ttk.Entry(frame22)
    password1.pack(pady=(15, 0), padx=15, anchor="nw")
    password2 = ttk.Entry(frame22)
    password2.pack(pady=(15, 0), padx=15, anchor="nw")

    # Label to display messages related to settings
    setting_message = tk.Label(content_frame, text="")
    setting_message.pack()

    # Save button to trigger saving of user settings
    tk.Button(content_frame, text="Save", bg="#C9C9C9", font=custom_font2,
              command=lambda: setting_message.config(text=save_user_settings(email.get(), password1.get(),
                                                                             password2.get()))).pack()


# Function to display user courses in content frame
def user_courses(content_frame: tk.Frame) -> None:
    # Creating and packing frames for organising layout
    frame00 = tk.Frame(content_frame)
    frame00.pack(pady=(15, 15), side=tk.TOP, fill=tk.X, anchor="nw")
    frame01 = tk.Frame(frame00)
    frame01.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")
    frame02 = tk.Frame(frame00)
    frame02.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")
    frame03 = tk.Frame(frame00)
    frame03.pack(pady=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")

    # Adding label and search entry field for search courses section
    tk.Label(frame01, text="Search Courses", font=custom_font2).pack(padx=15, anchor="nw")
    search = ttk.Entry(frame02, width=40)
    search.pack(padx=15, anchor="nw")

    # Adding filter button and a combobox for filter options
    filter_b = tk.Button(frame03, text="Filter", font=custom_font2, command=lambda: handle_filter())
    filter_b.pack(side=tk.LEFT, padx=(0, 5))

    filter_combobox = ttk.Combobox(frame03, font=custom_font2, values=FILTER_OPTIONS, state='readonly')
    filter_combobox.current(select_filter_value)
    filter_combobox.pack(padx=15, anchor="nw", side=tk.LEFT)
    filter_combobox.bind("<<ComboboxSelected>>", filter_courses)

    # Function to handle filtering of courses based on search criteria and selected filter
    def handle_filter() -> None:
        global select_filter_value
        global courses_filter_list
        search_list: list[Course] = []
        select_filter_value = filter_combobox.current()
        search_cat: str = search.get()
        if search_cat != "":
            select_filter_value = 0
            courses_filter_list.clear()
            for item in all_courses_list:
                if re.search(fr"^{search_cat}[a-zA-Z ]+$", item.name, re.IGNORECASE):
                    search_list.append(Course(item.id, item.name, item.passing_grade, item.active_status))
            courses_filter_list = search_list
        update_content(content_frame, "courses")

    # Displaying filtered courses in content frame
    for course in courses_filter_list:
        frame10 = tk.Frame(content_frame)
        frame10.pack(side=tk.TOP, fill=tk.X, anchor="n")
        frame11 = tk.Frame(frame10, bg="#C9C9C9")
        frame11.pack(pady=(15, 15), padx=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")
        tk.Label(frame11, text=f"{course.name} - Active: {'Yes' if course.active_status == 1 else 'No'}",
                 font=custom_font2, bg="#C9C9C9").pack(padx=15, anchor="nw")


def filter_courses(event) -> None:
    # Global list to hold filtered courses
    global courses_filter_list
    # Get selected filter option from event widget
    option = event.widget.get()
    # Match selected filter option and update courses_filter_list accordingly
    match option:
        case "All courses":
            # If "All courses" is selected, clear and copy all courses to filter list
            courses_filter_list.clear()
            courses_filter_list = copy.deepcopy(all_courses_list)
        case "Courses for degree":
            # If "Courses for degree" is selected, clear and copy degree courses to filter list
            courses_filter_list.clear()
            courses_filter_list = copy.deepcopy(all_courses_for_degree_list)
        case "Courses I am taking":
            # If "Courses I am taking" is selected, clear and copy user's courses to filter list
            courses_filter_list.clear()
            courses_filter_list = copy.deepcopy(user.courses)
        case _:
            # For any other option, just clear filter list
            courses_filter_list.clear()


# Function to display user grades in content frame
def user_grades(content_frame: tk.Frame) -> None:
    # Creating and packing main frame for user grades
    frame00 = tk.Frame(content_frame)
    frame00.pack(pady=(15, 15), side=tk.TOP, fill=tk.X, anchor="nw")

    # Creating and packing subframe within main frame
    frame01 = tk.Frame(frame00)
    frame01.pack(pady=(15, 15), side=tk.TOP, fill=tk.X, expand=True, anchor="nw")

    # Adding label to display "Current Courses"
    tk.Label(frame01, text="Current Courses", font=custom_font2).pack(padx=15, anchor="n")

    # Loop through user's current courses to display each course and its grade
    for course in user.courses:
        # Creating and packing frame for each course
        frame02 = tk.Frame(frame00, bg="#C9C9C9")
        frame02.pack(pady=(15, 0), padx=(15, 15), side=tk.TOP, fill=tk.X, expand=True, anchor="nw")

        # Creating and packing subframes within course frame for course name and grade
        frame021 = tk.Frame(frame02, bg="#C9C9C9")
        frame021.pack(pady=(15, 15), padx=(15, 15), side=tk.LEFT, fill=tk.X, expand=True, anchor="nw")
        frame022 = tk.Frame(frame02, bg="#C9C9C9")
        frame022.pack(pady=(15, 15), padx=(15, 15), side=tk.RIGHT, fill=tk.X, expand=True, anchor="ne")

        # Adding labels to display course name and grade
        tk.Label(frame021, text=course.name, font=custom_font2, bg="#C9C9C9").pack(padx=15, anchor="nw")
        tk.Label(frame022, text=grade_context(course), font=custom_font2, bg="#C9C9C9").pack(padx=15, anchor="ne")


# Function to get grade context for a given course
def grade_context(course: Course) -> str:
    # Iterate through user's grades to find grade for specified course
    for grade in user.grades:
        if grade.course.name == course.name:
            return f"{grade.grades}/100"
    # Return default value if no grade is found for course
    return f"-/100"


# Function to save user settings (email and password)
def save_user_settings(email_u: str, pass1: str, pass2: str) -> str:
    # Validate email and password lengths and return appropriate messages
    if not validate_email(email_u) and (len(pass1) < 8 or len(pass2) < 8):
        return ""
    elif validate_email(email_u) and (len(pass1) > 7 and len(pass2) > 7) and (len(pass1) == len(pass2)):
        return "Updated email and password"
    elif validate_email(email_u) and (len(pass1) < 8 or len(pass2) < 8):
        return "Updated email"
    elif (not validate_email(email_u) or email_u == "") and (len(pass1) > 7 and len(pass2) > 7) and (
            len(pass1) == len(pass2)):
        return "Update password"
    else:
        return ""


if __name__ == "__main__":
    main()
