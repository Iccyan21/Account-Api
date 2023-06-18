from . import views
from django.urls import path, include


urlpatterns = [
    path('sighup/', views.RegisterView.as_view(), name='user-signup'), # 新規登録処理'
    path('login/', views.LoginView.as_view(), name='user-login'), # ログイン処理
    path('users/<str:UserID>/', views.UserDetailView.as_view(), name='user-detail'), # ユーザ情報取得
    path('users/<str:UserID>/update/', views.UserUpdateView.as_view(), name='user-update'), # ユーザ情報更新
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('close/<str:UserID>/', views.CloseAccountView.as_view(), name='close-account'), # アカウント削除
]
