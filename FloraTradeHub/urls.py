
from django.contrib import admin
from django.urls import path, include
from core.views import HomePage, CategorySearch
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='homepage'),
    path('category_search/<int:category_id>/',
         CategorySearch.as_view(), name='category_search'),
    path('account/', include('profiles.urls')),
    path('flower/', include('flowers.urls')),

]
