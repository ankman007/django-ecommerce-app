# Project Description 
Django-based ecommerce store leveraging HTMX for dynamic frontend updates without full page reloads and integrated with Stripe for secure & flexible checkout processing.

## Technology used

- Django
- HTMX
- Bootstrap
- Sqlite3
- Stripe API

## To set up this project

1. cd into project directory
2. Create a new .env file by copying the env.example file
3. Open the .env file and update it with your credentials as needed
4. Build docker image with `docker-compose build`
5. Start container with `docker-compose up`
6. Project should be live at localhost port 8000.