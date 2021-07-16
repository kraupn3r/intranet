

from django.contrib import admin
from django.urls import include,path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls',namespace="accounts")),
    path('suggestions/',include('suggestions.urls',namespace="suggestions")),
    path('calendar/',include('calendary.urls',namespace="calendar")),
    path('',include('news.urls',namespace="news")),
    path('polls/',include('polls.urls',namespace="polls")),
    path('accounts/api/',include('accounts.api.urls')),
    path('calendar/api/',include('calendary.api.urls')),
    path('news/api/',include('news.api.urls')),
    path('suggestions/api/',include('suggestions.api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
