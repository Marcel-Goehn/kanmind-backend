
# KanMind Backend

This project is a backend for a Kanban board application built with **Django** and **Django REST Framework**.  
It provides a RESTful API for managing boards, tickets, and comments.


## Documentation

[API Documentation](https://linktodocumentation)


## Tech Stack

**Server:** Python, Django, Django REST Framework


## Features

- User authentication
- Board-based permission system (owner and members)
- Ticket management with status and priority
- Assignment and review workflow
- Comment system for tickets
- RESTful API design


## Installation



Clone the repository:
```bash
git clone https://github.com/Marcel-Goehn/kanmind-backend.git
```
Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

Migrate the database:
```bash
python manage.py migrate
```

Start development server:
```bash
python manage.py runserver
```

    
## Related

Here is the related frontend

[KanMind Frontend](https://github.com/Developer-Akademie-Backendkurs/project.KanMind)


## Authors

- [@Marcel-Goehn](https://github.com/Marcel-Goehn)


## License


This project is licensed under the MIT License.


## Feedback

If you have any feedback, feel free to reach out: 
marcelgoehn@googlemail.com

