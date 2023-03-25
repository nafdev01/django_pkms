# Knowledge Management System (KMS) for Students

This is a Django-based web application designed to help students organize their notes, store important terms, and set revision goals. It is a knowledge management system aimed at improving the learning experience of students.

## Features

- Multiple users support: each user can create their own profile and customize it.
- Note taking and organization: users can take and store notes for different subjects, topics, and categories.
- Tagging and labeling: users can assign tags and labels to their notes to make them easy to find and filter.
- Term repository: users can store important terms and definitions for different subjects and courses.
- Revision planning: users can set revision goals and deadlines for their notes and terms, and track their progress.
- Sharing notes: users can share their notes with others via email.
- Responsive UI: the application is designed to work on different devices and screen sizes.

## Requirements

To run this application, you need:

- Python 3.6 or later
- Django 3.0 or later
- A modern web browser

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/kms.git
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

####_Note_
_It helps to create aliases for common shell commands to ease update and troubleshooting processes and reduce repetition of commands e.g_
```bash
alias serve="python manage.py runserver"
alias migrate="python manage.py makemigrations && python manage.py migrate"
alias pkms="sudo service postgresql start && cd ~/Code/django_pkms/ && source ~/Code/django_pkms/.venv/bin/activate && serve"
alias dshell="python manage.py shell"
```

## Usage

1. Register a new account or login to an existing one.
2. Create your profile and customize it (e.g., upload a profile picture, add your full name and course details).
3. Add new notes and organize them by course, topic, and subtopic.
4. Assign tags and labels to your notes to make them easy to find and filter.
5. Store important terms and definitions in the glossary section.
6. Set revision objectives and deadlines fro each course.
7. Share your notes with others via email.
8. Log out when you are done.

## Contributions

Contributions to this project are welcome! If you find a bug, want to request a new feature, or have an idea for improvement, please create an issue on this project's GitHub page. If you want to contribute code, please fork the repository and submit a pull request.

## License
<!-- 
This application is licensed under the MIT License. See the LICENSE file for more details. -->
