import os
import sqlite3
import sys






def main(args):
    dbcon = sqlite3.connect('cronhoteldb.db')
    with dbcon:
	cursor = dbcon.cursor()
        cursor.execute(
            "CREATE TABLE TaskTimes(TaskId INTEGER PRIMARY KEY NOT NULL,DoEvery INTEGER NOT NULL,NumTimes INTEGER NOT NULL )")
        cursor.execute(
            "CREATE TABLE Tasks(TaskId INTEGER NOT NULL REFERENCES TasksTimes(TaskId),TaskName TEXT NOT NULL,Parameter INTEGER)")
        cursor.execute("CREATE TABLE Rooms(RoomNumber INTEGER PRIMARY KEY NOT NULL)")
        cursor.execute(
            "CREATE TABLE Residents(RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber),FirstName TEXT NOT NULL,LastName TEXT NOT NULL)")

        id=0
        inputfilename = args[1]
        with open(inputfilename) as inputfile:
            for line in inputfile:
                line= line.strip('\n')
                hotel=line.split(',')
                if (hotel[0] == 'room') and (len(hotel) == 4):
                    cursor.execute("INSERT INTO Rooms VALUES(?)", (hotel[1],))
                    cursor.execute("INSERT INTO Residents VALUES(?,?,?)", (hotel[1], hotel[2], hotel[3]))

                elif (hotel[0] == 'room' and len(hotel) == 2):
                    cursor.execute("INSERT INTO Rooms VALUES(?)", (hotel[1],))

                elif (hotel[0] == 'clean'):
                    cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (id, hotel[1], hotel[2]))
                    cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (id, hotel[0], 0))
                    id=id+1
                else:
                    cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (id, hotel[1], hotel[3]))
                    cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (id, hotel[0], hotel[2]))
                    id=id+1





if __name__ == '__main__' and not os.path.isfile('cronhoteldb.db'):
    main(sys.argv)










