from django.shortcuts import render, redirect
from django.contrib import messages
import sqlite3
import tensorflow as tf
import random
from email.message import EmailMessage
import ssl
import smtplib

LoggedInUser = ""
from playground.views import userSet
class User:
    def __init__(self,Username,Firstname, Lastname, Email, relative):
        self.__Username = Username
        self.__Firstname = Firstname
        self.__Lastname = Lastname
        self.__Email = Email
        self.relative = relative
     

    def getUsername(self):
        return self.__Username

    def getFirstname(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT Firstname FROM UserInfo WHERE Username =(:Username)", {'Username': self.__Username})
        self.__Firstname = list(c.fetchall())[0][0]
        return self.__Firstname

    def getLastname(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT Lastname FROM UserInfo WHERE Username =(:Username)", {'Username': self.__Username})
        self.__Lastname = list(c.fetchall())[0][0]
        return self.__Lastname

    def getEmail(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT Email FROM UserInfo WHERE Username =(:Username)", {'Username': self.__Username})
        self.__Email = list(c.fetchall())[0][0]
        return self.__Email

    def getrelative(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT relative FROM UserInfo WHERE Username =(:Username)", {'Username': self.__Username})
        self.relative = list(c.fetchall())[0][0]
        return self.relative

    def updateRelative(self, newRelative):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE UserInfo SET relative = (:Relative) WHERE Username = (:Username)""", 
            {'Username': self.__Username, 'Relative':newRelative})
   

    def updateDetails(self,Password,Firstname, Lastname, Email):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE UserInfo SET Password = (:Password), 
            Firstname = (:Firstname), Lastname = (:Lastname), 
            Email = (:Email)  WHERE Username = (:Username)""", 
            {'Username': self.__Username, 'Password': Password, 'Firstname': Firstname, 'Lastname': Lastname, 'Email': Email})
    

conn = sqlite3.connect('users.db')
c = conn.cursor()

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

def leaderboard(request):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT Username from UserInfo ORDER BY relative DESC")
    users = c.fetchall()
    c.execute("SELECT relative from UserInfo ORDER BY relative DESC")
    scores = c.fetchall()
    return render(request, 'leaderboard.html',{'users': users, 'scores': scores})

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
            with conn:
                record = c.execute("SELECT Username,Firstname,Lastname, Email, relative FROM UserInfo WHERE Username =(:Username)", {'Username': username})
                r = list(record)
            User1 = User(r[0][0],r[0][1],r[0][2],r[0][3],r[0][4]) #Intantiating the user object
            LoggedInUser = User1 #Storing the user object as a global variable so it can be accessed anywhere
            userSet(LoggedInUser) #Sending the user object to the playground.views file
            messages.success(request,f'User with username: {username} has been successfully logged in!' )
            return render(request, 'mainpage.html', {'Username' : username})
        else:
            messages.error(request, 'Incorrect username and/or password...')
            return redirect('login.html')

def forgottenLogin(request):
    username = request.POST['Username']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    if (not username):
        messages.error(request, f'Please enter a Username...')
        return redirect('forgotten.html')

    else :
        with conn:
            c.execute("SELECT * FROM UserInfo WHERE Username = (:Username)", {'Username': username})
        if len(c.fetchall()) == 1:
            with conn:
                    record = c.execute("SELECT Firstname,Lastname, Email FROM UserInfo WHERE Username =(:Username)", {'Username': username})
                    r = list(record)
            firstname = r[0][0]
            lastname = r[0][1]
            email_receiver = r[0][2]
            send_email(email_receiver,firstname,lastname, username)
            messages.success(request,f'Temporary password has been sent, please check your emails...' )
            return render(request, 'login.html')
        else:
            messages.error(request, 'Username was not found...')
            return redirect('forgotten.html')
     

    



def create_model():
    model = tf.keras.models.Sequential( #The tf.keras.models.Sequential function is used to create a sequential model, which is a linear stack of layers.
        [tf.keras.layers.Flatten(input_shape = (14,8,8)), #layer is used to flatten the input shape of (14,8,8) to a 1D array of size 896.
                                        tf.keras.layers.Dense(128, activation=tf.keras.activations.relu), #layer with 128 units and ReLU activation function is added to the model.
                                        tf.keras.layers.Dense(32, activation=tf.keras.activations.relu), #layer with 32 units and ReLU activation function is added to the model.   
                                        tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid),#layer with 1 unit and sigmoid activation function is added to the model.
                                        ]
                                        )
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss = tf.keras.losses.mean_squared_error, metrics=["accuracy"])
    return model
#This function creates the models for each new player
#this model is a simple feedforward neural network with two hidden layers and an output layer with a sigmoid activation function. 
# The model takes in a 3D input tensor of shape (14,8,8), flattens it to a 1D array, and produces a scalar output. 
# The model is trained to minimize the mean squared error loss between its predictions and the true labels, using the Adam optimizer.
    
def profile(request):
    if LoggedInUser == "":
        return render(request, 'mainpage.html')
    else:
        return render(request, 'profile.html', {'Username' : LoggedInUser.getUsername(), 'Firstname': LoggedInUser.getFirstname(), 'Lastname':LoggedInUser.getLastname(),'Email': LoggedInUser.getEmail()})


def updateDetails(request):
    FirstName = request.POST['FirstName']
    LastName = request.POST['LastName']
    Email = request.POST['Email']
    Password = request.POST['Password']
    PasswordRepeat = request.POST['PasswordRepeat']
    

    FirsName = FirstName.strip()
    LastName = LastName.strip()
    Email = Email.strip()
    Password = Password.strip()
    PasswordRepeat = PasswordRepeat.strip()


    if ((not Password) or (not FirsName) or (not LastName) or (not Email)):     
        messages.error(request, f'Empty field/s submitted!')
        return redirect('profile.html')
    if (not("@" in Email)):     
        messages.error(request, f'Email address is not valid!')
        return redirect('profile.html')
    if (not(Password == PasswordRepeat)):
        messages.error(request, f'Passwords do not match!')
        return redirect('profile.html')
    else :
        Password = hashPassword(LoggedInUser.getUsername(), Password)
        LoggedInUser.updateDetails(Password,FirstName, LastName, Email)
        messages.success(request,f'Details updated successfully for user :{LoggedInUser.getUsername()}' )
        return redirect('mainpage.html')



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



    if ((not Username) or (not Password) or (not FirsName) or (not LastName) or (not Email) or (not Password) or (not PasswordRepeat)):
        messages.error(request, f'Empty field/s submitted!')
        return redirect('register.html')
    if (not("@" in Email)):
        messages.error(request, f'Email address is not valid!')
        return redirect('register.html')
    if (not(Password == PasswordRepeat)):
        messages.error(request, f'Passwords do not match!')
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
    
    

def send_email(emailReceiver,firstName,lastName, username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    email_sender = "theidealchessopponent@gmail.com" #Email created for sending temporary passwords
    file = open('templates\EmailPass.txt','r') #Reading email token from file
    email_password = file.readline()
    email_receiver = emailReceiver
    first_name = firstName
    last_name = lastName
    chess_stuff = ['chess', 'knight', 'king', 'rook', 'queen', 'bishop', 'pawn']
    combined = first_name[0:1] + random.choice(chess_stuff) + random.choice(chess_stuff)[0:2] #Generating a random combination
    tempPassword = "".join(random.sample(combined,len(combined))) #Scrambling the combination so it cannot be replicated

    subject = "Temporary Password Request"
    body = f"""
    Hi {first_name} {last_name}, we have recieved a request to reset your password to a temporary one,
    your temporary password is:

                                    {tempPassword}
    """
    try:
        email  = EmailMessage()
        email['From'] = email_sender
        email['To'] = email_receiver
        email['Subject'] = subject
        email.set_content(body) 

        context = ssl.create_default_context()#Verifying remote server certificates with the create_default_context() method
        # SMTP: A class representing an SMTP client session, 
        # which can be used to connect to an SMTP server, send email messages, and close the connection.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            #SMTP_SSL: A subclass of SMTP that provides a secure (SSL/TLS) connection to the SMTP server.
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,email.as_string())
        Password = hashPassword(username,tempPassword)
        with conn:
            c.execute("""UPDATE UserInfo SET Password = (:Password) WHERE Username = (:Username)""", 
            {'Username': username,'Password': Password})
    except:
        pass





