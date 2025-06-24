# Django
## Table of Contents
1. [Initial Set Up](#Initial-Set-Up)
	1.1. [Set Up a Virtual Environment](#1-set-up-a-virtual-environment)
	1.2. [Install Required Packages](#2-install-required-packages)

2. [Create a Django Project and Application](#create-a-django-project-and-application)
	2.1 [Create Django Project](#1-Create-Django-Project)
	2.2 [Create Django App](#2-Create-Django-App)
	2.3 [Register Django App](#3-Register-Django-App)
	2.4 [Configure URL Routing](#4-Configure-URL-Routing)
		2.4.1 [Configure Application-Level URLs](#Configure-Application-Level-URLs)
		2.4.2 [Configure Application-Level URLs in Project URLs](#Configure-Application-Level-URLs-in-Project-URLs)
	2.5 [Create Sample View to Print Hello World](#5-Create-Sample-View-to-print-Hello-World)
	2.6 [Run the Development Server](#6-Run-the-Development-Server)

3. [HTML Templates in Django](#html-templates-in-django)
	3.1 [Create the Templates Directory](#1-create-the-templates-directory)
	3.2 [Define the Base Template](#2-define-the-base-template)
	3.3 [Create an Inheriting Template](#3-create-an-inheriting-template)
	3.4 [Render the Template from a View](#4-render-the-template-from-a-view)

4. [Create Database Model with Django ORM](#create-database-model-with-django-orm)
	4.1 [Define Your Model](#define-your-model)
	4.2 [Register the Model with Admin Panel](#register-the-model-with-admin-panel)
	4.3 [Apply Migrations](#apply-migrations)

5. [Create a View to Test Functionality](#create-a-view-to-test-functionality)
	5.1 [Create Template](#create-template)
	5.2 [Update Views](#update-views)
	5.3 [Add URL Routing](#add-url-routing)

6. [Working with Django Admin Panel](#working-with-django-admin-panel)
	6.1 [Create Admin User](#create-admin-user)
	6.2 [Run Server & Access Admin](#run-server--access-admin)

7. [Panel Configuration for Django Application](#panel-configuration-for-django-application)

8. [Add First Panel Route](#add-first-panel-route)
	8.1 [Files to be Updated for Adding Panel Route](#Files-to-be-Updated-for-Adding-Panel-Route)

9. [Add New Route](#add-new-route)

10. [Configure Home Page as Default Route](#Configure-Home-Page-as-Default-Route)

<br>

---

## Initial Set Up
### 1. Set Up a Virtual Environment
#### On Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

#### On macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

<br>

---

### 2. Install Required Packages
pip install django panel channels bokeh_django

#### Install Django
```bash
pip install django
```

#### Install Panel
```bash
pip install panel
```

#### Install hvPlot
```bash
pip install hvplot
```

#### Install Matplotlib
```bash
pip install matplotlib
```

#### Install Channels
```bash
pip install channels
```

#### Install bokeh_django
```bash
pip install bokeh_django
```

#### Install openpyxl for Excel Support
```bash
pip install openpyxl
```

#### Save Dependencies
```bash
pip freeze > requirements.txt
```

#### Install from `requirements.txt`
```bash
pip install -r requirements.txt
```
To install without any dependencies
```bash
pip install --no-deps -r requirements.txt
```

<br>

---

## Create a Django Project and Application
### 1. Create Django Project
```bash
django-admin startproject pde
```

<br>

### 2. Create Django App
```bash
cd pde
python manage.py startapp tvt
```

<br>

### 3. Register Django App
Open `pde/pde/settings.py` and add the newly created app to the `INSTALLED_APPS` list:
```py
INSTALLED_APPS = [
	...
	"tvt",
]
```

<br>

### 4. Configure URL Routing
#### Configure Application-Level URLs
Create a new file at `pde\tvt\urls.py` with the following content:
```py
from django.urls import path
from . import views

urlpatterns = [
	path("", views.home, name="home"),
]
```

<br>

#### Configure Application-Level URLs in Project URLs
Modify `pde\pde\urls.py` to include the app's URLs:
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path("admin/", admin.site.urls),
	path("", include("tvt.urls")),
]
```
> Tip: To namespace the app under a route (e.g., `test/`), use: `path("test/", include("tvt.urls"))`

<br>

### 5. Create Sample View to Print Hello World
Update `pde/tvt/views.py`
```py
from django.http import HttpResponse

def home(request):
	return HttpResponse("Hello World!")
```

<br>

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

<br>

---

## HTML Templates in Django
> **Note:** Django templates support inheritance, allowing templates to extend and reuse base structures.

<br>

### 1. Create the Templates Directory
Navigate to your app directory:
```
parallel_edits/tvt/
```
Create a folder named `templates` (ensure the name is exactly `templates`). Each app should have its own `templates` directory where all HTML templates specific to that app are stored.

<br>

### 2. Define the Base Template
In `tvt/templates/base.html`, define a base layout using Django's templating language (Jinja-like syntax):
```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{% block title %}Parallel Edits{% endblock %}</title>
</head>
<body>
	{% block content %}
		<p>This is the main page!</p>
	{% endblock %}
</body>
</html>
```
This base template includes **block tags** that allow child templates to override the `title` and `content` sections.

<br>

### 3. Create an Inheriting Template
Create a file `home.html` inside the same `templates` directory (`tvt/templates/home.html`), and extend the base template:
```html
{% extends "base.html" %}

{% block title %}Home Page{% endblock %}

{% block content %}
	<p>This is the home page!</p>
{% endblock %}
```

<br>

### 4. Render the Template from a View
Update your `home` view in `tvt/views.py`:
```python
from django.shortcuts import render

def home(request):
	return render(request, "home.html")
```

<br>

---

## Cookies/Sessions
### Create a table to store some user data and isolate it from others
pde/tvt/models.py
```py
from django.contrib.auth.models import User
from django.db import models

class Document(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    agile_pn = models.CharField(max_length=100, blank=True)
    agile_rev = models.CharField(max_length=100, blank=True)
    title = models.CharField("Document Title", max_length=255, blank=True)
    doc_type = models.CharField("Document Type", max_length=100, blank=True)
    polarion_id = models.CharField(max_length=100, blank=True)
```

pde/tvt/forms.py
```py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['agile_pn', 'agile_rev', 'title', 'doc_type', 'polarion_id']
        widgets = {
            'agile_pn': forms.TextInput(attrs={'placeholder': 'Agile PN'}),
            'agile_rev': forms.TextInput(attrs={'placeholder': 'Agile Rev'}),
            'title': forms.TextInput(attrs={'placeholder': 'Document Title'}),
            'doc_type': forms.TextInput(attrs={'placeholder': 'Document Type'}),
            'polarion_id': forms.TextInput(attrs={'placeholder': 'Polarion ID'}),
        }
```

pde/tvt/views.py
```py
from django.shortcuts import render, redirect
from .models import Document
from .forms import DocumentForm

def document_table_view(request):
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    if request.method == 'POST':
        if 'add' in request.POST:
            form = DocumentForm(request.POST)
            if form.is_valid():
                doc = form.save(commit=False)
                doc.session_key = session_key
                doc.save()
                return redirect('document_table')
        elif 'delete' in request.POST:
            doc_id = request.POST.get('delete')
            Document.objects.filter(id=doc_id, session_key=session_key).delete()

    form = DocumentForm()
    documents = Document.objects.filter(session_key=session_key)
    return render(request, 'document_table.html', {'form': form, 'documents': documents})
```

pde/tvt/urls.py
```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_table_view, name='document_table'),
]
```

pde/tvt/templates/document_table.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Document Table</title>
    <style>
        table, th, td { border: 1px solid #ccc; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; }
        th { background-color: #f0f0f0; }
    </style>
</head>
<body>
    <h2>Documents</h2>

    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" name="add">➕ Add Document</button>
    </form>

    <table>
        <thead>
            <tr>
                <th style="width:150px;">Agile PN</th>
                <th style="width:150px;">Agile Rev</th>
                <th style="width:350px;">Document Title</th>
                <th style="width:200px;">Document Type</th>
                <th style="width:150px;">Polarion ID</th>
                <th style="width:100px;"></th>
            </tr>
        </thead>
        <tbody>
            {% for doc in documents %}
                <tr>
                    <td>{{ doc.agile_pn }}</td>
                    <td>{{ doc.agile_rev }}</td>
                    <td>{{ doc.title }}</td>
                    <td>{{ doc.doc_type }}</td>
                    <td>{{ doc.polarion_id }}</td>
                    <td>
                        <form method="post" style="display:inline;">
                            {% csrf_token %}
                            <button type="submit" name="delete" value="{{ doc.id }}">🗑️</button>
                        </form>
                    </td>
                </tr>
            {% empty %}
                <tr><td colspan="6">No documents added yet.</td></tr>
            {% endfor %}
        </tbody>
    </table>

    <script>
        // Optional: Save table data in localStorage
        document.addEventListener('DOMContentLoaded', function () {
            const rows = Array.from(document.querySelectorAll('tbody tr')).map(tr => {
                return Array.from(tr.querySelectorAll('td')).slice(0, 5).map(td => td.textContent.trim());
            });
            localStorage.setItem('simple_table_data', JSON.stringify(rows));
            console.log("Saved table to localStorage:", rows);
        });
    </script>
</body>
</html>
```

```sh
python manage.py makemigrations tvt
python manage.py migrate
```

### Adding static files to html templates
1. Create css file and load all css data to it
pde/tvt/static/css/document_table.css

2. Create js file to load all javascript to it
pde/tvt/static/js/document_table.js
```html
<script src="{% static 'js/document_table.js' %}"></script>
```

3. Update template `pde/tvt/templates/document_table.html`
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/document_table.css' %}">
```

```sh
python manage.py collectstatic
```

pde/pde/settings.py
```py
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'tvt' / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

<br>

---

## Create Database Model with Django ORM
Django provides an **Object Relational Mapper (ORM)**, allowing you to define database models using Python code.

### Define Your Model
Update `tvt/models.py`:
```python
from django.db import models

# Create your models here.
class TodoItem(models.Model):
	title = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)
```

<br>

### Register the Model with Admin Panel
Update `tvt/admin.py`:
```python
from django.contrib import admin
from .models import TodoItem

# Register your models here.
admin.site.register(TodoItem)
```

<br>

### Apply Migrations
Run the following commands to create and apply the database schema:
```bash
python manage.py makemigrations
# Note: Run this every time you make changes to your models

python manage.py migrate
# Applies the migrations and updates db.sqlite3
```

<br>

## Create a View to Test Functionality
### Create Template
Create `todos.html` inside `tvt/templates/`:
```html
{% extends "base.html" %}

{% block title %}Todo List{% endblock %}

{% block content %}
	<ul>
		{% for t in todos %}
			<li>
				{{ t.title }}: {% if t.completed %}Completed{% else %}Not Completed{% endif %}
			</li>
		{% endfor %}
	</ul>
{% endblock %}
```
> 📝 Anything inside `{{ variable }}` is treated as a dynamic Django variable.

<br>

### Update Views
Edit `tvt/views.py`:
```python
from django.shortcuts import render
from .models import TodoItem

# Create your views here.
def home(request):
	return render(request, "home.html")

def todos(request):
	items = TodoItem.objects.all()
	return render(request, "todos.html", {"todos": items})
```

<br>

### Add URL Routing
Update your app's `tvt/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("todos/", views.todos, name="todos"),
]
```

<br>

## Working with Django Admin Panel
### Create Admin User
Create a superuser to access the admin panel:
```bash
python manage.py createsuperuser
```

Example credentials:
- **Username**: `cboggaram`
- **Password**: `password`

<br>

### Run Server & Access Admin
Start the development server:
```bash
python manage.py runserver
```

Open your browser and go to: `http://127.0.0.1:8000/admin`
- Log in using the credentials above.
- You’ll see users, groups, and your app (`tvt`) with the `TodoItem` model.
- Create 2 todo items: one marked as **Completed** and one as **Not Completed**.

Then visit: `http://127.0.0.1:8000/todos/`
You’ll see the list of todos displayed from the database.

<br>

---

## Panel Configuration for Django Application
### 1. Update `pde\pde\settings.py`
```py
from bokeh.settings import bokehjs_path
import os

STATICFILES_DIRS = [bokehjs_path()]

INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"tvt",
	"channels",
	"bokeh_django",
]

ASGI_APPLICATION = "pde.routing.application"
```

<br>

### 2. Create `pde\pde\routing.py`
```py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.apps import apps

bokeh_app_config = apps.get_app_config("bokeh_django")

application = ProtocolTypeRouter({
	"websocket": AuthMiddlewareStack(URLRouter(bokeh_app_config.routes.get_websocket_urlpatterns())),
	"http": AuthMiddlewareStack(URLRouter(bokeh_app_config.routes.get_http_urlpatterns())),
})
```

<br>

### 3. Update `pde\pde\asgi.py`
```py
import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pde.settings")
django.setup()
application = get_asgi_application()
```

<br>

### 4. Update `pde/pde/urls.py`
```py
from django.contrib import admin
from django.urls import path, include
from bokeh_django import autoload, static_extensions
from django.apps import apps
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import tvt.pn_app as tvt_app

pn_app_config = apps.get_app_config("bokeh_django")

urlpatterns = [
	path("admin/", admin.site.urls),
	path("", include("tvt.urls")),
]

bokeh_apps = [
	autoload("example", tvt_app.example),
]

urlpatterns += static_extensions()
urlpatterns += staticfiles_urlpatterns()
```

<br>

---

## Add first Panel Route
### Files to be Updated for Adding Panel Route
1. `pde\tvt\pn_app.py`
2. `pde\tvt\panel\example.py`
3. `pde\tvt\templates\example.html`
4. `pde\pde\urls.py`
5. `pde\tvt\urls.py`
6. `pde\tvt\views.py`

<br>

### 1. Create `pde\tvt\pn_app.py`
```py
import panel as pn
from .panel.example import Test

pn.extension()

def example(doc):
	content = Test.get_message()
	content.server_doc(doc)
```

<br>

### 2. Create `pde\tvt\panel\example.py`
```py
import panel as pn

pn.extension()

class Test:
	@staticmethod
	def get_message():
		return pn.pane.Markdown(
			"# My Interactive Dashboard",
			sizing_mode="stretch_width",
			css_classes=["my-title"]
		)
```

<br>

### 3. Create `pde\tvt\templates\example.html`
```html
{% extends "base.html" %}

{% block title %}Example Page{% endblock %}

{% block content %}
	<h1>Hello World</h1>
	{{ script|safe }}
{% endblock %}
```

<br>

### 4. Update `pde\pde\urls.py`
```py
bokeh_apps = [
	autoload("example", tvt_app.example),
]
```

<br>

### 5. Update `pde\tvt\urls.py`
```py
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('example/', views.hello_world),
]
```

<br>

### 6. Update `pde\tvt\views.py`
```py
from django.http import HttpResponse
from bokeh.embed import server_document
from django.shortcuts import render

def home(request):
	return HttpResponse("Hello World!")

def hello_world(request):
	script = server_document("/example/")
	return render(request, "example.html", dict(script=script))
```
> NOTE: The browser's Network tab may not show any activity since this setup does not trigger backend HTTP requests.

<br>

---

## Add New Route
### 1. Create `pde\tvt\panel\histogram.py`
```py
import panel as pn
import numpy as np
from matplotlib.figure import Figure

ACCENT = "purple"

pn.extension()

# Include CSS style here
pn.config.raw_css.append("""
    .my-title {
        font-size: 30px;
        text-align: center;
    }
""")

# Define the Chart class without self
class Chart:
    @staticmethod
    def bar_chart():
        data = np.random.uniform(0, 100, size=100)
        fig = Figure(figsize=(8, 4))
        ax = fig.subplots()
        ax.hist(data, bins=20, color=ACCENT)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 20)
        return fig

    @staticmethod
    def scatter_plot():
        x = np.random.uniform(0, 100, size=100)
        y = np.random.uniform(0, 100, size=100)
        fig = Figure(figsize=(8, 4))
        ax = fig.subplots()
        ax.scatter(x, y, color=ACCENT)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        return fig

    @staticmethod
    def empty_figure():
        fig = Figure(figsize=(8, 4))
        fig.subplots()
        return fig

    @staticmethod
    def show_bar_chart(plot_pane, event):
        plot_pane.object = Chart.bar_chart()

    @staticmethod
    def show_scatter_plot(plot_pane, event):
        plot_pane.object = Chart.scatter_plot()

    @staticmethod
    def clear_plot(plot_pane, event):
        plot_pane.object = Chart.empty_figure()

    @staticmethod
    def say_thankyou(plot_pane, event):
        plot_pane.object = Chart.empty_figure()
        # Include code if necessary

    @staticmethod
    def get_layout():
        button_width = 150
        plot_pane = pn.pane.Matplotlib(Chart.empty_figure(), format='svg', sizing_mode='scale_both')

        bar_button = pn.widgets.Button(name="Show Bar Chart", button_type="primary", width=button_width)
        bar_button.on_click(lambda event: Chart.show_bar_chart(plot_pane, event))

        scatter_button = pn.widgets.Button(name="Show Scatter Plot", button_type="primary", width=button_width)
        scatter_button.on_click(lambda event: Chart.show_scatter_plot(plot_pane, event))

        clear_button = pn.widgets.Button(name="Clear Plot", button_type="primary", width=button_width)
        clear_button.on_click(lambda event: Chart.clear_plot(plot_pane, event))

        thank_you_button = pn.widgets.Button(name="Say Thank You", button_type="primary", width=button_width)
        thank_you_button.on_click(lambda event: Chart.say_thankyou(plot_pane, event))

        top_buttons = pn.Row(pn.layout.HSpacer(), bar_button, scatter_button, pn.layout.HSpacer())
        bottom_buttons = pn.Row(pn.layout.HSpacer(), thank_you_button, pn.layout.HSpacer())

        right_sidebar = pn.Column(
            pn.layout.VSpacer(),
            pn.Row(pn.layout.HSpacer(), clear_button, pn.layout.HSpacer()),
            pn.layout.VSpacer(),
            sizing_mode="stretch_height",
            width=200,
        )

        left_sidebar = pn.Column(
            pn.layout.VSpacer(),
            pn.Row(pn.layout.HSpacer(), clear_button, pn.layout.HSpacer()),
            pn.layout.VSpacer(),
            sizing_mode="stretch_height",
            width=200,
        )

        center_layout = pn.Column(top_buttons, plot_pane, bottom_buttons, sizing_mode='stretch_both')

        title_pane = pn.pane.Markdown(
            "# My Interactive Dashboard",
            sizing_mode="stretch_width",
            css_classes=["my-title"]
        )

        full_layout = pn.Column(
            title_pane,
            pn.Row(
                left_sidebar,
                center_layout,
                right_sidebar,
                sizing_mode='stretch_both'
            ),
            sizing_mode='stretch_both'
        )

        return full_layout
```

<br>

### 2. Update `pde\tvt\pn_app.py`
```py
import panel as pn
from .panel.example import Test
from .panel.histogram import Chart

pn.extension()

def example(doc):
    content = Test.get_message()
    content.server_doc(doc)

def histogram(doc):
    layout = Chart.get_layout()
    layout.server_doc(doc)
```

<br>

### 3. Update `pde\tvt\views.py` with new route
```py
from django.http import HttpResponse
from bokeh.embed import server_document
from django.shortcuts import render

def home(request):
    return HttpResponse("Hello World!")

def hello_world(request):
    script = server_document("/example/")
    return render(request, "example.html", dict(script=script))

def histogram(request):
    script = server_document("/histogram/")
    return render(request, "histogram.html", dict(script=script))
```

<br>

### 4. Update `pde\tvt\urls.py` to include the new route in Django App
```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('example/', views.hello_world),
    path('histogram/', views.histogram),
]
```

<br>

### 5. Update `pde\pde\urls.py` to include the new route in Bokeh Apps
```py
from django.contrib import admin
from django.urls import path, include
from bokeh_django import autoload, static_extensions
from django.apps import apps
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import tvt.pn_app as tvt_app

pn_app_config = apps.get_app_config("bokeh_django")

urlpatterns = [
	path("admin/", admin.site.urls),
	path("", include("tvt.urls")),
]

bokeh_apps = [
    autoload("example", tvt_app.example),
    autoload("histogram", tvt_app.histogram),
]

urlpatterns += static_extensions()
urlpatterns += staticfiles_urlpatterns()
```

### 6. Create `pde\tvt\templates\histogram.html`
```html
{% extends "base.html" %}

{% block title %}Histogram{% endblock %}

{% block content %}
  {{ script|safe }}
{% endblock %}
```

<br>

---

## Configure Home Page as Default Route
### 1. Update `pde\pde\urls.py`
```py
from django.contrib import admin
from django.urls import path, include
from bokeh_django import autoload, static_extensions
from django.apps import apps
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import tvt.pn_app as tvt_app

pn_app_config = apps.get_app_config("bokeh_django")

urlpatterns = [
	path("admin/", admin.site.urls),
	path("", include("tvt.urls")),
]

bokeh_apps = [
    autoload("home", tvt_app.home),
    autoload("histogram", tvt_app.histogram),
]

urlpatterns += static_extensions()
urlpatterns += staticfiles_urlpatterns()
```

<br>

### 2. Create `pde\tvt\panel\home.py`
```py
import panel as pn

pn.extension()

class Test:
    @staticmethod
    def get_message():
        return pn.pane.Markdown(
            "# Trace Vizualization Tool",
            sizing_mode="stretch_width",
            css_classes=["my-title"]
        )
```

<br>

### 3. Create `pde\tvt\templates\home.html`
```html
{% extends "base.html" %}

{% block title %}Home Page{% endblock %}

{% block content %}
  {{ script|safe }}
{% endblock %}
```

<br>

### 4. Update `pde\tvt\pn_app.py`
```py
import panel as pn
from .panel.home import Test
from .panel.histogram import Chart

pn.extension()

def home(doc):
    content = Test.get_message()
    content.server_doc(doc)

def histogram(doc):
    layout = Chart.get_layout()
    layout.server_doc(doc)
```

<br>

### 5. Update `pde\tvt\urls.py`
```py
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
    path('histogram/', views.histogram),
]
```

<br>

### 6. Update `pde\tvt\views.py`
```py
from django.http import HttpResponse
from bokeh.embed import server_document
from django.shortcuts import render

def home(request):
    script = server_document("/home/")
    return render(request, "home.html", dict(script=script))

def histogram(request):
    script = server_document("/histogram/")
    return render(request, "histogram.html", dict(script=script))
```

<br>

---

## Include multiple files into one route
```py
from .panel.app_title import TitleClass
from .panel.cytoscape import Cytoscape
from .panel.simple_table import SimpleTable

def home(doc):
    title = TitleClass.get_title()
    graph = Cytoscape.show_dashboard()
    sim_table = SimpleTable.create_table()
    layout = pn.Column(title, graph, sim_table)
    layout.server_doc(doc)
```

<br>

---

## Sessions in Django
### Creating a session
```python
request.session['key'] = 'value'
```

<br>

### Reading a session
```python
val = request.session['key']          # Raises KeyError if not found
val = request.session.get('key')      # Returns None if not found
```

<br>

### Passing session values to a Panel Django app
`pde/tvt/views.py`
```python
from bokeh.embed import server_document
from django.shortcuts import render
def hello_world(request):
    request.session["key"] = "Chai"
    val = request.session.get("key")
    context = {"key": val}
    script = server_document("/home/")
    return render(request, "home.html", {"script": script, "context": context})
```

<br>

`pde/tvt/templates/home.html`
```html
{{ context.key }}
```

<br>

---

## Cookies in Django
### Setting a cookie
`pde/tvt/views.py`
```python
from bokeh.embed import server_document
from django.shortcuts import render
def traces(request):
    script = server_document("/traces/")
    response = render(request, "traces.html", {"script": script})
    response.set_cookie(key="key1", value="value1")
    return response
```

<br>

`pde/tvt/templates/traces.html`
```html
{{ context.key }}
```

<br>

---

### Setting a cookie with expiry (auto-deletion)
`pde/tvt/views.py`
```python
from datetime import datetime, timedelta
def traces(request):
    script = server_document("/traces/")
    response = render(request, "traces.html", {"script": script})
    expires = datetime.now() + timedelta(seconds=50)
    response.set_cookie(key="key1", value="value1", expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT"))
    return response
```

<br>

### Reading a cookie
`pde/tvt/views.py`
```python
def hello_world(request):
    script = server_document("/home/")
    context = request.COOKIES.get("key1")
    return render(request, "home.html", {"script": script, "context": context})
```
`pde/tvt/templates/home.html`
```html
{{ context }}
```
<br>

### Passing JSON data via cookies
```python
COLOR_DATA = [
    {"color": "red", "value": "#f00"},
    {"color": "green", "value": "#0f0"},
    {"color": "blue", "value": "#00f"},
    {"color": "cyan", "value": "#0ff"},
    {"color": "magenta", "value": "#f0f"},
    {"color": "yellow", "value": "#ff0"},
    {"color": "black", "value": "#000"},
]
```

#### Storing JSON in a cookie
`pde/tvt/views.py`
```python
import json
from bokeh.embed import server_document
def traces(request):
    script = server_document("/traces/")
    response = render(request, "traces.html", {"script": script})
    json_data = json.dumps(COLOR_DATA)
    response.set_cookie("color_data", json_data, max_age=3600)
    return response
```

### Retrieving JSON from a cookie
`pde/tvt/views.py`
```python
def hello_world(request):
    script = server_document("/home/")
    context = request.COOKIES.get("color_data")  # This is a JSON string
    return render(request, "home.html", {"script": script, "context": context})
```
`pde/tvt/templates/home.html`
```html
{{ context }}
```

<br>

---

### Get session id
views.py
```python
def traces(request):
    script = server_document("/traces/")
    SESSION_ID = request.session.session_key or request.session.save() or request.session.session_key
    print(f"Session ID (traces): {SESSION_ID}")
    response = render(request, "traces.html", {"script": script, "session_id": SESSION_ID})
    return response
```

<br>

---

## Caching
### Using Javascript to cache
1. Using `document.cookie`
```py
storage_key = "simple_table_data"
html = pn.pane.HTML("")
EXPIRE = 900

@staticmethod
def save_to_cookies():
    pn.state.cookies[SimpleTable.storage_key] = json.dumps(SimpleTable.data)
    data_str = json.dumps(SimpleTable.data).replace('"', '\\"')
    SimpleTable.html.object = f"""
    <script>
        document.cookie = "{SimpleTable.storage_key}={data_str}; Expires=Mon, 16 Jun 2025 23:59:00 GMT; SameSite=Lax; path=/";
    </script>
    """
```

<br>

2. Using `localStorage`
```py
storage_key = "simple_table_data"
html = pn.pane.HTML("")
EXPIRE = 900

@staticmethod
def save_to_cookies():
    pn.state.cookies[SimpleTable.storage_key] = json.dumps(SimpleTable.data)
    data_str = json.dumps(SimpleTable.data).replace('"', '\\"')
    expiry = (datetime.utcnow() + timedelta(seconds=SimpleTable.EXPIRE)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    SimpleTable.html.object = f"""
    <script>
        localStorage.setItem('{SimpleTable.storage_key}', '{data_str}')
    </script>
    """

@staticmethod
def load_from_cookies():
    SimpleTable.html.object = f"""
    <script>
        const data = localStorage.getItem('{SimpleTable.storage_key}');
        console.log('Data loaded from localStorage:', data);
    </script>
    """
```

