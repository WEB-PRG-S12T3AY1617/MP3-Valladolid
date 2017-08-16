"""mp3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
import post.views

urlpatterns = [
    url(r'^viewItem/accept/', post.views.accept),
    url(r'^viewItem/reject/', post.views.reject),
    url(r'^cancel/', post.views.cancel),
    url(r'^messages/', post.views.messages),
    url(r'^offer/', post.views.offer),
    url(r'^viewItem/', post.views.viewItem),
    url(r'^post/', post.views.post),
    url(r'^profile/', post.views.profile),
    url(r'^logout/', post.views.logout),
    url(r'^login/', post.views.login),
    url(r'^register/', post.views.register),
    url(r'^admin/', admin.site.urls),
    url(r'^$', post.views.viewPosts),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
