from django.db import models

class Dept(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f'{self.name}'

class Staff(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, related_name='StaffDept')
    name = models.CharField(max_length=30)
    exNum = models.SmallIntegerField(null=True)                              # 내선번호
    email = models.EmailField(unique=True, null=True)
    stat = models.CharField(max_length=20, null=True)   # 현황(재직, 퇴사 etc)

    def __str__(self):
        return f'{self.name}'


class Keyword(models.Model):
    word = models.CharField(max_length=100)
    dept = models.ForeignKey(Dept, on_delete=models.SET_NULL, null=True, blank=True, related_name='kwdDept')

#pk,부서,작성자,제목,작성시일,상태
class Portal(models.Model):
    title = models.TextField()
    text = models.TextField(max_length=10000, null=True, blank=True)
    files = models.FileField(null=True, blank=True)
    dept = models.ForeignKey(Dept, null=True, on_delete=models.SET_NULL, related_name='postDept')
    writer = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL, related_name='writer')
    date = models.DateTimeField()                   # 게시일
    inqDate = models.DateTimeField(auto_now=True)   # 조회일시

    def __str__(self):
        return f'[{self.dept}]{self.title}'
    
# Create your models here.
