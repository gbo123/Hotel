import os
import sqlite3

import sys

import hotelManagement
import time





if (os.path.isfile('cronhoteldb.db')):
        dbcon = sqlite3.connect('cronhoteldb.db')
        with dbcon:
                cursor = dbcon.cursor()

def dohoteltask(taskname,parameter):
                if taskname=='wakeup':
                        cursor.execute("SELECT FirstName FROM Residents WHERE RoomNumber=(?)", (parameter,))
                        firstname=cursor.fetchone()
                        cursor.execute("SELECT LastName FROM Residents WHERE RoomNumber=(?)", (parameter,))
                        lastname= cursor.fetchone()
                        timeforprint=time.time()
                        textForprint="%s %s in room %d recieved a wakeup call at %d" %(firstname[0],lastname[0],parameter,timeforprint)
                        print textForprint
                        return time.time()
                elif taskname=='breakfast':
                        cursor.execute("SELECT FirstName FROM Residents WHERE RoomNumber=(?)", (parameter,))
                        firstname = cursor.fetchone()
                        cursor.execute("SELECT LastName FROM Residents WHERE RoomNumber=(?)", (parameter,))
                        lastname = cursor.fetchone()
                        timeforprint = time.time()
                        textForprint = "%s %s in room %d has been served breakfast at %d" % (
                        firstname[0], lastname[0], parameter, timeforprint)
                        print textForprint
                        return time.time()

                elif taskname=='clean':
                        cursor.execute("SELECT RoomNumber FROM Rooms EXCEPT SELECT RoomNumber From Residents")
                        textForprint= cursor.fetchall()
                        numtext=len(textForprint)
                        print "Rooms",
                        for i in xrange(0, numtext):
                                print textForprint[i][0],
                                if i+1<numtext:
                                        sys.stdout.write(', '),
                        print "were cleaned at",
                        print time.time()
                        return time.time()















