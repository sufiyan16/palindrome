

from urllib import response
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from yaml import serialize
from .serializers import PalindromeSerializer, CreatePalindromeSerializer, RegisterSerializer, UpdateUserSerializer
from palindrome.models import Palindrome
from users.models import Profile
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny

from pal.api import serializers


@api_view(['GET'])
def getRoutes(request):

    routes=[
        {'GET':'api/palindrome/'},
        {'GET':'api/palindrome/id/'},
        {'GET':'api/create-palindrome/'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPalindromes(request):
    pal=Palindrome.objects.all()
    serializer=PalindromeSerializer(pal,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPalindrome(request,pk):
    pal=Palindrome.objects.get(id=pk)
    serializer=PalindromeSerializer(pal,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPalindrome(request):
    profile=request.user.profile

    serializer=CreatePalindromeSerializer(data=request.data)
    
    if serializer.is_valid():
        #validatedData = serializer.validated_data
        #validatedData['owner'] = profile
        #print(serializer.validated_data["owner"])

        a=serializer.validated_data['input']
        b=a[::-1]
        print(b)
        if a==b:
            serializer.save(owner=profile)
            print("yes")
            custom_data = {
            "status": True,
            "error": False,
            "message": 'You won the game',
            "data": serializer.data
        }
            return Response(custom_data)
        else:
            print("No")
            custom_data = {
            "status": False,
            "error": True,
            "message": 'You Loss the game, this character is not palidrome',
            "data": serializer.data
        }
            return Response(custom_data)
            
            
        #print(serializers)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatePalindrome(request,pk):
    profile=request.user.profile
    pal=Palindrome.objects.get(id=pk)
    print(pal)
    serializer=CreatePalindromeSerializer(instance=pal,data=request.data)
    if serializer.is_valid():    
        if pal.owner == profile:
            a=serializer.validated_data['input']
            print(a)
            b=a[::-1]
            serializer.save()
            custom_data = {
            "status": True,
            "error": True,
            "message": 'You have updated your palindrome',
            "data": serializer.data
}
        
            return Response(custom_data)
        
        else:
            custom_data = {
                "status": False,
                "error": False,
                "message": 'You cannot update different user palindrome',
                "data": serializer.data
            }

            return Response(custom_data)
            
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePalindrome(request,pk):

    try:
        pal=Palindrome.objects.get(id=pk)
       
    except Palindrome.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    
    if request.method=="DELETE" and request.user.profile==pal.owner:
           
            pal.delete()
            return Response(
            {'message': "deleted succesfully"},
        
        )
    else:
        return Response(
        {'message': "you do not have permission to do this action"},
    
    )

class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateUser(request,pk):
    profile=Profile.Objects.get(id=pk)
    serializer=UpdateUserSerializer(instance=profile,data=request.data)
    if serializer.is_valid():    
        serializer.save()
        return Response(serializer.data)
