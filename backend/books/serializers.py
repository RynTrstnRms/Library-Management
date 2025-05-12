from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, BorrowTransaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'copies_available', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_isbn(self, value):
        # Ensure ISBN is 10 or 13 characters long
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 characters long")
        return value

    def validate_copies_available(self, value):
        # Ensure copies_available is a positive integer
        if value < 0:
            raise serializers.ValidationError("Number of copies must be a positive integer")
        return value

class BorrowTransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BorrowTransaction
        fields = ['id', 'user', 'book', 'user_id', 'book_id', 'borrow_date', 'return_date', 'status']
        read_only_fields = ['borrow_date', 'return_date', 'status']

    def validate(self, data):
        book = Book.objects.filter(id=data['book_id']).first()
        if not book:
            raise serializers.ValidationError("The selected book does not exist.")
        if book.copies_available <= 0:
            raise serializers.ValidationError("No copies of this book are available for borrowing.")
        return data
