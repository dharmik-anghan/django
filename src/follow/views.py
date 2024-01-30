from rest_framework.views import APIView
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from .serializers import FollowSerializer, FollowerSerializer, FollowingSerializer
from account.models import User
from rest_framework.response import Response
from .models import Follow

# Create your views here.


class FollowViews(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def follower_count_user(self, followed_to):
        follower_count = Follow.objects.filter(followed_to=followed_to).count()
        user = User.objects.get(pk=followed_to)
        user.follower_count = follower_count
        user.save()

    def folloing_count_user(self, followed_by):
        following_count = Follow.objects.filter(followed_by=followed_by).count()
        user = User.objects.get(pk=followed_by)
        user.following_count = following_count
        user.save()

    def post(self, request):
        data = {}
        data["followed_by"] = request.user.id
        data["followed_to"] = request.query_params.get("id")

        if int(data["followed_by"]) == int(data["followed_to"]):
            return Response({"msg": "Can't perform this action"}, status=400)

        if Follow.objects.filter(
            followed_by=data["followed_by"], followed_to=data["followed_to"]
        ).exists():
            return Response({"msg": "Already followed"}, status=200)

        if data["followed_to"]:
            try:
                user = User.objects.get(pk=data["followed_to"])
            except User.DoesNotExist:
                return Response({"msg": "User not found"}, status=404)
            serializer = FollowSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.follower_count_user(data["followed_to"])
            self.folloing_count_user(data["followed_by"])
            return Response({"msg": serializer.data}, status=201)
        else:
            return Response({"msg": "ID required"}, status=400)

    def delete(self, request):
        data = {}
        data["followed_by"] = request.user.id
        data["followed_to"] = request.query_params.get("id")

        if Follow.objects.filter(
            followed_by=data["followed_by"], followed_to=data["followed_to"]
        ).exists():
            try:
                follow_info = Follow.objects.get(
                    followed_by=data["followed_by"], followed_to=data["followed_to"]
                )
                follow_info.delete()
                self.follower_count_user(data["followed_to"])
                self.folloing_count_user(data["followed_by"])
                return Response({"msg": "User unfollowed"}, status=200)
            except:
                return Response({"msg": "Something went wrong"}, status=400)
        else:
            return Response({"msg": "Not following user"}, status=200)


class GetFollowerView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("id")
        users = Follow.objects.filter(followed_to=user_id).all()
        serializer = FollowerSerializer(users, many=True)
        return Response(serializer.data)


class GetFollowingView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("id")
        users = Follow.objects.filter(followed_by=user_id).all()
        serializer = FollowingSerializer(users, many=True)
        return Response(serializer.data)
