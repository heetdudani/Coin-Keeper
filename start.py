import os

print ("1 Run server")
print ("2 makemigrations")
print ("3 migrate")

a = int(input('enter choise : '))

if a == 1:
    os.system("python manage.py runserver 3599")
    # b = int(input("Custom server if yes 1 / no 0 : "))
    # if b == 1:
    #     s = int(input("server : "))
    #     os.system(f"python manage.py runserver {s}")
    # elif b==0:
    #     os.system("python manage.py runserver")
    # else:
    #     print("invalid")

elif a==2:
    os.system("python manage.py makemigrations")
    
elif a==3:
    os.system("python manage.py migrate")
    
else :
    print("invalid")
    
