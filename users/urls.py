from django.urls import path
from .views import SignupView, CustomLoginView, UserSearchView, FriendRequestView, RespondFriendRequestView, ListFriendsView, ListPendingRequestsView


urlpatterns = [
   path('signup/', SignupView.as_view(), name='signup'),
   path('login/', CustomLoginView.as_view(), name='login'),
   path('search/', UserSearchView.as_view(), name='search'),
   path('friends/', ListFriendsView.as_view(), name='friends'),
   path('pending-requests/', ListPendingRequestsView.as_view(), name='pending_requests'),
   path('send-request/<int:to_user_id>/', FriendRequestView.as_view(), name='send_request'),
   path('respond-request/<int:request_id>/<str:action>/', RespondFriendRequestView.as_view(), name='respond_request'),
]