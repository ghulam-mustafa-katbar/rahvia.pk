from rest_framework import status, views, permissions
from rest_framework.response import Response
from .models import Student
from .serializers import StudentProfileSerializer

class StudentProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            student = user.student_profile
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        try:
            student = user.student_profile
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentProfileSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
