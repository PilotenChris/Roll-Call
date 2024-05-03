import os.path
import re
import sqlite3
import tkinter as tk
from tkinter import ttk
import bcrypt
from validator_collection import checkers

DBFILE: str = "roll_call.db"

custom_label_font: tuple = ("Helvetica", 15)


def main() -> None:
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
    cur.execute("CREATE TABLE User(Id INTEGER NOT NULL UNIQUE," +
                "FirstName TEXT NOT NULL, Surname TEXT NOT NULL, Birth TEXT NOT NULL," +
                "Email TEXT NOT NULL UNIQUE, UniEmail TEXT," +
                "Password TEXT NOT NULL, Account INTEGER NOT NULL," +
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
                "PRIMARY KEY(UserId, DegreeId))")

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

    cur.execute("CREATE TRIGGER CreateUniEmail AFTER INSERT ON User " + "\n" +
                "BEGIN " + "\n" +
                "UPDATE User SET UniEmail = NEW.Id || '@idkUniversity.com' WHERE Id = NEW.Id;" + "\n" +
                "END;")

    cur.execute("CREATE TRIGGER AssignUser AFTER INSERT ON User " + "\n" +
                "BEGIN " + "\n" +
                "UPDATE User SET Account = 1 WHERE Id = NEW.Id;" + "\n" +
                "END;")

    # Insert the default data into table Account
    cur.execute("INSERT INTO Account (AccountType) VALUES ('Student')," +
                "('Teacher'), ('Admin')")

    con.commit()
    con.close()


def check_login(email: str, password: str) -> bool:
    # Connect to the database and go through User to find password by email
    with sqlite3.connect(DBFILE) as db:
        cur = db.cursor()
        cur.execute("SELECT Password FROM User WHERE Email = ?", (email,))
        # If you found the Email, put password in the result, else put None in the result
        result = cur.fetchone()

        # If the result is None, then the Email was wrong, and return False
        if result is None:
            return False

        stored_hash_password = result[0].encode("utf-8")
        password_encode = password.encode("utf-8")

        # Check and return true if the password is correct, else return false
        return bcrypt.checkpw(password_encode, stored_hash_password)


def validate_date(date_b: str) -> bool:
    return checkers.is_date(date_b)


def validate_email(email_u: str) -> bool:
    return checkers.is_email(email_u)


def create_new_user(firstname: str, surname: str, birth: str, email: str, password: str) -> None:
    with sqlite3.connect(DBFILE) as db:
        cur = db.cursor()
        cur.execute("INSERT INTO User VALUES (?, ?, ?, ?, null, ?, null)", (firstname, surname, birth,
                                                                            email, password))


def start() -> None:
    window = tk.Tk()
    window.geometry("700x400")

    # Create frames and store them in a dictionary for easy access
    frames = {
        "main": ttk.Frame(window),
        "create_user": ttk.Frame(window),
        "login": ttk.Frame(window)
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


def main_frame(frame, frames):
    ttk.Label(frame, text="Create account or login", font=custom_label_font, padding=(0, 20)).pack()
    createb = ttk.Button(frame, text="Create", style="alt.TButton", command=lambda: frames["create_user"].tkraise())
    createb.pack(pady=5)
    loginb = ttk.Button(frame, text="Login", style="alt.TButton", command=lambda: frames["login"].tkraise())
    loginb.pack(pady=5)


def create_user(frame, frames) -> None:
    ttk.Label(frame, text="Create a New User", font=custom_label_font).pack(pady=(10, 10))
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
    password1 = ttk.Entry(frame)
    password2 = ttk.Entry(frame)
    password1.pack(pady=(0, 5))
    password2.pack(pady=(0, 5))
    ttk.Button(frame, text="Create user", command=lambda: validate_create(first_name.get(), surname.get(),
                                                                          birthdate.get(), email.get(), password1.get(),
                                                                          password2.get())).pack()
    user_message = ttk.Label(frame, text="")
    user_message.pack()

    def validate_create(f_name: str, s_name: str, date_b: str, email_u: str, pass1: str, pass2: str) -> None:
        if (f_name.isalpha() and f_name != "" and s_name.isalpha() and s_name != "" and validate_date(date_b) and
                validate_email(email_u) and pass1 != "" and pass2 != ""):
            hash_pass1: str = ""
            hash_pass2: str = ""
            if validate_password(hash_pass1, hash_pass2):
                first_name.delete(0, "end")
                surname.delete(0, "end")
                birthdate.delete(0, "end")
                email.delete(0, "end")
                password1.delete(0, "end")
                password2.delete(0, "end")
                frames["login"].tkraise()
            else:
                user_message.config(text="Wrong password")
        elif not f_name.isalpha() or f_name == "" or not s_name.isalpha() or s_name == "":
            user_message.config(text="Missing name")
        elif not validate_date(date_b):
            user_message.config(text="Incorrect date/format")
        elif not validate_email(email_u):
            user_message.config(text="Invalid email")
        else:
            user_message.config(text="Please enter required information")


def login(frame, frames) -> None:
    ttk.Label(frame, text="Login User", font=custom_label_font).pack(pady=20)
    ttk.Button(frame, text="Back to Main", command=lambda: frames["main"].tkraise()).pack()


if __name__ == "__main__":
    main()
