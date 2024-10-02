Flask Notes Application

This is a simple note-taking web application, similar to Google Keep, built using Flask. The application provides a secure user authentication system, allowing users to register, log in, and manage their notes.

User Authentication:

  Login and Registration System: Users can register with their email and password to create an account. Once registered, they can log in to securely access their notes.
  Password Reset via Email: If a user forgets their password, the application allows them to request a password reset. An email is sent with a link to reset the password securely.
  
Note Management:

  Users can create, view, edit, and delete notes after logging in.
  Notes are stored securely and associated with the logged-in user's account.
  Email Notifications:

Reset Password Feature: 

  The application uses an email service to send password reset links, ensuring users can regain access to their accounts if they forget their login credentials.

Technologies Used:

  Flask Framework: Handles routing, form validation, and session management.
  PostgreSQL: For lightweight storage of user data and notes.
  Flask-WTF: For form validation, including registration and login forms.
  Flask-Mail: Used for sending password reset emails.
  HTML/CSS: Front-end user interface to interact with the application.
