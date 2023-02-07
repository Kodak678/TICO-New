from email.message import EmailMessage
import ssl
import smtplib
import random
import sqlite3


def send_email(emailReceiver,firstName,lastName):
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

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,email.as_string())
    except:
        pass

for i in range(0,10):
    send_email("xeroro1114@letpays.com","Gideon","Omotayo")



