from allauth.account.views import SignupView, LoginView
from .forms import CustomLoginForm, CustomSignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from .forms import UserProfileForm, UserInterestForm
from .models import UserProfile
from post.models import Post, UserInterest


class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        print("Triggered")
        return response

@login_required
def sign_out(request):
    logout(request)
    return redirect('login')



@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_interest, created = UserInterest.objects.get_or_create(user=request.user)
    total_posts = Post.objects.filter(created_by=request.user).count()
    posts = Post.objects.filter(created_by=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        interest_form = UserInterestForm(request.POST, instance=user_interest)
        
        if profile_form.is_valid() and interest_form.is_valid():
            profile_form.save()
            interest_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        interest_form = UserInterestForm(instance=user_interest)
    
    context = {
        'profile_form': profile_form,
        'interest_form': interest_form,
        'total_posts': total_posts,
        'posts': posts,
    }
    
    return render(request, 'auth_app/profile.html', context)
    
@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'auth_app/edit_profile.html', {'form': form})