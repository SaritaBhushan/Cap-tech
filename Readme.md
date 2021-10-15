Requirement:
- Perform CRUD
- maintain tables for User_details, user_login_status with custom user_role and user_permission model (DO NOT USE THE DEFAULT DJANGO ROLE AND PERMISSIONS)
- User authentication using JWT Token 
- containerize the app using Docker

cd Cap-tech/
docker-compose -f docker-compose.yml --env-file .env up
docker-compose -f docker-compose.yml --env-file .env down

sudo docker exec -it <django_container_id>  /bin/bash
ls
python manage.py migrate
exit

sudo docker exec -it <mysql_container_id>  /bin/bash
mysql -u mig -p
use UserJWTAuth;
show tables;
exit;
exit