;; This buffer is for text that is not saved, and for Lisp evaluation.
;; To create a file, visit it with C-x C-f and enter text in its buffer.

<!--
{{form.as_table}}

<table border="1">
{% for element in data %}
    <tr>
    <td><p>column 1 </p></td>
    <td><p>column 2 </p></td>
    <td><p>column 3 </p></td>
    <td><p>column 4 </p></td>
    <td><p>column 5 </p></td>
    </tr>
{% endfor %}
</tr>
</table>

-->






	{% for field in form %}
        <tr>
            <td>{{ field.label}}{{ field }}</td>
            <td>{{ field.label}}{{ field }}</td>
        </tr>
	{% endfor %}
	


class Test(models.Model):
    id = models.ForeignKey(Multi,to_field='id',blank=True, default=0,on_delete=models.SET_DEFAULT)
    id = models.IntegerField(blank=True,primary_key=True);
    studid = models.ForeignKey(Stud,to_field='id',blank=True, default=0,on_delete=models.SET_DEFAULT)

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



 # record results for student in mu_test
    test[0].correct = cor
    test[0].errors = fel

    time.tzset()
    tm = time.localtime()
    timeT = time.strftime('%H:%M:%S',tm)
    dateT = time.strftime('20%y-%m-%d',tm)
    b = datetime.datetime.now().replace(microsecond=0)

    # Week number
    a = datetime.datetime.strptime(test[0].start, '%Y-%m-%d %H:%M:%S')
    print(b-a)
    #test[0].week = b.isocalendar()[1]
    test[0].tid = b-a



    cor = 0
    fel = 0

    for i in range(120):
        mu = Multi.test_120[i]
        muid = "{}: {}x{}".format(i+1,mu[0],mu[1])

        studres=lastval.values(muid)[0][muid] # Check that's the correct student
        

        if(studres != None):
            if (int(studres) == int(mu[0])*int(mu[1])):
                print("{}: {}x{}={}".format(studid,mu[0],mu[1],studres))
                cor += 1
            else:
                print("!!{}: {}x{}={}".format(studid,mu[0],mu[1],studres))
                fel += 1


    {% with 'Me' as sname %}
    {% for test in tests %}
    {% if test.studid.name == sname %}
    <p>{{ test.studid.name }}, {{ test.studid.klass }}, {{ test.correct }}, {{ test.errors }} </p>
    {% endif %}
    {% endfor %}
    {% endwith %}



    # Two forms
    
     <form method='POST'>
    {{form1.as_p}}
    <button type="submit" name="btnform1">Save Changes</button>
    </form>
    <form method='POST'>
    {{form2.as_p}}
    <button type="submit" name="btnform2">Save Changes</button>
    </form>


    if request.method=='POST' and 'btnform1' in request.POST:
    do something...
    if request.method=='POST' and 'btnform2' in request.POST:
    do something...
