import sys,time,datetime
from django.conf import settings
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth import authenticate
from .encrypt import encrypt,decrypt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Stud,Multi
from .forms import MuForm,ResForm,StudForm,StartForm,TeachForm

t1 = time.time()

def LoginRequiredView(LoginRequiredMixin):
    
    return HttpResponseRedirect('/admin/login/?next=/admin/')

def findstudid(name,klass):
    stud1 = Stud.objects.filter(name=name,klass=klass.upper())
    stud2 = Stud.objects.filter(name=name,klass=klass.lower())

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
    studs = Stud.objects.all()
    tests = Test.objects.all()
    teachform = TeachForm(request.POST)
    if (request.method == 'POST'):
        if (teachform.is_valid()):
            context={
                'studs':studs,
                'tests':tests
            }
            
            return HttpResponseRedirect('/mu/teacher/',context)
        else:
            return HttpResponse('Form unvalid!')

    elif (request.method == 'GET'):
        form = TeachForm()
        context = {
            'form':form,
            'studs':studs,
            'tests':tests
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
    fields = Stud.objects.all()
    print('t1',t1)
    if (request.method == 'POST'):
        studform = StudForm(request.POST)
        if (studform.is_valid()):
            name = studform.cleaned_data['name']
            klass = studform.cleaned_data['klass']
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

                #start = datetime.datetime.now().strftime('%H:%M:%S')
                start = datetime.datetime.now().strftime("%H:%M:%S")
                response = HttpResponseRedirect('/mu/test/',context)
                response.set_cookie('studid',studid,max_age=600)
                response.set_cookie('start',start,max_age=600)
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
    
    #fields = Multi.objects.all()
    studid = request.COOKIES['studid']
    stud = Stud.objects.filter(studid=studid)
    name = stud[0].name
    klass = stud[0].klass

    date = datetime.datetime.now().strftime('20%y-%m-%d')
    start = request.COOKIES['start']
    start = datetime.datetime.strptime(start,"%H:%M:%S")
    
    week = int(datetime.datetime.now().isocalendar()[1])


    print('Name: {}, Klass: {}, studid: {}\n'.format(name,klass,studid))

    if request.method == 'POST':
        muform = MuForm(request.POST)

        if muform.is_valid():
            end = datetime.datetime.now().strftime("%H:%M;%S")
            #end = datetime.datetime.now()
            start = start.strftime("%H:%M;%S")
            print('start:',start)
            print('end: ',end)
            #seconds = (end-start).seconds
            #print(seconds)
            seconds = 72
            #end = end.strftime('%H:%M:%S')

            # t2 = time.time()
            # dt = t2 -t1
            # print('t1=',t1)
            # print('t2=',t2)
            minutes = int(seconds/60)
            seconds = int(seconds - minutes*60 )
            tid = "{}:{}".format(minutes,seconds)

            
            test = Multi(studid_id=studid,date=date,start=start,end=end,week=week,tid=tid)    
                        
            correct = 0
            errors = 0
            
            for i in range(120):
                mu = Multi.test_120[i]
                muid = "{}: {}x{}".format(i+1,mu[0],mu[1])
                studres = muform.cleaned_data[muid]

                if(studres != None): 
                    if (int(studres) == int(mu[0])*int(mu[1])):
                        correct += 1
                        setattr(test,muid,studres)
                    else:
                        errors += 1
                        setattr(test,muid,'!{}'.format(studres))
                else:
                    #errors +=1      # No answer = error
                    #setattr(test,muid,'?')
                    pass
                    
            test.__dict__.update(correct=correct,errors=errors)
            test.save()
            #muform.save()
            
            muform = MuForm() # Clear form to avoid student back corrections
            return HttpResponseRedirect('/mu/results/',{'form':muform,'stud':stud,'studid':studid})
        else:
            return HttpResponse('Form unvalid!')
         
    else:
        form = MuForm()

        # Start timer
        #time.tzset()
        #tm = time.localtime()

        #timeT = time.strftime('%H:%M:%S',tm)
        #dateT = time.strftime('20%y-%m-%d',tm)
        #a = datetime.datetime.now().replace(microsecond=0)

        # Update start time of the student
        #t1 = time.time()
        print('t1_view: ',t1)
        context ={
            'form':form,
            'stud':stud,
            'name': name,
            'klass':klass,
            'studid':studid,
            't1':t1
        }
        return render(request, 'MuForm.html', context)

def StudView(request):
    mus = Stud.objects.all()

    html = ''
    for mu in mus:
        var = f'<li> Name: {mu.name}, Date: {mu.date}, Time: {mu.time}</li><br>'
        html = html + var
    return HttpResponse(html,status = 200)


def ResView(request):

    muls = Multi.objects.all()
    studid = request.COOKIES['studid']
    # Get the ID of the student
    stud = Stud.objects.filter(pk=studid)
    
    # End timer
    b = datetime.datetime.now().replace(microsecond=0)
    
    tm = time.localtime()
    timeT = time.strftime('%H:%M:%S',tm)
    
    name  = stud[0].name
    klass = stud[0].klass

    print('{}:{},{}\n'.format(studid,name,klass))
    
    # Correct the students multiplications
       
    html = ''
    cor=0
    fel=99
    var = '<p>Du hade, {} korrekta svar och {} fel.</p>'.format(cor,fel)
    html = html + var

    html = html +'</br>'

    
    return HttpResponse(html,status = 200)


