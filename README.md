#  Fitness Booking API

A Django REST API for managing fitness class schedules and client bookings. Built for scheduling, tracking, and managing fitness sessions — with Swagger-powered documentation for easy testing.

---

## 🔗  Repository

GitHub: [https://github.com/akashakerror404/BOOKING](https://github.com/akashakerror404/BOOKING)

---

##  Features

- List upcoming fitness classes
- Book slots in a class
- View all upcoming bookings by email
- Fully documented via Swagger (`drf-yasg`)
- Uses Django REST Framework

---

##  Technologies Used

- Django 4.x
- Django REST Framework
- drf-yasg (Swagger)
- SQLite3 (default)
- Python 3.10+

---

##  Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/akashakerror404/BOOKING.git
cd BOOKING
python -m venv env
env\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Apply migrations:
```bash
python manage.py migrate
python manage.py runserver

```

## Open the Swagger API docs:
 - Swagger UI: http://127.0.0.1:8000/swagger/
 - Redoc: http://127.0.0.1:8000/redoc/

## Example Requests:
Get Available Classes
```bash
curl -X GET "http://localhost:8000/api/classes/?timezone=America/New_York"

```
Create a Booking
```bash
curl -X POST "http://localhost:8000/api/book/" \
-H "Content-Type: application/json" \
-d '{"fitness_class": 1, "client_name": "Ram", "client_email": "ram@gmail.com"}'
```
Get Client Bookings
```bash
curl -X GET "http://localhost:8000/api/bookings/?email=ram@gmail.com"
```
Testing
```bash
python manage.py test
```
