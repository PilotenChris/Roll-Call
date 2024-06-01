# Roll-Call

## Video
Link will be provided soon.

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

Due to time constraints, we currently focused on developing features primarily for students.

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
