from rest_framework import generics
from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "Logged in successfully",
                "access_token": access_token,
                "refresh_token": str(refresh),
                "role": user.role,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# List all users (Admin only)
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Ensure only admin can access

# Add a user (Admin only)
class AddUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Delete a user (Admin only)
class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

