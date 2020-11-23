import sys,time,datetime
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Student,Multi
from .forms import MuForm,ResForm,StudForm,StartForm,TeachForm
from django.conf import settings
from .encrypt import encrypt,decrypt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def LoginRequiredView(LoginRequiredMixin):
    
    return HttpResponseRedirect('/admin/login/?next=/admin/')

def findstudid(name,klass):
    print(klass.lower())
    
    stud1 = Student.objects.filter(name=name,klass=klass.upper())
    stud2 = Student.objects.filter(name=name,klass=klass.lower())

    
    #print('Number of students:', stud1.count())
    #print('Number of students:', stud2.count())

    if(stud1.count() == 1):
        stud=stud1
    else:
        stud=stud2

    if(stud.count() > 0):
        studid = stud[0].studid

        print('Name: {}, Studid: {}\n'.format(name,studid))
        return studid
    else:
        return None

@login_required
def TeachView(request):
    studs = Student.objects.all()
    teachform = TeachForm(request.POST)
    if (request.method == 'POST'):
        if (teachform.is_valid()):
            context={
            'studs':studs
            }
            
            return HttpResponseRedirect('/mu/teacher/',context)
        else:
            return HttpResponse('Form unvalid!')

    elif (request.method == 'GET'):
        form = TeachForm()
        context = {
            'form':form,
            'studs':studs
        }
        return render(request, 'teacher.html',context)

    


def StartView(request):

    if (request.method == 'POST'):
        startform = StartForm(request.POST)
        if (startform.is_valid()):
            name = startform.cleaned_data['name']
            password = startform.cleaned_data['password']

            #user = User.objects.get(username=name)
            spass = authenticate(username=name,password=password)

            if spass is None:
                #return ender(request, 'StartForm.html')
                # New stuff
                return HttpResponse('Username/password unvalid')
            else:
                context={
                    'name':name,
                    'password':password
                }

                return HttpResponseRedirect('/mu/student/',context)

        else:
            return HttpResponse('Form unvalid {}'.format(startform))

    elif (request.method == 'GET'):
        form = StartForm()
        context = {
            'form':form,
        }
        return render(request, 'login.html',context)



    
def StudIn(request):
    # New stuff
    fields = Student.objects.all()
    
    if (request.method == 'POST'):
        studform = StudForm(request.POST)
        if (studform.is_valid()):
            name = studform.cleaned_data['name']
            klass = studform.cleaned_data['klass']
            #password = studform.cleaned_data['password']
            studid = findstudid(name,klass)
            
            #print('spass:',spass)
            #studform.save()
            # Find the name in db and return the corresponing studid

            if(studid is None):
                return HttpResponse('Felt namn eller fel klass. Prova igen!')
                #studform.save()

                return render(request, 'StudForm.html')
            else:
                context={
                    'studid':studid,
                    'name':name
                }


                response = HttpResponseRedirect('/mu/test/',context)
                response.set_cookie('studid',studid)

                return response
        else:
            return HttpResponse('Form unvalid {}'.format(studform))

            
    elif (request.method == 'GET'):
        form = StudForm()
        context = {
            'form':form,
        }
        return render(request, 'StudForm.html',context)

def MuTest(request):

    fields = Multi.objects.all()
    studid = request.COOKIES['studid']
    stud = Student.objects.filter(pk=studid)

    name = stud[0].name
    klass = stud[0].klass
    week = stud[0].week
    
    print('Name: {}, Klass: {}, studid: {}\n'.format(name,klass,studid))
    if request.method == 'POST':
        muform = MuForm(request.POST)
        #print('muform:',muform)
        if muform.is_valid():
            muform.save()
            muform = MuForm() # Clear form to avoid student corrections
            return HttpResponseRedirect('/mu/results/',{'form':muform,'stud':stud,'studid':studid})
        else:
            return HttpResponse('Form unvalid {}'.format(muform))
         
    else:
        form = MuForm()

        # Start timer
        time.tzset()
        tm = time.localtime()

        timeT = time.strftime('%H:%M:%S',tm)
        dateT = time.strftime('20%y-%m-%d',tm)
        a = datetime.datetime.now().replace(microsecond=0)
        print(a)
        # Update start time of the student

        stud.update(start=a,week=week)
                               
        context ={
            'form':form,
            'stud':stud,
            'name': name,
            'klass':klass,
            'studid':studid
        }
        return render(request, 'MuForm.html', context)

def StudView(request):
    mus = Student.objects.all()

    html = ''
    for mu in mus:
        var = f'<li> Name: {mu.name}, Date: {mu.date}, Time: {mu.time}</li><br>'
        html = html + var
    return HttpResponse(html,status = 200)


def ResView(request):

    res = Multi.objects.all()
    studid = request.COOKIES['studid']
    stud = Student.objects.filter(pk=studid)
    # End timer
    b = datetime.datetime.now().replace(microsecond=0)
    
    tm = time.localtime()
    timeT = time.strftime('%H:%M:%S',tm)
    
    # Update end time of the student

    stud.update(end=timeT)
        
    name  = stud[0].name
    klass = stud[0].klass

    print('{}:{},{}\n'.format(studid,name,klass))
    
    # Correct student multiplications
    
       
    html = ''

    cor = 0
    fel = 0
    allafel = ''
    lastid= res.count()
    lastval = Multi.objects.filter(id=lastid)
    #print('lastval', lastval.values('1: 6x6')[0]['1: 6x6'])
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
                allafel += '{}x{}≠{}'.format(mu[0],mu[1],studres) + '</br>'

    #var = '<li> {} -> {} {}</li><br>'.format(m,mu[0],mu[1])
    var = '<p>Du hade, {} korrekta svar och {} fel.</p>'.format(cor,fel)
    html = html + var

    html = html +'</br>' + allafel

    
    # Update student results
    oldres = stud[0].result
    if (oldres != None):
        newresult = oldres + ',({},{})'.format(cor,fel)
    else:
        newresult = '({},{})'.format(cor,fel)

    stud.update(result=newresult)
    time.tzset()
    tm = time.localtime()
    timeT = time.strftime('%H:%M:%S',tm)
    dateT = time.strftime('20%y-%m-%d',tm)
    b = datetime.datetime.now().replace(microsecond=0)

    # Week number
    a = datetime.datetime.strptime(stud[0].start, '%Y-%m-%d %H:%M:%S')
    print(a)
    print(b-a)
    oldate = stud[0].week
    print(oldate)
    if(oldate != None):
        newdate = oldate + ',{}'.format(b.isocalendar()[1])
    else:
        newdate = '{}'.format(b.isocalendar()[1])
        
    stud.update(week=newdate)
    stud.update(end=b-a)

    return HttpResponse(html,status = 200)


#            for label in labels:
#                locals()[label] = form.cleaned_data[locals()[label]]                

#  try:
#      name = MuModel.objects.get( stud_name = 'Philippe')
#  except:
#      raise Http404('No results %s %d' % (stud_name,locals()[1]))

# return HttpResponseRedirect(f'/results/', {'mu':mu})
