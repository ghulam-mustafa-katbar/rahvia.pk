from rest_framework import generics, permissions, filters
from .models import CareerField
from .serializers import CareerFieldSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.role == 'ADMIN')

class CareerFieldListCreateView(generics.ListCreateAPIView):
    queryset = CareerField.objects.filter(is_active=True).order_by('name')
    serializer_class = CareerFieldSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category', 'stream_requirement', 'typical_degrees', 'required_exams']

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        stream = self.request.query_params.get('stream')
        if category:
            qs = qs.filter(category=category)
        if stream:
            qs = qs.filter(stream_requirement=stream)
        return qs

class CareerFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareerField.objects.all()
    serializer_class = CareerFieldSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'field_id'
