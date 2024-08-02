# Welcome to IndiBot

.env file:

    Token=
    API_URL=
    API_TOKEN=
    
Deploy:
    
    docker-compose up --build -d
    docker-compose exec django bash entrypoint.sh
    
    Create API_TOKEN
    1. docker exec -it <Container> bash
    2. python manage.py drf_create_token admin
    3. copy the token to .env file

    
Test Bot:

    t.me/inditest_bot
    
Prod Bot:
    
    Coming Soon...
   
