import os
import sqlite3
import time
import hotelWorker

def main():
    dict = {}
    dbcon = sqlite3.connect('cronhoteldb.db')
    while 1:
        if not os.path.isfile("cronhoteldb.db"):  # if file does not exist
            break

        with dbcon:
            cursor = dbcon.cursor()
            cursor.execute(
                "SELECT * FROM TaskTimes JOIN Tasks ON TaskTimes.TaskId = Tasks.TaskId WHERE TaskTimes.NumTimes > 0")
            res = cursor.fetchall()
            if len(res) == 0:
                break
            for task in res:
                if not dict.has_key(task[0]):
                    dict[task[0]] = hotelWorker.dohoteltask(task[4], task[5])
                    cursor.execute("UPDATE TaskTimes SET NumTimes = (?) WHERE TaskId = (?)", (task[2] - 1, task[0],))
                    # print res
                elif dict[task[0]] + task[1] < time.time():
                    dict[task[0]] = hotelWorker.dohoteltask(task[4], task[5])
                    cursor.execute("UPDATE TaskTimes SET NumTimes = (?) WHERE TaskId = (?)", (task[2] - 1, task[0],))
                    # print res
        dbcon.commit()

    dbcon.close()

if __name__ == '__main__':
    main()