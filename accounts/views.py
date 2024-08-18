from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import json

User = get_user_model()


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_pending:
                return JsonResponse({'error': 'Account is pending approval'}, status=403)
            login(request, user)
            profile_image_url = user.profile_image.url if user.profile_image else None
            return JsonResponse({'message': 'Login successful'
                                 , 'username': user.username
                                 , 'is_authenticated': True
                                 , 'is_pending': user.is_pending
                                 , 'profile_image_url': profile_image_url
                                 }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            email = data['email']
            username = data['username']
            password = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()

            return JsonResponse({'message': 'User created successfully'}, status=201)

        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def signout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def user_info(request):
    user = request.user
    data = {
        'username': user.username,
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
    }
    return JsonResponse(data)


@csrf_exempt
def check_auth(request):
    if request.user.is_authenticated:
        profile_image_url = request.build_absolute_uri(
            request.user.profile_image.url) if request.user.profile_image else None
        return JsonResponse({
            'is_authenticated': True,
            'username': request.user.username,
            'profile_image_url': profile_image_url,
        }, status=200)
    else:
        return JsonResponse({'isAuthenticated': False}, status=200)


def approve_user(request, user_id):
    if request.user.is_admin:
        user = CustomUser.objects.get(id=user_id)
        user.role = 'member'
        user.save()
        return redirect('user_list')


def pending_check(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_pending:
            return HttpResponseForbidden("Your account is pending approval.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def pending(request):
    return render(request, 'accounts/pending.html')


