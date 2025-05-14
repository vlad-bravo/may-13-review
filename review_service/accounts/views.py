from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    TelegramConnectForm
)
# import telegram
from django.conf import settings

class CustomLoginView(LoginView):
    """
    Custom login view that uses the custom authentication form
    and redirects to the dashboard after login.
    """
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        """Add success message on login."""
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('dashboard_home')


class CustomLogoutView(LogoutView):
    """
    Custom logout view that adds a success message.
    """
    next_page = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    """
    View for new user registration.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard_home')
    
    def form_valid(self, form):
        """Log the user in after successful registration."""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Регистрация прошла успешно!')
        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    View for user profile management, including Telegram connection.
    """
    model = CustomUser
    fields = ['company_name', 'phone', 'email']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['telegram_form'] = TelegramConnectForm()
        return context
    
    def post(self, request, *args, **kwargs):
        # Handle Telegram connection separately
        if 'connect_telegram' in request.POST:
            return self._handle_telegram_connection(request)
        return super().post(request, *args, **kwargs)
    
    def _handle_telegram_connection(self, request):
        form = TelegramConnectForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']
            
            try:
                # Verify the code with Telegram
                bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
                updates = bot.get_updates()
                
                for update in updates:
                    if update.message and update.message.text == verification_code:
                        # Save the chat ID
                        request.user.telegram_chat_id = update.message.chat.id
                        request.user.save()
                        messages.success(request, 'Telegram успешно подключен!')
                        return redirect('profile')
                
                messages.error(request, 'Код не найден. Убедитесь, что вы отправили код боту.')
            except Exception as e:
                messages.error(request, f'Ошибка подключения Telegram: {str(e)}')
        
        return self.get(request)


def telegram_webhook(request):
    """
    View for handling Telegram bot webhook.
    This would be set up as the webhook URL in your Telegram bot.
    """
    if request.method == 'POST':
        try:
            update = telegram.Update.de_json(request.json, bot)
            chat_id = update.message.chat.id
            text = update.message.text
            
            # Check if this is a verification code from a user
            if text.isdigit() and len(text) == 6:
                # In a real implementation, you would match this with a user
                # and update their telegram_chat_id
                pass
            
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'})


def get_telegram_verification_code(request):
    """
    View that generates and displays a verification code for Telegram connection.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    import random
    verification_code = str(random.randint(100000, 999999))
    request.session['telegram_verification_code'] = verification_code
    
    context = {
        'verification_code': verification_code,
        'bot_username': settings.TELEGRAM_BOT_USERNAME,
    }
    
    return render(request, 'accounts/telegram_verification.html', context)
