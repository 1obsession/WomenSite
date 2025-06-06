from django.urls import path, register_converter
from django.views.decorators.cache import cache_page

from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', cache_page(30)(views.WomenHome.as_view()), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostlist.as_view(), name='tag'),
    path('edit_page/<slug:edit_slug>/', views.UpdatePage.as_view(), name='edit_page'),
]


