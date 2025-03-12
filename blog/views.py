from itertools import chain
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic import UpdateView, TemplateView, FormView


from . import forms
from .models import Ticket, Review, UserFollow

User = get_user_model()


class FluxView(LoginRequiredMixin, ListView):
    template_name = 'blog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        followed_user_ids = UserFollow.objects.filter(
            user=user).values_list('followed_user', flat=True)
        tickets = Ticket.objects.filter(
            user__in=followed_user_ids) | Ticket.objects.filter(user=user)
        reviews = Review.objects.filter(
            user__in=followed_user_ids) | Review.objects.filter(user=user)
        posts = sorted(list(tickets) + list(reviews),
                       key=lambda x: x.time_created, reverse=True)
        return posts


@login_required
def post(request):
    tickets = Ticket.objects.all()
    return render(request, 'blog/tickets.html', context={'tickets': tickets})


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
    return render(request, 'blog/photo_upload.html', context={'form': form})


@login_required
def ticket_upload(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            if photo_form:
                image = photo_form.save(commit=False)
                image.uploader = request.user
                image.save()
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.image = image
            ticket.save()
            return redirect('posts')

    context = {'ticket_form': ticket_form,
               'photo_form': photo_form,
               }
    return render(request, 'blog/create_ticket.html', context=context)


class SubscriptionsView(LoginRequiredMixin, TemplateView):

    template_name = 'blog/subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['following'] = UserFollow.objects.filter(user=user)
        context['followers'] = UserFollow.objects.filter(followed_user=user)
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = "blog/create_ticket.html"
    form_class = forms.TicketForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'photo_form' not in context:
            context['photo_form'] = forms.PhotoForm
        context["submit_text"] = 'Créer'
        return context

    def form_valid(self, form):
        photo_form = forms.PhotoForm(self.request.POST, self.request.FILES)

        if photo_form.is_valid():
            image = photo_form.save(commit=False)
            image.uploader = self.request.user
            image.save()

            ticket = form.save(commit=False)
            ticket.user = self.request.user
            ticket.image = image
            ticket.save()
            return super().form_valid(form)
        else:
            ticket = form.save(commit=False)
            ticket.user = self.request.user
            ticket.save()
            return super().form_valid(form)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'blog/ticket.html'
    context_object_name = 'ticket'


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'Blog/create_ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'photo_form' not in context:
            context['photo_form'] = forms.PhotoForm
        context["submit_text"] = 'Modifier'
        return context


class BlogTicketView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "blog/tickets.html"
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = context['tickets']
        reviews = Review.objects.filter(ticket__in=tickets)

        reviews_by_ticket = {ticket.id: [] for ticket in tickets}
        for review in reviews:
            reviews_by_ticket[review.ticket.id].append(review)
        context["reviews_by_ticket"] = reviews_by_ticket
        return context


class UserPostViews(LoginRequiredMixin, ListView):

    template_name = "blog/user_posts.html"
    context_object_name = "user_posts"
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        tickets = Ticket.objects.filter(user=user)
        reviews = Review.objects.filter(user=user)
        user_posts = sorted(chain(
            tickets, reviews), key=lambda instance: instance.time_created,
            reverse=True)
        return user_posts


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'blog/delete_ticket.html'
    context_object_name = "ticket"
    success_url = reverse_lazy("home")


class ReviewCreateView (LoginRequiredMixin, CreateView):
    model = Review
    form_class = forms.ReviewForm
    template_name = 'blog/create_review.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Créer"
        return context


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'blog/review.html'
    context_object_name = "review"


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = forms.ReviewForm
    template_name = "blog/create_review.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Modifier"
        return context


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'blog/delete_review.html'
    context_object_name = "review"
    success_url = reverse_lazy('home')


class FollowDeleteView(LoginRequiredMixin, DeleteView):
    model = UserFollow
    template_name = 'blog/unfollow.html'
    context_object_name = "followed_user"
    success_url = reverse_lazy("subscriptions")


class TicketAndReviewCreateView(LoginRequiredMixin, FormView):
    template_name = 'blog/create_ticket_and_review.html'
    success_url = reverse_lazy('posts')
    form_class = forms.TicketForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'ticket_form' not in context:
            context['ticket_form'] = forms.TicketForm()
        if 'photo_form' not in context:
            context['photo_form'] = forms.PhotoForm()
        if 'review_form' not in context:
            context['review_form'] = forms.ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), photo_form.is_valid(),
                review_form.is_valid()]):
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
            return redirect(self.success_url)
        else:
            return self.form_invalid(ticket_form)


@login_required
def search_users(request):
    query = request.GET.get("q", "").strip()
    following_ids = UserFollow.objects.filter(
        user=request.user).values_list("followed_user_id", flat=True)

    users = User.objects.exclude(
        id=request.user.id).exclude(id__in=following_ids)

    if query:
        users.filter(username__icontains=query)

    following = UserFollow.objects.filter(user=request.user)
    followers = UserFollow.objects.filter(followed_user=request.user)

    return render(request, "blog/subscriptions.html",
                  {'users': users,
                   'query': query,
                   'following': following,
                   "followers": followers})


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        UserFollow.objects.get_or_create(
            user=request.user, followed_user=user_to_follow)
    return redirect('subscriptions')


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = UserFollow.objects.filter(
        user=request.user, followed_user=user_to_unfollow).first()
    if follow:
        follow.delete()
    return redirect('subscriptions')


@login_required
def block_user(request, pk):
    follow = get_object_or_404(UserFollow, pk=pk)

    if follow.followed_user == request.user:
        follow.blocked_follower = True
        follow.save
    return redirect('subscriptions')


@login_required
def unblock_user(request, pk):
    follow = get_object_or_404(UserFollow, pk=pk)

    if follow.followed_user == request.user:
        follow.blocked_follower = False
        follow.save
    return redirect('subscriptions')

class BlockUserView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        follow = get_object_or_404(UserFollow, pk=pk)
        if follow.followed_user == request.user:
            follow.blocked_follower = True
            follow.save()
        return HttpResponseRedirect(reverse_lazy('subscriptions'))

class UnblockUserView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        follow = get_object_or_404(UserFollow, pk=pk)
        if follow.followed_user == request.user:
            follow.blocked_follower = False
            follow.save()
        return HttpResponseRedirect(reverse_lazy('subscriptions'))