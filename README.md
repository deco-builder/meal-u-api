# MealU API

MealU addresses the difficulty of providing university students with easy access to healthy, locally-sourced meals. Due to their hectic schedules, many students struggle to find time to prepare healthy meals and frequently rely on fast foods.

---

## Features

- User authentication (with JWT-based access and refresh tokens)
- Role-based permissions for `Client`, `Warehouse`, and `Courier` users
- Ingredient management with dynamic pricing based on preparation type
- Recipe and mealkit management with the nutrition details
- Order management including cart, checkout, processing and delivery
- Integration with AWS S3 for image storage

---

## Tech Stack

### Backend

- Django
- Django REST Framework
- PostgreSQL
- AWS S3 for media storage

### Others

- Docker for containerization
- AWS EC2 for hosting

---

## Installation

To install and set up the project locally, follow these steps:

1. **Clone the repository:**
    
    ```bash
    git clone https://github.com/deco-builder/meal-u-api
    cd meal-u-api
    ```
    
2. **Set up a virtual environment:**
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    
3. **Install dependencies:**
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Set up PostgreSQL:**
    - Install PostgreSQL on your local machine or use a cloud instance.
    - Create a database for the project and update the `.env` file with the connection details.
5. **Set up AWS S3 for media storage:**
    - Create an S3 bucket and configure your access keys.
    - Update the `.env` file with `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_STORAGE_BUCKET_NAME`.
    - See configuration for more details for `.env`
6. **Run database migrations:**
    
    ```bash
    python manage.py migrate
    ```
    
7. **Run the development server:**
    
    ```bash
    python manage.py runserver
    ```
    

---

## Configuration

Ensure the following configurations are set correctly in your `.env` file:

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
DEBUG=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
```

### Static & Media Files

The project is set up to serve static files via S3:

- `STATIC_URL`: Files like CSS, JS, and images are stored on S3.
- `MEDIA_URL`: User-uploaded images are also stored in S3 buckets.

---

## Deployment

To deploy the project on AWS EC2, follow these steps:

1. **Set up an EC2 instance** with Ubuntu 24.04.
2. **Install Docker** and configure it to run your app using the `Dockerfile`.
3. **Set up AWS S3** for media storage, and configure the app to use S3 for image uploads.
4. **Set environment variables** for your application.
5. **Run the Docker container** to serve the application.

---