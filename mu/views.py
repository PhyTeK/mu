import sys,time,datetime
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404
 
from .models import Student,Multi
from .forms import MuForm, ResForm,StudForm


def findstudid(name):
    stud = Student.objects.filter(name=name)[0]

    if(stud != None):
        studid = stud.studid

        print('Name: {}, Studid: {}\n'.format(name,studid))
        return studid
    else:
        return None


def StudIn(request):
    fields = Student.objects.all()
    
    if (request.method == 'POST'):
        studform = StudForm(request.POST)
        if (studform.is_valid()):
            name = studform.cleaned_data['name']
            #studform.save()
            # Find the name in db and return the corresponing studid
            studid=findstudid(name)
            if studid == None:
                print("Name does not exist!!\n")
                return render(request, 'StudForm.html',context)
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
    stud = Student.objects.filter(pk=studid)[0]

    name = stud.name
    klass = stud.klass

    print('Name: {}, Klass: {}, studid: {}\n'.format(name,klass,studid))
    if request.method == 'POST':
        muform = MuForm(request.POST)
        #print('muform:',muform)
        if muform.is_valid():
            muform.save()
            
            return HttpResponseRedirect('/mu/results/',{'form':muform,'stud':stud,'studid':studid})
        else:
            return HttpResponse('Form unvalid {}'.format(muform))
         
    else:
        form = MuForm()
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
    print('res size:',sys.getsizeof(res))
    
    html = ''

    cor = 0
    lastid= res.count()
    lastval = Multi.objects.filter(id=lastid)
    #print('lastval', lastval.values('1: 6x6')[0]['1: 6x6'])
    for i in range(120):
        mu = Multi.test_120[i]
        muid = "{}: {}x{}".format(i+1,mu[0],mu[1])
        studres=lastval.values(muid)[0][muid]
        if(studres != None):
            if (int(studres) == int(mu[0])*int(mu[1])):
                print("{}x{}={}".format(mu[0],mu[1],studres))
                cor += 1

    #var = '<li> {} -> {} {}</li><br>'.format(m,mu[0],mu[1])
    var = '<p>correct answers={}</p>'.format(cor)
    html = html + var

    # Added the result to the specific student.
    tm = time.localtime()
    timeT = time.strftime('%H:%M:%S',tm)
    dateT = time.strftime('20%y-%m-%d',tm)
    Student.objects.create(name='Philippe',date=dateT,start='{},'.format(timeT),result='{},'.format(cor))

 
        
    return HttpResponse(html,status = 200)


#            for label in labels:
#                locals()[label] = form.cleaned_data[locals()[label]]                

#  try:
#      name = MuModel.objects.get( stud_name = 'Philippe')
#  except:
#      raise Http404('No results %s %d' % (stud_name,locals()[1]))

# return HttpResponseRedirect(f'/results/', {'mu':mu})
