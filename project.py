import os.path
import sqlite3
import tkinter as tk
from tkinter import ttk
import bcrypt

DBFILE: str = "roll_call.db"

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
                "Name TEXT NOT NULL, Birth TEXT NOT NULL," +
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

        # Check and return true if the password is correct
        return bcrypt.checkpw(password_encode, stored_hash_password)


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

    # Show the main frame initially
    frames["main"].tkraise()
    window.mainloop()


def main_frame(frame, frames):
    ttk.Label(frame, text="Create account or login", font=25, padding=(0, 20)).pack()
    createb = ttk.Button(frame, text="Create", style="alt.TButton", command=lambda: frames["create_user"].tkraise())
    createb.pack(pady=5)
    loginb = ttk.Button(frame, text="Login", style="alt.TButton", command=lambda: frames["login"].tkraise())
    loginb.pack(pady=5)


def create_user(frame, frames) -> None:
    ttk.Label(frame, text="Create a New User", font=25).pack(pady=20)
    ttk.Button(frame, text="Back to Main", command=lambda: frames["main"].tkraise()).pack()


def login(frame, frames) -> None:
    ttk.Label(frame, text="Login User", font=25).pack(pady=20)
    ttk.Button(frame, text="Back to Main", command=lambda: frames["main"].tkraise()).pack()


if __name__ == "__main__":
    main()
