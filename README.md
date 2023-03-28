# Knowledge Management System (KMS) for Students

This is a Django-based web application designed to help students organize their notes, store important terms, and set revision goals. It is a knowledge management system aimed at improving the learning experience of students by streamlining the management of academic study materials through an easy to use interface.

Check out the Django application here: [https://django-pkms-7bpbf.ondigitalocean.app/](https://www.pkms.live/)

## Features

- **Multi-user support**: Each user can create and customize their own profile, and all notes and associated data are unique to each user, ensuring that each user's data is kept private and secure.
- **Robust authentication system**: Users can securely create and access their accounts, reset their passwords, and recover their accounts in case of any mishaps.
- **Customizability**: Users can personalize their profiles with a variety of settings, such as changing their profile picture or choosing a preferred color scheme.
- **Dashboard**: Users can view their courses, the latest note entries and both active and overdue revision objectives on a centralized dashboard.
- **Note taking and organization**: Users can take and store notes hierarchically, starting with the course, followed by the topic, then subtopic, and finally, individual entries. This hierarchical structure allows for easy navigation and quick access to notes.
- **Glossary**: Users can store important terms and definitions for different courses, making it easier to study and review key concepts.
- **Revision planning**: Users can set revision goals and deadlines and track their progress, helping them stay on top of their studies and achieve their academic goals.
- **Note sharing**: Users can share their notes with others via email, making it easy to share notes with friends and family.
- **Responsive UI**: The application is designed to work on different devices and screen sizes, ensuring a consistent and user-friendly experience across all platforms.


## Requirements

To run this application, you need:

- Python 3.10.8 or later
- PostgreSQL database (version 15.0 or later)
- Django 4.0 or later
- A modern web browser

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/nafdev01/django_pkms.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Create the database and apply the migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
4. Start the development server:
```bash
python manage.py runserver
```

5. Open your web browser and go to http://localhost:8000/ to access the application.

#### _Note_
_It helps to create aliases for common shell commands to ease update and troubleshooting processes and reduce repetition of commands e.g_
```bash
alias serve="python manage.py runserver"
alias migrate="python manage.py makemigrations && python manage.py migrate"
alias pkms="sudo service postgresql start && cd ~/Code/django_pkms/ && source ~/Code/django_pkms/.venv/bin/activate && serve"
alias dshell="python manage.py shell"
```

## Usage

1. Register a new account or login to an existing one.
2. Customize your profile (e.g., upload a profile picture, add your full name and email, and update course details).
3. Add new notes and organize them by course, topic, and subtopic.
4. Store important terms and definitions in the glossary section.
5. Set revision objectives and deadlines for each of them.
6. Share your notes with others via email.
7. Log out when you are done.

## Contributions

Contributions to this project are welcome! If you find a bug, want to request a new feature, or have an idea for improvement, please create an issue on this project's GitHub page. If you want to contribute code, please fork the repository and submit a pull request.

## License
_Pending_
<!-- 
This application is licensed under the MIT License. See the LICENSE file for more details. -->
