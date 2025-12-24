# Ecommerce Django App

## Overview

This is a basic ecommerce application built with Django. It includes functionality for displaying products, viewing products by category, managing a shopping cart, and user authentication with login functionality.

## Features

* User authentication (login, logout, register)
* Product listing with images
* Product detail page
* Category-based product filtering
* Shopping cart management
* Bootstrap card layout for products
* Static images for demonstration

## Project Structure

```
ecommerce_project/
├── store/
│   ├── migrations/
│   ├── static/store/images/   # Product images
│   ├── templates/store/       # HTML templates
│   │   ├── product_list.html
│   │   ├── products_by_category.html
│   │   ├── login.html
│   │   └── base.html
│   ├── views.py
│   └── models.py
├── ecommerce_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
```

2. Navigate to the project directory:

```bash
cd ecommerce-django-app/ecommerce_project
```

3. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open your browser and go to `http://127.0.0.1:8000/` to view the site.

## User Authentication

* Users can log in via the `login.html` template.
* Ensure `django.contrib.auth` is included in `INSTALLED_APPS`.
* Login URL can be configured in `settings.py` as:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

## Notes

* Static images are stored in `store/static/store/images/`.
* Templates are located in `store/templates/store/`.
* Make sure `store` is included in `INSTALLED_APPS` in `settings.py`.

## Author

* Gogo Shedrack
