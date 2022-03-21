import requests
import random
from isodate import parse_duration
import wikipedia
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from datetime import datetime
from calc.models import Contact
# Create your views here.
def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def wiki(request):
     if request.method =="POST":
        search=request.POST['search']
        try:
            result= wikipedia.page(search)
        except wikipedia.DisambiguationError as e:
            s = random.choice(e.options)
            result = wikipedia.page(s)  
        context={
                'title':result.title,
                'link':result.url,
                'summary':result.summary
            }
        return render(request,'wikipedia.html',context)
     else:
        return render(request,'wikipedia.html')

def youtube(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']
      
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails,statistics',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'viewsk': int(result['statistics']['viewCount'])//1000
            }
            if video_data['viewsk']>=1000:
                float1=video_data['viewsk']/1000
                format_float = "{:.2f}".format(float1)
                video_data['views']=str(format_float)+'m'+' '
            else :
                video_data['views']=str( video_data['viewsk'])+'k'+' '
            videos.append(video_data)

    context = {
        'videos' : videos
    }
    return render(request,'you_tube.html',context)

def books(request):
    if request.method =="POST":
        search=request.POST['search']
        url="https://www.googleapis.com/books/v1/volumes?q="+search
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo'].get('title'),
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                'authors': answer['items'][i]['volumeInfo'].get('authors')
     
            }
            result_list.append(result_dict)
            context={
                'results':result_list
            }
        
        return render(request,'books.html',context)
    else:
       return render(request,'books.html')
         
def contact(request):
    if request.method=='POST':
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        email=request.POST.get('email')
        comment=request.POST.get('comment')
        contact=Contact(first_name=first_name,last_name=last_name,email=email,comment=comment,date=datetime.today())
        contact.save()
        messages.success(request, "Your message has been sent")
    return render(request,'contact.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
    
def login(request):
    if request.method=='POST':
         username=request.POST['username']
         password=request.POST['password']
         user=auth.authenticate(username=username,password=password)
         if user is not None:
             auth.login(request,user)
             return redirect('/')
         else:
             messages.error(request, "Error: Invalid credentials")
             return redirect('login')
    else :
         return render(request,'login.html')
# Create your views here.
def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if password==password1:
            if User.objects.filter(username=username).exists():
               messages.info(request,'Info : Username taken')
               return redirect('register')
            elif User.objects.filter(email=email).exists():
               messages.info(request,'Info: email taken')
               return redirect('register')
            else:
               user=User.objects.create_user(username=username,password=password,first_name=first_name, last_name= last_name,email=email)
               user.save();
               messages.success(request, "Success: User created")
               return redirect('login')
        else:
            messages.warning(request, "Warning: Password not matching")
            return redirect('register')
        return redirect('/')

    else:
        return render(request,'register.html')


