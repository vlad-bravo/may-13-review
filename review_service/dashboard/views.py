from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from review_analytics.utils import get_review_stats, generate_review_chart
from review_analytics.tasks import send_telegram_report
from django.conf import settings
import googlemaps

@login_required
def dashboard_home(request):
    user = request.user
    stats = get_review_stats(user)
    chart = generate_review_chart(stats)
    
    # Инициализация Google Maps
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    context = {
        'stats': stats,
        'chart': chart,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def send_report(request):
    if request.method == 'POST':
        user = request.user
        send_telegram_report.delay(user.id)
        # Можно добавить сообщение об успешной отправке
    return render(request, 'dashboard/reports.html')
