import sys
import os.path
import sqlite3
import hotelWorker


def main(args):
    if os.path.isfile("cronhoteldb.db"):
        return

    # os.remove('cronhoteldb.db')
    dbcon = sqlite3.connect('cronhoteldb.db')
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute(
            "CREATE TABLE TaskTimes(TaskId INTEGER NOT NULL , DoEvery INTEGER NOT NULL, NumTimes INTEGER NOT NULL , PRIMARY KEY (TaskId))")
        cursor.execute(
            "CREATE TABLE Tasks(TaskId INTEGER NOT NULL REFERENCES TaskTimes(TaskId), TaskName TEXT NOT NULL, Parameter INTEGER)")
        cursor.execute("CREATE TABLE Rooms(RoomNumber INTEGER PRIMARY KEY NOT NULL)")
        cursor.execute(
            "CREATE TABLE Residents(RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber), FirstName TEXT NOT NULL, LastName TEXT NOT NULL)")

        inputfilename = args[1]
        with open(inputfilename) as inputfile:
            i = 0
            for line in inputfile:
                line = line.strip('\n')
                line = line.strip('\r')
                # print(line)
                lineParts = line.split(',')
                if lineParts[0] == 'room':
                    # print (lineParts[1])
                    cursor.execute("INSERT INTO Rooms VALUES(?)", (lineParts[1],))
                    if len(lineParts) == 4:
                        cursor.execute("INSERT INTO Residents VALUES(?,?,?)",
                                       (lineParts[1], lineParts[2], lineParts[3],))
                elif lineParts[0] == 'clean':
                    cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (i, lineParts[1], lineParts[2],))
                    cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (i, lineParts[0], 0,))
                    i += 1
                elif lineParts[0] == 'breakfast':
                    cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (i, lineParts[1], lineParts[3],))
                    cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (i, lineParts[0], lineParts[2],))
                    i += 1
                elif lineParts[0] == 'wakeup':
                    cursor.execute("INSERT INTO TaskTimes VALUES(?,?,?)", (i, lineParts[1], lineParts[3],))
                    cursor.execute("INSERT INTO Tasks VALUES(?,?,?)", (i, lineParts[0], lineParts[2],))
                    i += 1

    dbcon.commit()
    dbcon.close()

if __name__ == '__main__':
    main(sys.argv)
