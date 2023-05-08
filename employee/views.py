from tabnanny import check
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from employee.forms import AddForm, SearchForm
from employee.models import Employee, Checkin, GENDER_CHOICES, EDUCATION_LEVEL
import datetime
import os
import cv2 # opencv
from keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# load the facenet model
facenet_model = load_model('facenet_keras.h5')
facenet_model._make_predict_function()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

IMG_SIZE = 160

def get_embedding(model, face):
    # scale pixel values
    face = face.astype('float32')
    # standardization
    mean, std = face.mean(), face.std()
    face = (face-mean)/std
    # transfer face into one sample (3 dimension to 4 dimension)
    sample = np.expand_dims(face, axis=0)
    # make prediction to get embedding
    
    yhat = model.predict(sample)
    return yhat[0]

def extract_face_ver2(filename, face_cascade):
    print(filename)
    filename = os.path.join(filename)
    print(filename)
    img = cv2.imread(filename)
    img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    faces_array = []
    for (x,y,w,h) in faces:
        crop = img_array[y:y+h, x:x+w]
        crop = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
        crop = crop.astype('float32')
        # standardization
        mean, std = crop.mean(), crop.std()
        crop = (crop-mean)/std
        # transfer face into one sample
        sample = np.expand_dims(crop, axis=0)
        faces_array.append(sample)
    return faces_array

def get_embedding_bydir(filename, facenet_model, face_cascade):
    # load the photo and extract the face
    face = extract_face_ver2(filename=filename,face_cascade = face_cascade)[0][0]
    emd = get_embedding(facenet_model, face)
    return emd

def sklearn_cosine(x,y):
    return cosine_similarity(x, y)

# print(get_embedding_bydir('/home/baocongidol/WorkSpace/ttcs/media/elton_john.jpg',facenet_model, face_cascade ).shape)


class EmployeeView(View):
    template_name = 'employee/index.html'
    name = 'employee'

    def get(self, request):
        add_form = AddForm()
        search_form = SearchForm()

        employees = Employee.objects.all().values()
        for i in range(len(employees)):
            edulevle = employees[i]['educationLevel']
            employees[i]['educationLevel'] = EDUCATION_LEVEL[edulevle][1]

            gender = employees[i]['gender']
            employees[i]['gender'] = GENDER_CHOICES[gender][1]

        context = {
            'name': self.name,
            'employees': employees,
            'add_form': add_form,
            'search_form': search_form,
        }
        return render(request,self.template_name, context=context)

    def post(self, request):
        add_form = AddForm(request.POST,request.FILES)
        search_form = SearchForm(request.POST, request.FILES)
        func_name = 'infor'
    

        if add_form.is_valid():
            employee = add_form.save()
            try:
                embedding = get_embedding_bydir(employee.avatar.path, facenet_model=facenet_model, face_cascade=face_cascade)
                employee.embedding = embedding
                employee.save()
            except:
                employee.delete()
                return render(request,"error.html")

            func_name = 'add'
        
        if search_form.is_valid():
            
            query = search_form.save()
            try:
                query_embd = get_embedding_bydir(query.avatar.path, facenet_model=facenet_model, face_cascade=face_cascade)
                query.embedding = query_embd
                query.save()
            except:
                query.delete()
                return render(request,"error.html")

            
            points ={}
            ebd_q = np.frombuffer(query.embedding, dtype=np.float32)
            for employee in Employee.objects.all():
                key = employee.id
                ebd_e = np.frombuffer(employee.embedding, dtype=np.float32)
                val = sklearn_cosine(ebd_q.reshape(1,-1),ebd_e.reshape(1,-1))
                points[key]= val[0][0]
            
            e_id = max(points, key= lambda x: points[x])
            if (e_id >0.8):
                employee = Employee.objects.get(pk = e_id)
                Checkin.objects.create(employee= employee)
            
            func_name = 'search'   
        
        employees = Employee.objects.all().values()
        for i in range(len(employees)):
            edulevle = employees[i]['educationLevel']
            employees[i]['educationLevel'] = EDUCATION_LEVEL[edulevle][1]

            gender = employees[i]['gender']
            employees[i]['gender'] = GENDER_CHOICES[gender][1]

        context = {
            'name': self.name,
            'employees': employees,
            'add_form': add_form,
            'search_form': search_form,
            'func_name': func_name,
        }
        return render(request,self.template_name, context=context)
    
    def delete(self, request):
        Employee.objects.get(pk=request.GET['employeeId']).delete()
        return HttpResponse(status=200)


class HomeView(View):
    template_name = 'home/index.html'
    name = 'home'
    def get (self, request):
        employees = Employee.objects.all().values()
        for i in range(len(employees)):
            edulevle = employees[i]['educationLevel']
            employees[i]['educationLevel'] = EDUCATION_LEVEL[edulevle][1]

            gender = employees[i]['gender']
            employees[i]['gender'] = GENDER_CHOICES[gender][1]

            daycheck = datetime.date.today()
            checkin = Checkin.objects.filter(employee = employees[i]['id'],date = daycheck)
            employees[i]['status'] = 'active'
            if (len(checkin) == 0):
                employees[i]['status'] = 'deactive'



        context = {
            'name': self.name,
            'employees': employees
            }
        return render(request,self.template_name, context=context)

class SalaryView(View):
    template_name = 'salary/salary.html'
    name = 'salary'
    

    def get (self, request):
        employees = Employee.objects.all().values()

        for i in range(len(employees)):
            checkin = Checkin.objects.filter(employee = employees[i]["id"])


            employees[i]['workday'] = len(checkin)
            employees[i]['salary'] = len(checkin)* 50000
            edulevle = employees[i]['educationLevel']
            employees[i]['educationLevel'] = EDUCATION_LEVEL[edulevle][1]

        context = {
            'name': self.name,
            'employees': employees
            }
        return render(request,self.template_name, context=context)

class LoginView(View):
    template_name = 'auth/login.html'
    name = 'login'
    def get (self, request):
        
        context={
            'name': self.name
        }

        return render(request, self.template_name, context=context)


