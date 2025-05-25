from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from .serializers import MovieSerializer,UserSerializer,VoteSerializer,MyVoteSerializer,UserRegister,MongoPersonSerializer,MongoMovieSerializer , MongoRatingSerializer
from .models import Movie,Vote,User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import filters
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import JsonResponse
from .models import MongoMovie
import json

class MongoMovieClass(generics.ListCreateAPIView):
    serializer_class = MongoMovieSerializer
    permission_classes= [AllowAny]

    def get_queryset(self):
        return MongoMovie.objects.all()
    
    def get(self,request , *args, **kwargs):
        return self.list(request , *args, **kwargs)
    
    def post (self , request , *args, **kwargs):
        return self.create(request , *args, **kwargs)



@api_view(["POST"])
@permission_classes([AllowAny])
def mongo_rating_view(request):
    if request.method == "POST":
        serializer = MongoRatingSerializer(data=request.data ,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)



@api_view(["POST"])
@permission_classes([AllowAny])
def mongo_person_view(request):
    if request.method == "POST":
        serializer = MongoPersonSerializer(data=request.data ,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)



class MovieViewsets(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields=['title','average_rating','year']
    ordering_fields=['average_rating']

    def get_permissions(self):
        if self.action in [ 'update_vote']:  # Changed to match action names
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    @action(detail=True, methods=['get','POST'], url_path='vote')
    def vote(self, request, pk=None):  # Renamed to just 'vote'
        if request.method == 'GET':
            return Response({"detail": "Submit your vote via POST"})
        movie = self.get_object()
        serializer = VoteSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            if movie.vote_set.filter(user=request.user).exists():
                return Response(
                    {'error': 'You have already voted for this movie'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get','put', 'patch'], url_path='update-vote')
    def update_vote(self, request, pk=None):
        if request.method == 'GET':
            return Response({"detail": "Update your vote via PUT"})
        movie = self.get_object()
        vote = get_object_or_404(movie.vote_set, user=request.user)
        
        serializer = VoteSerializer(vote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_class(self):
        if self.action in ['vote','update_vote'] :
            return VoteSerializer
        return super().get_serializer_class()
    

class CustomeTokenObtainPairView(TokenObtainPairView):
    def post(self,request,*args, **kwargs):
        try:
            response=super().post(request,*args, **kwargs)
            tokens = response.data

            access_token=tokens['access']
            refresh_token=tokens['refresh']


            res = Response()

            res.data={'success':True}

            res.set_cookie(
                key="access_token",
                value=str(access_token),
                httponly=True,
                secure=True,
                samesite="None",
                path='/'
            )
            res.set_cookie(
                key="refresh_token",
                value= str(refresh_token),
                httponly=True,
                secure=True,
                samesite="None",
                path='/'
            )
            res.data.update(tokens)
            return res
        except:
            return Response({'success':False})
        
@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    try:
        res=Response()
        res.data={'success':True}
        res.delete_cookie('access_token',path="/",samesite="None")
        res.delete_cookie('refresh_token',path='/',samesite="None")
        print(res)
        return res
        
    except:
        return Response({'success':False})
    

class MyRatings(generics.ListAPIView):
    serializer_class=MyVoteSerializer
    # permission_classes=[IsAuthenticated]
    def get_queryset(self):
        current_user=self.request.user
        return Vote.objects.filter(user=current_user)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def is_logged_in(request):
    serializer = UserSerializer(request.user, many=False)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer=UserRegister(data=request.data,context={"request":request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)
    # newuser.username=request.username
    # if (request.password == request.confirm_password):
    #     newuser.password=request.password
    # newuser.save()

@api_view(["GET"])
@permission_classes([AllowAny])
def all_users(request):
    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)