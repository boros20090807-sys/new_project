from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from .models import Games, GamesReview ,SystemRequirements
from .serializers import (
    AutoSerializer,
    GamesReviewSerializer,
    RegisterSerializer,
    loginSerializer,
    SystemSerializer,
    PublisherSerializer,
)


def home(request):
    games = Games.objects.all()
    context = {
        'games': games,
    }
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html')



def deteilz(request, id):
    games=Games.objects.get(id=id)
    cotext={
        'games':games
    }
    return render(request, 'main/deteilz.html',cotext)




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


class GamesReviewListCreateView(ListCreateAPIView):
    queryset = GamesReview.objects.all()
    serializer_class = GamesReviewSerializer
    
    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_fields=['name','raiting']
    search_fields=['text','name']


class GamesReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = GamesReview.objects.all()
    serializer_class = GamesReviewSerializer

class AutoLisCreateView(ListCreateAPIView):
    queryset = Games.objects.all()
    serializer_class = AutoSerializer

    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_fields=['title','type_games','type_platform']
    search_fields=['description','title']

class AutoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Games.objects.all()
    serializer_class = AutoSerializer

class SystemListCreateView(ListCreateAPIView):
    queryset = SystemRequirements.objects.all()
    serializer_class = SystemSerializer

    filter_backends=[DjangoFilterBackend]
    filterset_fields=['os','processor','ram','graphics','storage']

class SystemDetailView(RetrieveUpdateDestroyAPIView):
    queryset = SystemRequirements.objects.all()
    serializer_class = GamesReviewSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = SystemRequirements.objects.all()
    serializer_class = PublisherSerializer