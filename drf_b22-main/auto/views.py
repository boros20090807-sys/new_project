from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Games, GamesReview ,SystemRequirements,Publisher
from .serializers import (
    GamesSerializer,
    GamesReviewSerializer,
    RegisterSerializer,
    loginSerializer,
    SystemSerializer,
    PublisherSerializer,
)

@api_view(['POST'])
def logout(request):
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
        return Response({'messages': 'successful'})
    return Response({'error': 'вы не были авторизованы'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login(request):
    serializer = loginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'messages': 'вы успешно зашли в аккаунт',
                'my_token': token.key,
            }
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'Answer': 'Successful',
                'username': user.username,
                'token': token.key,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def auto_list(request):
#     auto = Games.objects.all()
#     paginator = PageNumberPagination()
#     paginator.page_size = 1
#     page = paginator.paginate_queryset(auto, request)
#     serializers = AutoSerializer(page, many=True)
#     return paginator.get_paginated_response(serializers.data)


# @api_view(['POST'])
# def auto_create(request):
#     serializers = AutoSerializer(data=request.data)
#     if serializers.is_valid():
#         serializers.save()
#         return Response(serializers.data, status=status.HTTP_201_CREATED)
#     return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT', 'PATCH'])
# def auto_update(request, pk):
#     auto = get_object_or_404(Games, pk=pk)
#     serializers = AutoSerializer(
#         auto,
#         partial=True,
#         data=request.data
#     )
#     if serializers.is_valid():
#         serializers.save()
#         return Response(serializers.data)
#     return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def auto_detail(request, pk):
#     auto = get_object_or_404(Games, pk=pk)
#     serializers = AutoSerializer(auto)
#     return Response(serializers.data)


# @api_view(['DELETE'])
# def auto_delete(request, pk):
#     auto = get_object_or_404(Games, pk=pk)
#     auto.delete()
#     return Response(
#         {'messages': 'The game was deleted'},
#         status=status.HTTP_204_NO_CONTENT
#     )

class GamesReviewViewSet(ModelViewSet):
    queryset = GamesReview.objects.all()
    serializer_class = GamesReviewSerializer

    permission_classes= [
        IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        queryset = GamesReview.objects.all()

        min_rating = self.request.query_params.get('min_rating')

        if min_rating:
            queryset = queryset.filter(raiting__gte=min_rating)

        return queryset

    def perform_created(self,serializer):
        serializer.save(user = self.request.user)


class GamesReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = GamesReview.objects.all()
    serializer_class = GamesReviewSerializer


class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer


    @action(detail=False, methods=['get'])
    def expensive(self, request):
        autos = Games.objects. filter(price__gte = 100)

        serializer = GamesSerializer(
            autos,
            many = True
        )
        return Response(serializer.data)   

    @action(detail=False, methods=['get'])
    def game_type(self, request):
        type_games = request.query_params.get('type_games')
        type_platform = request.query_params.get('type_platform')
        publisher=request.query_params.get('publisher')

        queryset = Games.objects.all()

        if type_games:
            queryset = queryset.filter(type_games=type_games)
        if type_platform:
            queryset = queryset.filter(type_platform=type_platform)
        if publisher:
            queryset = queryset.filter(publisher=publisher)
    
        serializer = GamesSerializer(
                queryset,
                many = True
        )
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def reviews(self, request, pk = None):
        auto = self.get_object()
        reviews = GamesReview.objects.filter(game=auto)

        serializer = GamesReviewSerializer(
            reviews,
            many = True
        )   
        return Response(serializer.data)

    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_fields=['type_games','type_platform','publisher']

class SystemViewSet(viewsets.ModelViewSet):
    queryset = SystemRequirements.objects.all()
    serializer_class = SystemSerializer

    filter_backends=[DjangoFilterBackend]
    filterset_fields=['os','processor','ram','graphics','storage']


class SystemDetailView(RetrieveUpdateDestroyAPIView):
    queryset = SystemRequirements.objects.all()
    serializer_class = SystemSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer