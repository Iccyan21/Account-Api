from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, AccessToken

# ログイン処理
class LoginSerializer(serializers.Serializer):
    UserID = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        UserID = data.get('UserID')
        password = data.get('password')
        userid = User.objects.get(UserID=UserID)
        re_password = User.objects.get(password=password)
        if UserID == userid.UserID:
            if password == re_password.password:
                return data

            else:
                raise serializers.ValidationError('ログイン失敗')



# ここのUserSerialzerは全てのフィールドを表すシリアルライザー
# このシリアルライザーを使用するとUserモデルの全てのフィールドを表示
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['UserID', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}



# これは新規登録用のシリアルライザー、新規登録に必要なフィールドだけを記述
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('UserID','name','email','password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user

# Update用のシリアライザー        
class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, allow_blank=True)
    comment = serializers.CharField(max_length=100, allow_blank=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
    
class CloseAccountSerializer(serializers.Serializer):
    message = serializers.CharField(default="Account and user successfully removed")
