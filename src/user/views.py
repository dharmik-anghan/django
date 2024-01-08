from .models import User
from django import http
from django.utils.timezone import now
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer

# Create your views here.
class UserAPI(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            # raise Response("User not found", status=status.HTTP_404_NOT_FOUND)
            raise http.Http404

    def get(self, request):
        pk = request.GET.get('id')
        if not pk:
            return Response({"message": "Id required"}, status=status.HTTP_200_OK)
        user = self.get_user(pk)
        context = UserSerializer(user)

        return Response({"User": context.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.data:
            return Response("Missing request in body", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        pk = request.GET.get('id')
        if not pk:
            return Response({"message": "Id required"}, status=status.HTTP_200_OK)
        if not request.data:
            return Response("Details Saved", status=status.HTTP_200_OK)
        
        user = self.get_user(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(updated_at = now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        pk = request.GET.get('id')
        if not pk:
            return Response({"message": "Id required"}, status=status.HTTP_200_OK)
        user = self.get_user(pk)
        user.delete()
        return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)