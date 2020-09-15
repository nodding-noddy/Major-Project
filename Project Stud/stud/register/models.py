from django.db import models

# Create your models here.

class Branch(models.Model):
    branch_name = models.CharField(max_length = 25)
    branch_code = models.CharField(max_length = 2,primary_key='True',default = 'UD')

    class Meta:
        db_table = 'branch_data'
    
    def __str__(self):
        return f"{self.branch_name} ({self.branch_code})"

class Roll_manager(models.Manager):
    def retrieve(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""SELECT roll_no FROM student_data""")
            result = cursor.fetchall()
            return result


class Student_data(models.Model):
    roll_no = models.CharField(max_length = 12,primary_key=True,default = '020')
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.CharField(max_length = 50)
    b_code = models.ForeignKey(Branch,on_delete=models.CASCADE,related_name = 'students')
    attendance = models.IntegerField(default=0)
    roll_man = Roll_manager()
    objects = models.Manager()
    
    class Meta:
        db_table = 'student_data'

    def __str__(self):
        return f"Name = {self.first_name} {self.last_name} Roll no. = {self.roll_no} Branch = {self.b_code}"


class Admin(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.CharField(max_length = 30,primary_key=True)
    password = models.CharField(max_length = 20)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,default = 'UD')

    class Meta:
        db_table = 'admin_data'
    
    def __str__(self):
        return f"Email = {self.email} Name = {self.first_name} {self.last_name} Password = {self.password}"