from django import forms,utils
import time,datetime
from .models import Stud,Multi,Results

class StartForm(forms.ModelForm):
    name = forms.CharField(required=True,initial='',label='')
    password = forms.CharField(required=True,initial='',label='',widget=forms.PasswordInput)

    class Meta:
        model = Stud
        fields = ['name','password']

        
    
class TeachForm(forms.ModelForm):

    WEEKS = [('47','47'),('48','48')]
    #name = forms.CharField(required=True,initial='hi',label='name')
    klasser = forms.ChoiceField(label='Klass',choices = Results.CLASSES,widget=forms.Select)
    weeks = forms.ChoiceField(label='Vecka',choices = WEEKS,widget=forms.Select)

    class Meta:
        model = Results
        fields = ['klasser']




class MuForm(forms.ModelForm):

    i=0;
    for f in Multi.test_120:
        i = i + 1
        fname = '{}: {}x{}'.format(i,f[0],f[1])                   
        #locals()[fname]= forms.IntegerField(label_suffix='=',required=False,widget=forms.TextInput)
        locals()[fname]= forms.CharField(label_suffix='=',required=False)
        locals()[fname].widget.attrs.update(size='5',max_length=3)

        del locals()[fname]

        
    class Meta:
        model = Multi
        fields = []
        i=0
        labels = {}
        widgets = {}
        for f in model.test_120:
            i = i+1
            fname = '{}: {}x{}'.format(i,f[0],f[1])                   
            fields.append(fname)
            labels[fname] = '{}x{}'.format(f[0],f[1])
            widgets[fname] = forms.TextInput(attrs={'style': 'width: 50px'})

            

        
class StudForm(forms.ModelForm):
    tid = time.localtime()
    #password = forms.CharField(label='Lösenord',max_length=32, widget=forms.PasswordInput)
    #print(password)
    name = forms.CharField(label='Ditt namn',initial='',required=True)
    klass = forms.CharField(label='Din klass    ',label_suffix=': ',max_length=4,required=True)
    #start = forms.CharField(disabled=True,required=False,label_suffix='', initial='{}:{}'.format(tid.tm_hour+1,tid.tm_min))
    #date = forms.DateField(initial=datetime.date.today,label_suffix='',disabled=True,required=False)

    #studid = forms.IntegerField(label_suffix='',required=False)
    #studid.widget.attrs.update(disabled=True,required=False)

    class Meta:
        model = Stud
        fields = ['name','klass']
    

        help_text = {
            'name' : 'Skriv ditt namn här!',
            'klass' : 'Skriv din klass här!',
         }

class ResForm(forms.ModelForm):
    tid = time.localtime()
    name = forms.CharField(label_suffix='',required=False)
    time = forms.CharField(disabled=True,required=False,label_suffix='', initial='{}:{}'.format(tid.tm_hour+1,tid.tm_min))
    #date = forms.DateField(initial=datetime.date.today,label_suffix='',disabled=True,required=False)

    # iterable 
    KLASS_CHOICES =( 
        ("1", "One"), 
        ("2", "Two"), 
        ("3", "Three"), 
        ("4", "Four"), 
        ("5", "Five"), 
    )

    klass_field = forms.ChoiceField(choices = KLASS_CHOICES)

    class Meta:
        model = Stud
        fields = ['name','klass']
    
        
  
