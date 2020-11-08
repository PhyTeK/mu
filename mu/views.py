import sys,time,datetime
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404
 
from .models import Student,Multi
from .forms import MuForm,ResForm

def MuTest(request):

    fields = Multi.objects.all()
    
    if request.method == 'POST':
        muform = MuForm(request.POST)
        #print('muform:',muform)
        if muform.is_valid():
            muform.save()
            
            return HttpResponseRedirect('/mu/results')
        else:
            return HttpResponse('Form unvalid {}'.format(muform))
         
    else:
        form = MuForm()
        context ={
            'form':form,
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
    Student.objects.create(name='Philippe',date=dateT,time='{},'.format(timeT),result='{},'.format(cor))

 
        
    return HttpResponse(html,status = 200)


#            for label in labels:
#                locals()[label] = form.cleaned_data[locals()[label]]                

#  try:
#      name = MuModel.objects.get( stud_name = 'Philippe')
#  except:
#      raise Http404('No results %s %d' % (stud_name,locals()[1]))

# return HttpResponseRedirect(f'/results/', {'mu':mu})
