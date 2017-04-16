# DB connection
import pymysql
# To get the device's IP address
import socket
# Password encryption
from passlib.hash import pbkdf2_sha256

import time


class SnapDB:
    # Get conection with database -> connection
    def getConnection(self):
        # Database Variables
        db_host = 'localhost'
        db_port = 3306
        db_user = 'root'
        db_password = ''
        db_charset = 'utf8'
        db_database = 'snapchat'

        conn = pymysql.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset=db_charset)
        return conn


    # Gets the device's IP Address --> ipAddress
    def getIPadress(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('192.0.0.8', 1027))
        ipAddress = s.getsockname()[0]
        return ipAddress


    # Adds a new user to the database
    def addUser(self, nickName, name, password):
        # Getting connection
        conn = self.getConnection()
        cur = conn.cursor()

        # Password encrypted
        password = pbkdf2_sha256.hash(password)

        # INSERT command
        cur.execute("INSERT INTO user(userNickname, userName, userPassword, userIPAddress) VALUES('"+nickName+"', '"+name+"', '"+password+"', '"+self.getIPadress()+"');")

        # Changes are saved through 'commit()'
        conn.commit()

        # Closing cursor and connection
        cur.close()
        conn.close()


    # Checks if the userNickname and Password are correct --> userID/void
    def checkLogin(self, nickname, password):
        conn = self.getConnection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM user;")

        session = False
        name = ""
        userID = 0

        for element in cur:
            # Verifies the given password and the encrypted one
            check = pbkdf2_sha256.verify(password, element[3])

            if check == True and element[1] == nickname:
                session = True
                name = element[2]
                userID = element[0]
                break
        cur.close()
        conn.close()

        if session == True:
            print("Sesión iniciada con éxito,", name)
            self.updateIP(userID)
            return userID
        else:
            print("Error en los campos")


    # Updates the user's IP Address in the DB
    def updateIP(self, userID):
        conn = self.getConnection()
        cur = conn.cursor()

        cur.execute("UPDATE user SET userIPAddress = '"+self.getIPadress()+"' WHERE userID = "+str(userID)+"")
        conn.commit()
        cur.close()
        conn.close()


class Snap:
    def __init__(self, _snapID, snapDate, snapChannel):
        self._snapID = _snapID
        self.snapDate = snapDate
        self.snapChannel = snapChannel



class Channel:
    def __init__(self, _channelID, userID, friendID):
        self._channelID = _channelID
        self.userID = userID
        self.friendID = friendID



class User(SnapDB, Snap):
    def __init__(self, userID):
        conn = self.getConnection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM user WHERE userID = "+str(userID)+";")
        cur.close()
        conn.close()

        for element in cur:
            self.userID = element[0]
            self.userNickname = element[1]
            self.userName = element[2]
            self.userPassword = element[3]
            self.userIPAddress = element[4]


    # Adds a new friend (friendID) to the user's friend list in the DB
    def addFriend(self, friendID):
        conn = self.getConnection()
        cur = conn.cursor()

        if str(self.userID) == str(friendID):
            print("No te puedes agregar a tí mismo")
        else:
            cur.execute("SELECT COUNT(*) FROM channel WHERE userID = "+str(self.userID)+" AND friendID = "+friendID+";")
            num = 0
            for element in cur:
                num = element[0]

            if num == 1:
                print("Ya existe")
            else:
                cur.execute("INSERT into channel(userID, friendID) VALUES('"+str(self.userID)+"', '"+str(friendID)+"')")
                conn.commit()

        cur.close()
        conn.close()


    # Deletes the relation that connects userID - friendID from the DB
    def deleteFriend(self, friendID):
        conn = self.getConnection()
        cur = conn.cursor()

        cur.execute("DELETE FROM channel WHERE userID = "+str(self.userID)+" AND friendID = "+str(friendID)+";")
        conn.commit()
        cur.close()
        conn.close()





