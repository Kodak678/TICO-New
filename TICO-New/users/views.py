from django.shortcuts import render, redirect
from django.contrib import messages
import sqlite3
import tensorflow as tf
import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Tells program to ignore an unimportant warning
LoggedInUser = ""

class User:
    def __init__(self,Username, Password,Firstname, Lastname, Email, relative):
        self.Username = Username
        self.Password = Password
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Email = Email
        self.relative = relative
     

    def getUsername(self):
        return self.Username

    def getFirstname(self):
        return self.Firstname

    def getLastname(self):
        return self.Lastname

    def getEmail(self):
        return self.Email

    def getrelative(self):
        return self.relative

    def resetPassword(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        words = ["Chess", "Board", "Pawn", "Knights", "king"]
        code = random.choice(words)
        count = 0
        for i in code:
            count+= ord(i)
        tempPass = self.Password - count
        with conn:
            c.execute("UPDATE UserInfo SET Password = (:tempPass)  WHERE Username = (:Username)", {'Username': self.Username, 'tempPass': tempPass})

    
    def updateDetails(self,Password,Firstname, Lastname, Email):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE UserInfo SET Password = (:Password), 
            Firstname = (:Firstname), Lastname = (:Lastname), 
            Email = (:Email)  WHERE Username = (:Username)""", 
            {'Username': self.Username, 'Password': Password, 'Firstname': Firstname, 'Lastname': Lastname, 'Email': Email})

# conn = sqlite3.connect('users.db')
# c = conn.cursor()

# c.execute("""CREATE TABLE UserInfo (    
#     Username text,
#     Password text,
#     FirstName text,
#     LastName text,
#     Email text,
#     relative float
# )""")

# conn.commit()
# conn.close()

def hashPassword(Username, Password):
    Pass = Username + Password
    Password = ""
    Sum = 0
    for character in Pass:
        Password += str(ord(character)) # ord() function returns the unicode value of an ASCII character
        Sum += ord(character)
    Password =  int(Password) - Sum
    Password = str(Sum) + str(Password) 
    return Password



def login(request):
    return render(request, 'login.html')

def forgotten(request):
    return render(request, 'forgotten.html')

def register(request):
    return render(request, 'register.html')

def authenticate(request):
    global LoggedInUser
    username = request.POST['Username']
    password = request.POST['Password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    if ((not username) or (not password)):
        messages.error(request, f'Empty field/s submitted!')
        return redirect('login.html')
    else :
        password = hashPassword(username, password)
        c.execute("SELECT * FROM UserInfo WHERE Username = (:Username) AND Password = (:Password)", {'Username': username, 'Password':password})

        if len(c.fetchall()) == 1:
            messages.success(request,f'User with username: {username} has been successfully logged in!' )
            with conn:
                record = c.execute("SELECT Username, Password, Firstname,Lastname, Email, relative FROM UserInfo WHERE Username =(:Username)", {'Username': username})
                r = list(record)
            User1 = User(r[0][0],r[0][1],r[0][2],r[0][3],r[0][4],r[0][5])
            LoggedInUser = User1
            return render(request, 'mainpage.html', {'Username' : username})
        else:
            messages.error(request, 'Incorrect username and/or password...')
            return redirect('login.html')

def forgottenLogin(request):
    global LoggedInUser
    username = request.POST['Username']
    password = request.POST['Password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    if ((not username) or (not password)):
        messages.error(request, f'Empty field/s submitted!')
        return redirect('login.html')
    else :
        with conn:
            c.execute("SELECT * FROM UserInfo WHERE Username = (:Username) AND Password = (:Password)", {'Username': username, 'Password':password})

        if len(c.fetchall()) == 1:
            messages.success(request,f'User with username: {username} has been successfully logged in!' )
            with conn:
                record = c.execute("SELECT Username, Password, Firstname,Lastname, Email, relative FROM UserInfo WHERE Username =(:Username)", {'Username': username})
                r = list(record)
            User1 = User(r[0][0],r[0][1],r[0][2],r[0][3],r[0][4],r[0][5])
            LoggedInUser = User1
            return render(request, 'mainpage.html', {'Username' : username})
        else:
            messages.error(request, 'Incorrect username and/or password...')
            return redirect('forgotten.html')
    

def create_model():
    model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape = (14,8,8)), 
                                        tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                        tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)])
    model.compile(optimizer=tf.keras.optimizers.Adam(5e-4), loss= 'mean_squared_error')
    return model



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
        
        c.execute("SELECT * FROM UserInfo WHERE Username = (:Username)", {'Username': Username})

        if len(c.fetchall()) == 0:
            messages.success(request,f'User with username: {Username} has been successfully registered.' )

            model = create_model()
            model.load_weights(f'./users/TICOweights/TICO')
            model.save(f'./models/{Username}')
            #The above code creates a model with some basic training for each user so that it can then be loaded for the minimax
            Password = hashPassword(Username, Password)
            with conn:
                c.execute("INSERT INTO UserInfo VALUES (?,?,?,?,?,?)", (Username, Password, FirsName, LastName, Email, 0.0))
            return redirect('mainpage.html')
        else:
            messages.error(request, f'User not registered username: {Username} is already taken!')
            return redirect('register.html')
    
    

  




