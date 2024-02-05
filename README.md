# Blogicum: The Social Media Of The Personal Diaries

This is a web application written in Django to help people share their thoughts/ideas with others. Users can create their own diary (page) and generate content. The content is represented by a post that includes a location, category and message. Users can navigate to specific categories and view all related posts. They can also visit other users' pages, read and comment on them.

## Quick start

Navigate to the directory where you want the project to reside.

```bash
git clone git@github.com:sava9ecode/django_sprint1.git
python3 -m venv venv && source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Navigate to the `blogicum` directory and apply migrations.

```bash
python manage.py migrate
```

Make sure that the file `manage.py` is present in the current directory and launch a development server.

```bash
python manage.py runserver
```

Open your browser at http://127.0.0.1:8000.

## Run the tests

Navigate to the `django_sprint1` directory and execute the following commands.

```bash
pytest
flake8
```

## Author

* [Evgeny Savage](https://github.com/sava9ecode)
