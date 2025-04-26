from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomSignupForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Require email verification
            user.save()
            
            # Send verification email
            send_verification_email(request, user)
            return redirect('signup_pending')
    else:
        form = CustomSignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def send_verification_email(request, user):
    subject = "Verify Your Email Address"
    message = render_to_string('emails/verification_email.html', {
        'user': user,
        'domain': request.get_host(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject, message, 'noreply@markethub.com', [user.email])