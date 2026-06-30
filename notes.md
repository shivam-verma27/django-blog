# Django Revision Notes

## 1. MVT Architecture

```text
User Request
     ↓
URL
     ↓
View
     ↓
Model (Database)
     ↓
Template
     ↓
Response
```

### URL

Maps URL to a view.

```python
path('', views.home, name='home')
```

### View

Contains business logic.

```python
def home(request):
    return render(request,'blog/home.html')
```

### Model

Defines database structure.

```python
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
```

### Template

Displays data.

```html
{{ post.title }}
```

---

# 2. ORM Queries

## Get All Posts

```python
Post.objects.all()
```

Returns QuerySet.

---

## Get One Post

```python
Post.objects.get(id=1)
```

Returns single object.

---

## Filter Posts

```python
Post.objects.filter(title='Django')
```

Returns QuerySet.

---

## Delete

```python
post = Post.objects.get(id=1)
post.delete()
```

---

## Update

```python
post = Post.objects.get(id=1)

post.title = "New Title"
post.save()
```

---

# 3. CRUD

## Create

```python
post = Post(
    title=title,
    content=content
)

post.save()
```

---

## Read

```python
Post.objects.all()
Post.objects.get(id=1)
```

---

## Update

```python
post.title = title
post.content = content
post.save()
```

---

## Delete

```python
post.delete()
```

---

# 4. Forms

## Empty Form

```python
form = PostForm()
```

Used for GET request.

---

## Filled Form

```python
form = PostForm(request.POST)
```

Used for POST request.

---

## Validation

```python
if form.is_valid():
```

Checks:

* Required fields
* Max length
* Data type
* Custom validation

---

## Save

```python
form.save()
```

Stores data in database.

---

# 5. cleaned_data

```python
form.cleaned_data['title']
```

Returns validated and cleaned data.

Example:

Input:

"     Django Basics     "

Output:

"Django Basics"

---

# 6. Custom Validation

```python
def clean_title(self):

    title = self.cleaned_data['title']

    if len(title) < 5:
        raise forms.ValidationError(
            "Title must be at least 5 characters."
        )

    return title
```

### ValidationError

User error.

Shows error on form.

Does NOT crash application.

---

# 7. Messages Framework

## Import

```python
from django.contrib import messages
```

---

## Success Message

```python
messages.success(
    request,
    "Post created successfully!"
)
```

---

## Display

```html
{% if messages %}
    {% for message in messages %}
        <p>{{ message }}</p>
    {% endfor %}
{% endif %}
```

Usually placed in base.html.

---

# 8. Template Inheritance

## Base Template

```html
{% block content %}
{% endblock %}
```

---

## Child Template

```html
{% extends 'blog/base.html' %}

{% block content %}
...
{% endblock %}
```

### Why?

Change one file.

Reflect everywhere.

DRY Principle.

---

# 9. Static Files

## Folder Structure

blog/
static/
blog/
style.css

---

## Base Template

```html
{% load static %}

<link rel="stylesheet"
href="{% static 'blog/style.css' %}">
```

---

# 10. CSS Concepts

## Padding

Distance between content and border.

```css
padding:10px;
```

---

## Margin

Distance outside border.

```css
margin:10px;
```

---

## Border

```css
border:1px solid black;
```

---

## Hover

```css
a:hover{
    color:red;
}
```

Only active when mouse is over element.

---

# 11. Semantic HTML

## Good

```html
<nav>
<header>
<article>
<footer>
```

Meaningful tags.

---

## Generic

```html
<div>
<span>
```

No meaning.

---

# 12. Search Feature

## Form

```html
<form method="GET">
```

Search uses GET.

---

## Get Query

```python
query = request.GET.get('q')
```

---

## Search

```python
Post.objects.filter(
    title__icontains=query
)
```

---

## Search Title OR Content

```python
from django.db.models import Q

Post.objects.filter(
    Q(title__icontains=query) |
    Q(content__icontains=query)
)
```

---

# 13. Q Objects

## OR

```python
Q(title__icontains=query) |
Q(content__icontains=query)
```

---

## AND

```python
Q(title__icontains=query) &
Q(content__icontains=query)
```

---

# 14. Truthy and Falsy Values

Falsy:

```python
None
""
[]
{}
0
False
```

Example:

```python
if query:
```

Runs only if query has value.

---

# 15. Django Learning Order

Completed:

✓ Models
✓ Views
✓ URLs
✓ Templates
✓ CRUD
✓ ORM
✓ Forms
✓ Validation
✓ Messages
✓ Static Files
✓ Search
✓ CSS Basics

Next:

1. Authentication
2. Relationships
3. Class Based Views
4. Pagination
5. File Uploads
6. Deployment
7. Django REST Framework

```
```
