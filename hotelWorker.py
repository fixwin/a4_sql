import sqlite3
import time

def dohoteltask(taskname, parameter):
    dbcon = sqlite3.connect('cronhoteldb.db')
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM Tasks WHERE TaskName=(?) AND  Parameter=(?)", (taskname, parameter,))
        res = cursor.fetchone()
        if taskname == 'wakeup':
            cursor.execute("SELECT * FROM Residents WHERE RoomNumber=(?)", (res[2],))
            res = cursor.fetchone()
            print(str(res[1]) + " " + str(res[2]) + " in room " + str(res[0]) + " received a wakeup call at " + str(
                time.time()))
            return time.time()
        elif taskname == 'breakfast':
            cursor.execute("SELECT * FROM Residents WHERE RoomNumber=(?)", (res[2],))
            res = cursor.fetchone()
            print(str(res[1]) + " " + str(res[2]) + " in room " + str(res[0]) + " has been served breakfast at " + str(
                time.time()))
            return time.time()
        elif taskname == 'clean':
            cursor.execute("SELECT * FROM Rooms LEFT JOIN Residents ON Rooms.RoomNumber = Residents.RoomNumber ORDER BY Rooms.RoomNumber ASC")
            res = cursor.fetchall()
            # print res
            emptyRooms = ""
            for room in res:
                if room[1] == None:
                    emptyRooms += str(room[0]) + ", "
            emptyRooms = emptyRooms.strip(', ')
            print("Rooms " + emptyRooms + " were cleaned at " + str(time.time()))
            return time.time()

    dbcon.commit()
    dbcon.close()
