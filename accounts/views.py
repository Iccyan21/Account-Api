from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from django.conf import settings
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .models import AccessToken, User

from .serializers import LoginSerializer, RegisterSerializer, UserUpdateSerializer, CloseAccountSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

class LoginView(GenericAPIView):
    """ログインAPIクラス"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(UserID=serializer.validated_data["UserID"])
            userid = serializer.validated_data['UserID']
            token = AccessToken.create(user)
            return Response({'detail': "ログインが成功しました。", 'error': 0, 'token': token.token, 'UserID': userid})
        return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)

# ログアウト
class LogoutView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        logout(request)
        return Response({'detail': "ログアウトが成功しました。"})
    

# 新規登録処理
# これは新規登録用のシリアルライザー、新規登録に必要なフィールドだけを記述
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    print("RegisterView")
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # すでにEmailが使われている場合
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                print("email")
                return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)

            # パスワードと確認パスワードが一致しない場合
            if serializer.validated_data['password'] != request.data['password_confirmation']:
                print("password")
                return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)


            # UserIDがすでに使われていた場合
            if User.objects.filter(UserID=serializer.validated_data['UserID']).exists():
                print("UserID")
                return Response({'error': 3}, status=HTTP_400_BAD_REQUEST)

            # エラーなし
            try:
                serializer.save()
            except:
                # データベースエラー
                print("データベースエラー")
                return Response({'error': 11}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            

            return Response(serializer.data, status=HTTP_201_CREATED)
        print("バリデーションエラー")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request, UserID):
        # ユーザ情報の取得
        user = User.objects.filter(UserID=UserID).first()

        if not user:
            # ユーザが存在しない場合
            return Response({"message": "No User found"}, status=404)

        response_data = {
            "message": "User details by UserID",
            "user": {
                "user_id": user.UserID,
                "nickname": user.name,
                "comment": user.comment,
            }
        }

        return JsonResponse(response_data, status=200, charset='utf-8',json_dumps_params={'ensure_ascii': False})


class UserUpdateView(APIView):
    def patch(self, request, UserID):
        # ユーザ情報の取得
        user = User.objects.filter(UserID=UserID).first()

        if not user:
            # ユーザが存在しない場合
            return JsonResponse({"message": "No User found"}, status=404)

        if UserID != user.UserID:
            # 認証と異なるIDのユーザを指定した場合
            return JsonResponse({"message": "No Permission for Update"}, status=403)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            response_data = {
                "message": "User successfully updated",
                "user": {
                    "name": user.name,
                    "comment": user.comment
                }
            }
            return JsonResponse(response_data, status=200,json_dumps_params={'ensure_ascii': False})
        else:
            error_message = serializer.errors.get('non_field_errors', ['User updation failed'])[0]
            return JsonResponse({"message": "User updation failed", "cause": error_message}, status=400)

    def post(self, request, UserID):
        return JsonResponse({"message": "Method not allowed"}, status=405)
 
class CloseAccountView(APIView):
    def post(self, request,UserID):
        ## アカウントの削除処理
        try:
            user = User.objects.filter(UserID=UserID).first()
            user.delete()
        except User.DoesNotExist:
            raise JsonResponse("No User found")

        return JsonResponse({"message": "Account and user successfully removed"}, status=200)
        
