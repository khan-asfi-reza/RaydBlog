from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, \
    UpdateAPIView
from rest_framework.mixins import CreateModelMixin

from Apps.Core.permissions.is_post_authenticated import IsPostAndAuthenticated, IsEditAuthenticatedOrTrue


class CreateAPI(APIView):
    """
    Create API For Non Model Object
    """
    serializer_class = None

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_class(**kwargs, context={"request": self.request})

    def post(self, request, *args, **kwargs):
        serialized_data = self.get_serializer_class(data=request.data)
        if serialized_data.is_valid():
            data = serialized_data.save()
            return Response(
                data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CoreUpdateAPIView(UpdateAPIView):
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CoreRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CoreRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserCreateListAPIView(ListCreateAPIView):
    """
    Must have User Field in model
    """
    permission_classes = [IsPostAndAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    """
    Must have User Field in Model
    """
    permission_classes = [IsEditAuthenticatedOrTrue]

