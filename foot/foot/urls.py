
from django.contrib import admin
from django.urls import path
from server import views
from knox import views as knox_views

urlpatterns = [
    path('admin/',                          admin.site.urls,                    name='admin'         ),
    path('api/login/',                      views.LoginAPI.as_view(),           name='login'         ),
    path('api/logout/',                     knox_views.LogoutView.as_view(),    name='logout'        ),
    path('api/get-all/',                    views.getAllAccount,                name='get-all'       ),
    path('api/register/',                   views.RegisterAPI.as_view(),        name='register'      ),
    path('api/logoutall/',                  knox_views.LogoutAllView.as_view(), name='logoutall'     ),
    path('api/get-user/<str:usr>',          views.getProfile,                   name='get-user'      ),
    path('api/get-history/<str:usr>',        views.getHistory,                   name='get-history'   ),
    path('api/update-profile/<str:usr>',    views.updateProfile,                name='update-profile'),
]
