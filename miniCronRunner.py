import os
import sqlite3
import hotelWorker
import time




def check():
    if (os.path.isfile('cronhoteldb.db')):
        dbcon = sqlite3.connect('cronhoteldb.db')
        with dbcon:
            cursor=dbcon.cursor()
            cursor.execute("SELECT TaskId,DoEvery FROM TaskTimes WHERE NumTimes>0")
            checkNum = cursor.fetchall()
            if len(checkNum) == 0:
                return False
            else:
                return True


def main():
    done =False
    while  (os.path.isfile('cronhoteldb.db') and done==False and check()):
        dbcon=sqlite3.connect('cronhoteldb.db')
        with dbcon:
            cursor = dbcon.cursor()
            cursor.execute("SELECT TaskId FROM TaskTimes")
            tasklist=cursor.fetchall()
            tasknum =len(tasklist)
            taskArray=[]
            for i in range(tasknum):
                taskArray.append(0)
            for i in xrange(0, len(taskArray)):
                cursor.execute("SELECT TaskName,Parameter FROM Tasks WHERE TaskId=(?)", (i,))
                mission= cursor.fetchone()
                timer= hotelWorker.dohoteltask(mission[0],mission[1])
                taskArray[i]=timer
                cursor.execute("UPDATE TaskTimes set NumTimes=NumTimes-1 WHERE TaskId=(?) ",(i,))
            while(done==False):
                cursor.execute("SELECT TaskId,DoEvery FROM TaskTimes WHERE NumTimes>0")
                taskToDo = cursor.fetchall()
                if len(taskToDo)==0:
                    done=True
                if done==False:
                    for hoteltask in taskToDo:
                        taskindex= hoteltask[0]
                        taskdoevery= hoteltask[1]
                        if time.time()>=taskArray[taskindex]+taskdoevery:
                            cursor.execute("SELECT TaskName,Parameter FROM Tasks WHERE TaskId=(?)", (taskindex,))
                            mission2 = cursor.fetchone()
                            timers = hotelWorker.dohoteltask(mission2[0], mission2[1])
                            taskArray[taskindex] = timers
                            cursor.execute("UPDATE TaskTimes set NumTimes=NumTimes-1 WHERE TaskId=(?) ", (taskindex,))





if __name__ == '__main__' :
    main()



































