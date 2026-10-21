from rest_framework import status, views, permissions
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer

class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Registration successful.',
                'user': UserDetailSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = data['user']
            student_id = None
            if hasattr(user, 'student_profile'):
                student_id = str(user.student_profile.student_id)
            
            return Response({
                'message': 'Login successful.',
                'user': UserDetailSerializer(user).data,
                'student_id': student_id,
                'tokens': {
                    'access': data['access'],
                    'refresh': data['refresh']
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserDetailSerializer(user).data
        if hasattr(user, 'student_profile'):
            data['student_id'] = str(user.student_profile.student_id)
        if user.role == User.Role.COUNSELOR:
            from schools.serializers import SchoolSerializer
            assigned = user.schools.all()
            data['assigned_schools'] = SchoolSerializer(assigned, many=True).data
        return Response(data)

    def patch(self, request):
        user = request.user
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            if hasattr(user, 'student_profile'):
                data['student_id'] = str(user.student_profile.student_id)
            if user.role == User.Role.COUNSELOR:
                from schools.serializers import SchoolSerializer
                assigned = user.schools.all()
                data['assigned_schools'] = SchoolSerializer(assigned, many=True).data
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
