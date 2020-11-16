import sys,time,datetime
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Student,Multi
from .forms import MuForm, ResForm,StudForm
from django.conf import settings
from .encrypt import encrypt,decrypt

def findstudid(name):
    stud = Student.objects.filter(name=name)
    print(stud.count())
    if(stud.count() > 0):
        studid = stud[0].studid

        print('Name: {}, Studid: {}\n'.format(name,studid))
        return studid
    else:
        return None


def StudIn(request):
    #u = User.objects.create_user('Philippe','','secret')
    #u.save()

    ec=encrypt('abc123')
    dc=decrypt(ec)
    print(ec,dc)
    fields = Student.objects.all()
    
    if (request.method == 'POST'):
        studform = StudForm(request.POST)
        if (studform.is_valid()):
            name = studform.cleaned_data['name']
            klass = studform.cleaned_data['klass']
            password = studform.cleaned_data['password']
            studid = findstudid(name)

            
            if(studid is None):  # Warning anyone can create a password!!
                user = User.objects.create_user(username=name,email=None,password=password)
                #user.set_password(password)
                user.save()
                studform.save()

            user = User.objects.get(username=name)
            spass = authenticate(username=name,password=password)
            print('spass:',spass)
            #studform.save()
            # Find the name in db and return the corresponing studid

            if(studid is None or spass is None):
                return HttpResponse("Name/password not valid!!\n")
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

    #var = '<li> {} -> {} {}</li><br>'.format(m,mu[0],mu[1])
    var = '<p>Du hade {} korrekta svar.</p>'.format(cor)
    html = html + var

    # Update student results
    oldres = stud[0].result
    if (oldres != None):
        newresult = oldres + ',{}'.format(cor)
    else:
        newresult = '{}'.format(cor)

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
    if(oldate != ''):
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
