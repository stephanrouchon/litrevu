from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from . import forms
from . import models

User = get_user_model()

@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'blog/home.html', context={'tickets':tickets})

@login_required
def post(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'blog/tickets.html', context={'tickets':tickets})

@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form':form})
            

@login_required
def ticket_upload(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            image = photo_form.save(commit=False)
            image.uploader = request.user
            image.save()
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.image = image
            ticket.save()
            return redirect('posts')
            
    context = { 'ticket_form':ticket_form,
               'photo_form':photo_form,
               }
    return render(request, 'blog/create_ticket.html', context=context)

@login_required
def view_post(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review =get_object_or_404(models.Review, ticket=ticket )
    return render(request, 'blog/view_post.html', {'ticket':ticket, 'review':review, 'user':request.user})

@login_required
def edit_ticket(request, ticket_id):
    ticket =  get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context= {
        'edit_form': edit_form,
        'delete_form' : delete_form,
    }
    return render(request, 'blog/edit_ticket.html', context=context)


@login_required
def review_create(request):
    review_form = forms.ReviewForm()
    if request.method =='POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid() :
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
        
    context = {'review_form':review_form}
    return render(request, 'blog/create_review.html', context=context)

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, user_id)
    if request.user != user_to_follow:
        models.UserFollow.objects.get_or_create(user=request.user, followed_user=user_to_follow)
    return redirect('profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = models.UserFollow.objects.get_or_create(user=request.user, followed_user=user_to_unfollow)
    follow.delete()
    return redirect('profile', user_id=user_id)

@login_required
def subscriptions(request):
    user = request.user
    following = models.UserFollow.objects.filter(user=user)
    followers = models.UserFollow.objects.filter(followed_user=user)
    context = {
        'following': following,
        'followers': followers,
    }
    return render(request, 'blog/subscriptions.html', context=context)

@login_required
def ticket_and_review(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    review_form = forms.ReviewForm()

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), photo_form.is_valid(), review_form.is_valid()]):
            image = photo_form.save(commit=False)
            image.uploader = request.user
            image.save()
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.image = image
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('posts')
            
    context = { 'ticket_form':ticket_form,
               'photo_form':photo_form,
               'review_form':review_form,
               }
    return render(request, 'blog/create_ticket_and_review.html', context=context)
    