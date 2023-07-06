from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from app1 import app
from django.shortcuts import render
from app1.app import get_reading


def landingPage(request):
        return render(request, 'landing.html')


from django.http import HttpResponse

def homePage(request):
    if request.method == 'POST':
        if 'start' in request.POST:
            # Récupérer les fichiers images à partir de la requête HTTP
            images = request.FILES.getlist('imageUpload')

            readings = []  # list to store meter readings from each image

            for index, img_file in enumerate(images):
                # Enregistrer l'image sur le disque
                filename = 'image{}.png'.format(index+1)
                with open(filename, 'wb') as f:
                    f.write(img_file.read())

                # Extraire les chiffres de l'image
                meter_reading = get_reading(filename)
                readings.append('Image {}: {}'.format(index+1, meter_reading))

            # Save the result to a text file without HTML tags
            with open('result.txt', 'w') as f:
                for reading in readings:
                    f.write(reading + '\n')

            # Renvoyer la réponse HTTP avec le résultat
            return render(request, 'result.html', {'readings': readings})

    return render(request, 'home.html')





def signupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("not the same password !")
        else:
        
        
        
             my_user=User.objects.create_user(uname,email,pass1)
             my_user.save()
             return redirect('login')
    
    return render(request,'signup.html')

def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("username or passeword is incorrect")
    return render(request,'login.html')


