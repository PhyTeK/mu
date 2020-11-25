from django.db import models
#from countdowntimer_model.models import CountdownTimer

#class Time(models.Model,CountdownTimer):
#    pass
#    duration_in_minutes = models.CharField(max_length = 200,null=True)
#    state = models.IntegerField(blank=True,primary_key=True);

class Multi(models.Model):
    #timer = Time.objects.create(
    #duration_in_minutes=5,

    #state=Time.STATE.RUNNING,
    #)
    
    #remtid = timer.remaining_time_in_minutes()
    #print(remtid)
    
    test_120 = [
        [6,6],[8,4],[6,3],[2,2],[5,9],[7,5],
        [3,7],[9,9],[8,6],[6,7],[3,8],[9,4],
        [4,8],[6,4],[7,7],[9,3],[4,6],[6,8],
        [3,9],[8,8],[9,6],[4,7],[5,8],[8,3],
        [6,9],[7,3],[4,9],[3,6],[7,4],[10,10],
        [7,7],[8,6],[1,5],[8,8],[6,9],[0,7],
        [5,3],[9,9],[8,7],[7,3],[3,2],[4,8],
        [6,7],[8,7],[7,3],[3,2],[4,8],[9,7],
        [3,8],[4,7],[6,8],[3,6],[5,9],[4,6],
        [9,6],[3,0],[7,6],[8,4],[3,7],[5,5],
        [6,0],[7,6],[1,1],[4,6],[8,7],[7,3],
        [9,9],[8,6],[6,3],[6,9],[8,8],[9,6],
        [7,4],[3,8],[7,9],[6,5],[9,8],[6,6],
        [8,9],[6,7],[2,4],[9,4],[7,7],[4,8],
        [3,9],[7,8],[6,8],[9,7],[1,4],[9,2],
        [7,4],[9,6],[7,8],[9,9],[7,6],[8,3],
        [6,6],[4,9],[8,8],[4,7],[9,3],[7,7],
        [7,9],[4,6],[8,4],[9,7],[8,6],[7,3],
        [6,4],[9,8],[6,7],[8,9],[3,7],[6,9],
        [6,8],[2,0],[8,7],[6,3],[7,2],[10,1]]

    i = 0
    for m in test_120:
        i = i + 1
        label = '{}: {}x{}'.format(i,m[0],m[1])
        locals()[label] = models.CharField(blank=True, null=True,max_length=4,default='')
         
        del locals()['label']

    class Meta:

        def __str__(self):
            return self.test_120

    

class Stud(models.Model):
    id = models.IntegerField(blank=True,primary_key=True)
    name = models.CharField(max_length = 80)    # name of student
    fname = models.CharField(max_length = 80)   # Familly name
    klass = models.CharField(max_length = 8)    # Classe of the student
    
    
    class Meta:
        ordering = ['name']
        def __str__(self):
            return self.name

        

class Test(models.Model):
    id = models.IntegerField(blank=True,primary_key=True);
    studid = models.ForeignKey(Stud,verbose_name='id',on_delete=models.SET_DEFAULT)
    week = models.PositiveSmallIntegerField()  # Week of the test
    date = models.DateField(null=True)         # Date of the test
    start = models.DateField(null=True)        # Start of the test
    tid =  models.FloatField(null=True)        # Time in minutes
    correct = models.IntegerField(null=False)  # Correct answers
    errors = models.IntegerField(null=False)   # Wrong answers
    
    class Meta:
        ordering = ['week']
        def __str__(self):
            return self.week
