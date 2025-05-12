from django.urls import path
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .views import BookViewSet, BorrowTransactionViewSet
from .serializers import UserSerializer


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


urlpatterns = [
    #ENDPOINT NG BOOKS
    path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='book-detail'),
    path('books/<int:pk>/delete/', BookViewSet.as_view({'delete': 'destroy'}), name='book-delete'),
    
    #ENDPOINT NG TRANSACTIONS
    path('transactions/', BorrowTransactionViewSet.as_view({'get': 'list'}), name='transaction-list'),
    path('transactions/<int:pk>/', BorrowTransactionViewSet.as_view({'get': 'retrieve'}), name='transaction-detail'),
    
    #ENDPOINT NG BORROW
    path('borrow/', BorrowTransactionViewSet.as_view({'post': 'create'}), name='borrow-book'),
    path('return/<int:borrow_id>/', BorrowTransactionViewSet.as_view({'post': 'return_book'}), name='return-book'),

    #ENDPOINT NG USERS
    path('users/', UserListView.as_view(), name='user-list'),
]
