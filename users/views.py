from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import sqlite3



# conn = sqlite3.connect('users.db')
# c = conn.cursor()

# c.execute("""CREATE TABLE UserInfo (
#     Username text,
#     FirstName text,
#     LastName text,
#     Email text
# )""")

# c.execute("""CREATE TABLE Users (
#     Username text,
#     Password text
# )""")

# conn.commit()
# conn.close()

def hashPassword(Username, Password):
    Pass = Username + Password
    Password = ""
    Sum = 0
    for character in Pass:
        Password += str(ord(character))
        Sum += ord(character)
    Password =  int(Password) - Sum
    Password = str(Sum) + str(Password) 
    return Password



def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def authenticate(request):
    username = request.POST['Username']
    password = request.POST['Password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    if ((not username) or (not password)):
        messages.error(request, f'Empty field/s submitted!')
        return redirect('login.html')
    else :
        password = hashPassword(username, password)
        c.execute("SELECT * FROM Users WHERE Username = (:Username) AND Password = (:Password)", {'Username': username, 'Password':password})

        if len(c.fetchall()) == 1:
            messages.success(request,f'User with username: {username} has been successfully logged in!' )
            return redirect('mainpage.html')
        else:
            messages.error(request, 'Incorrect username and/or password...')
            return redirect('login.html')
    

def addUser(request):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    FirstName = request.POST['FirstName']
    LastName = request.POST['LastName']
    Email = request.POST['Email']
    Username = request.POST['Username']
    Password = request.POST['Password']
    PasswordRepeat = request.POST['PasswordRepeat']

    FirsName = FirstName.strip()
    LastName = LastName.strip()
    Email = Email.strip()
    Username = Username.strip()
    Password = Password.strip()
    PasswordRepeat = PasswordRepeat.strip()



    if ((not Username) or (not Password) or (not FirsName) or (not LastName) or (not("@" in Email)) or (not(Password == PasswordRepeat))):
        messages.error(request, f'Empty or invalid fields submitted!')
        return redirect('register.html')
    else :
        
        c.execute("SELECT * FROM Users WHERE Username = (:Username)", {'Username': Username})

        if len(c.fetchall()) == 0:
            messages.success(request,f'User with username: {Username} has been successfully registered.' )
            Password = hashPassword(Username, Password)
            with conn:
                c.execute("INSERT INTO Users VALUES (?,?)", (Username, Password))
                c.execute("INSERT INTO UserInfo VALUES (?,?,?,?)", (Username, FirsName, LastName, Email))
            return redirect('mainpage.html')
        else:
            messages.error(request, f'User not registered username {Username} is already taken!')
            return redirect('register.html')
    
    

  




