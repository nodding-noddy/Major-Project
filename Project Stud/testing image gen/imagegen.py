import psycopg2
import qrcode

con = psycopg2.connect(user='monkeymon',
database ='college',
host = 'localhost',
password = 'con9988')

cursor = con.cursor()

cursor.execute("SELECT * FROM student_data")
students = cursor.fetchall()

for student in students:
    image = qrcode.make(student[0])
    name = student[0]
    image.save("D:\\test QR output\\%s.png"%name,"PNG")


cursor.close()
con.close()



