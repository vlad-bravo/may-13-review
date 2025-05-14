from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard_home, send_report
from accounts.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_home, name='dashboard_home'),
    path('reports/', send_report, name='send_report'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('reviews/', include('reviews.urls')),
]
