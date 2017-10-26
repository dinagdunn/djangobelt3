# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'main/index.html')

def process(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'],email=request.POST['email'], password=hashed_pw, bday=request.POST['birthday'])
        request.session['id'] = user.id
        request.session['name']= user.name
        return redirect('/pokes')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        request.session['name']= login_return['user'].name
        return redirect('/pokes')
    else:
        messages.error(request, login_return['errors'])
        return redirect('/')


def pokes(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

    user = User.objects.get(id=request.session['id'])

    context = {
        # 'mypokes': Poke.objects.filter(pokes=user),
        'mypokes': Poke.objects.filter(id=request.session['id']),

        'allusers': User.objects.exclude(id=request.session['id']),

    }
    return render(request, 'main/pokes.html', context)

def newpoke(request):
    
    if request.method == 'POST':
        newpoke = Poke.objects.create(poke_hist=request.POST['poke_hist'], poker_id=request.session['id'])
    
    
        a = Poke.objects.get(id=newpoke.id)

        User.objects.get(id=request.session['id']).tot_pokes.add(a)
    
        
    return redirect('/pokes')
    
def logout(request):
    del request.session
    return redirect('/')