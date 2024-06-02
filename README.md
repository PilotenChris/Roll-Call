# Roll-Call

## Video
https://youtu.be/i4kcW-_j_AY

## Description of Our Product
Roll-Call is a university portal designed to facilitate easy access to account information, courses, and grades for students. Here's what students can do with Roll-Call:
- **Account Creation**: Students can create a new account by inputting their name, surname, birth date, email, and password.
- **Login**: Students can log in to their existing account using their email and password.
- **Account Management**: Upon logging in, students can view their ID, full name, birth date, email, university email, and the degree they are registered for. They can also change their email and password.
- **Course Access**: The "Courses" page allows students to search for courses offered by the university, filter courses by degree, or view courses they are currently enrolled in.
- **Grade Overview**: The "Grades" page displays grades for each course a student is enrolled in.
- **Sign Out**: Students can sign out of the portal, which closes their session.

## Original Plan
We aimed to develop a comprehensive university portal for Students, Teachers, and Admins to manage courses, grades, and user information. Key features included:
- **Student Features**: Ability to change minor account settings, select courses, view peers and teachers, and apply for new courses.
- **Teacher Features**: Account management similar to students, ability to view and manage courses they teach, set or change grades.
- **Admin Features**: Full control over user accounts, course approvals, and teacher assignments.

Due to time constraints, we have currently focused on developing features primarily for students.

## Future Development
We plan to expand the functionality to include:
- **Student Interface**: Enhanced access to course information, peer and teacher details, and course applications.
- **Teacher GUI**: Full feature set for course management and grading.
- **Admin GUI**: Comprehensive administration capabilities over courses, teachers, and student accounts.

## Installation and Setup
To install all required packages, run the following command:
```bash
pip install -r requirements.txt
```
After that you should be able to run 
```bash
python project.py
```
To  run the project.
This will create the required database where the first user you create will have default dummy data added to it. Any other user that get created will not come with dummy data.
The database is a simple SQLite database.

## System Design
**Person, Student, Teacher & Admin**
- **Person** is the superclass and Student, Teacher, and Admin inherit all the functionalities from Person. Person includes the individual’s ID, name, surname birthdate, email, and university email.
- **Student** includes degree, list of courses by the class Course and list of grades by the class Grade.
- **Teacher** includes a list of courses by the class Course.
- **Admin** includes nothing more.

This differentiation ensures that each user account type logs into the correct portal for their needs.

**Course**
- **Course** includes the ID, name, passing grade, and active status.

**Grade**
- **Grade** includes the course and grade for that course.

**Project Details**

In the project, we chose to use **tkinter** to create our GUI for the university portal, **bcrypt** to encrypt passwords and also be able to check if passwords are correct, **sqlite3** for our database, and **validator_collection** to be able to check for email and date. The project.py contains the GUI, create and insert of the database, and all the pages of the GUI. We use the Person, Student, Teacher, and Admin class as well as Course and Grade class to show all the relevant information for the different user types. Due to the extensive time required for GUI development, we ended up only creating GUI and functionality for the Student account type.

**Testing**

**test_project** tests our validate_date function, validate_email, and validate_password functions, to ensure they work correctly. If GUI development hadn’t taken so much time, we would have added more functions that would have been needed in the project.

**Database**

**roll_call.db:** Our database uses **SQLite** and is built up by 11 tables. 
- **Account** table has an AccountId and AccountType, this is meant to link the user to a Student, Teacher, or Admin account. 
- **User** table has an Id, Name, Birth, Email, UniEmail, Password and the link to AccountId. 
- **Degrees** table is to link the tables **DegreeBase** (like Bachelor, Master, etc.), **DegreeBaseName** (like of “Science”, etc.), **DegreeType** (like Zoology, Entomology, etc.), so that **Degrees** table becomes a list of degrees like this (“Bachelor” of “Science” “Zoology”). 
- **Degree** table is connecting the user table with the **Degrees** table, to show which degree the user is taking by all the ids from **Degrees** and **User** table. 
- **Course** table is for all the courses for the university, and has CourseId, CourseName, PassingGrade and Active (to show if the course is active or not). 
- **Connection** table connects the **Course** table and **Degrees** table with all the ids from both tables, to show which degrees can take the specific course. 
- **CourseEnrollments** table has UserId, CourseId, StartDate, Assigned and links the **User** up with all the **Courses** they are taking or want to take. Assigned is the field that decides if the user is taking the class or if they have requested to take the course. 
- **Grade** table has UserId, CourseId, and Grade, where it connects a grade for a student and for a specific course they are taking. We have 2 triggers, one to set the new account to be student when it gets created, and one to make a university email for them by their id number when the user gets created.

