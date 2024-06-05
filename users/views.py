from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.throttling import UserRateThrottle
from .serializers import UserSerializer, FriendRequestSerializer, ProfileSerializer
from .models import FriendRequest


class CustomPagination(PageNumberPagination):
    page_size = 10


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        request.data['email'] = request.data.get('email', '').lower()
        return super().post(request, *args, **kwargs)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get('q', '').lower()
        if '@' in keyword:
            return User.objects.filter(email__iexact=keyword)
        return User.objects.filter(
            Q(username__icontains=keyword) |
            Q(first_name__icontains=keyword) |
            Q(last_name__icontains=keyword)
        )


class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend_requests'


class FriendRequestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]
    serializer_class = FriendRequestSerializer

    def post(self, request, to_user_id):
        from_user = request.user
        to_user = User.objects.get(id=to_user_id)
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)

        if created:
            return Response({'status': 'Friend request sent.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)


class RespondFriendRequestView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id, action):
        try:
            user = request.user
            friend_request = FriendRequest.objects.get(id=request_id, to_user=user)
            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                user.profile.friends.add(friend_request.from_user.profile)
                friend_request.from_user.profile.friends.add(user.profile)
                return Response({'status': 'Friend request accepted.'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                friend_request.status = 'rejected'
                friend_request.save()
                return Response({'status': 'Friend request rejected.'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
        except FriendRequest.DoesNotExist:
            return Response({'status': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)


class ListFriendsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(profile__in=self.request.user.profile.friends.all())


class ListPendingRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')