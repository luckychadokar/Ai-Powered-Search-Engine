from langdetect import detect
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import RecentSearch, GenerationHistory
import os
import base64
import requests
from openai import OpenAI

# OpenRouter Client Setup
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

@login_required(login_url='/signin/')
def bot_search(request):
    query = request.GET.get('query')
    ans = "FOUND NOTHING"
    recent_searches = []

    if query:
        try:
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query}
                ]
            )
            ans = response.choices[0].message.content.strip()
            RecentSearch.objects.create(user=request.user, query=query)
        except Exception as e:
            ans = f"Error: {str(e)}"

    recent_searches = RecentSearch.objects.filter(user=request.user).order_by('-timestamp')[:25]
    return render(request, 'user.html', {'ans': ans, 'query': query, 'recent_searches': recent_searches})

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def signuppage(request):
    if request.method == "POST":
        Name = request.POST.get('name')
        unm = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('password')

        if not (Name and unm and email and pwd):
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')

        if User.objects.filter(username=unm).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=unm, email=email, password=pwd)
        user.first_name = Name
        user.save()
        messages.success(request, "Account created successfully. Please sign in.")
        return redirect('signinpage')
    return render(request, 'signup.html')

def signin(request):
    return render(request, 'signin.html')

def signinpage(request):
    if request.method == 'POST':
        unm = request.POST.get('username')
        pwd = request.POST.get('password')

        if not (unm and pwd):
            messages.error(request, "Username and password are required.")
            return render(request, 'signin.html')

        user = auth.authenticate(username=unm, password=pwd)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Welcome {user.first_name}!")
            return redirect('index')
        messages.error(request, "Invalid username or password.")
        return render(request, 'signin.html')
    return render(request, 'signin.html')

def user(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'user.html', {'username': username})

def logout_view(request):
    auth.logout(request)
    return redirect('index')

def pdf_view(request):
    return render(request, 'pdf.html')

def generate_image(request):
    images = None
    error = None
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    if request.method == 'POST':
        try:
            prompt = request.POST.get('prompt')
            width = int(request.POST.get('width', 1024))
            height = int(request.POST.get('height', 1024))

            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
            payload = {"inputs": prompt, "parameters": {"width": width, "height": height}}

            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                image_data = base64.b64encode(response.content).decode('utf-8')
                image_url = f"data:image/png;base64,{image_data}"
                images = [image_url]

                GenerationHistory.objects.create(
                    prompt=prompt,
                    width=width,
                    height=height,
                    images=[image_url],
                    timestamp=timezone.now()
                )
            else:
                error = f"API Error: {response.status_code} - {response.text[:200]}"
        except Exception as e:
            error = f"Error: {str(e)}"

    history = GenerationHistory.objects.all().order_by('-timestamp')[:10]
    return render(request, 'generate_image.html', {
        'images': images,
        'error': error,
        'current_time': current_time,
        'history': history
    })
