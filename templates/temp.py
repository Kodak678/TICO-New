Username = "G"
Password = "h"
FirsName = "3"
LastName = "j"
Email = "@ "
Password = Password.strip()
Username = Username.strip()
FirsName = FirsName.strip()
LastName = LastName.strip()
Email = Email.strip()

import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

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

c.execute("SELECT * FROM Users")
print(c.fetchall())
conn.commit()
conn.close()


