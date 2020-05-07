from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

app_name = 'lesson'


class MyHackedView(auth_views.PasswordResetView):
    success_url = reverse_lazy('lesson:password_reset_done')


urlpatterns = [
    path('materials/', views.all_materials, name='all_materials'),
    path('', views.all_lessons, name='all_lessons'),
    # path('', views.MaterialListView.as_view(), name='all_materials'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.material_details,
         name='material_details'),
    path('<slug:slug>/',
         views.lesson_details,
         name='lesson_details'),

    path('<int:material_id>/share/', views.share_material,
         name='share_material'),
    path('create/', views.create_form, name='create_form'),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', MyHackedView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('lesson:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.view_profile, name='profile'),
    path('register/', views.register, name='register'),
    path('edit_user/', views.edit_user, name='edit_user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
