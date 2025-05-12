cd backend
pip install mysql

#create a database named **library_db**

#USER CREATION USING TERMINAL

python manage.py shell



from django.contrib.auth.models import User

users_data = [
    {'username': 'student1', 'email': 'student1@library.com', 'password': 'Student2023!'},
    {'username': 'student2', 'email': 'student2@library.com', 'password': 'Student2023!'},
    {'username': 'student3', 'email': 'student3@library.com', 'password': 'Student2023!'},
    {'username': 'student4', 'email': 'student4@library.com', 'password': 'Student2023!'},
    {'username': 'student5', 'email': 'student5@library.com', 'password': 'Student2023!'},
    {'username': 'student6', 'email': 'student6@library.com', 'password': 'Student2023!'},
    {'username': 'student7', 'email': 'student7@library.com', 'password': 'Student2023!'},
    {'username': 'student8', 'email': 'student8@library.com', 'password': 'Student2023!'},
    {'username': 'student9', 'email': 'student9@library.com', 'password': 'Student2023!'},
    {'username': 'student10', 'email': 'student10@library.com', 'password': 'Student2023!'},
]

for data in users_data:
    user = User.objects.create_user(**data)
    print(f"Created user: {user.username}")

print("\nAll users:")
for user in User.objects.all():
    print(f"Username: {user.username}, Staff: {user.is_staff}, Superuser: {user.is_superuser}")



#cd frontend

npm install
npm install axios
