from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    """
    List all profiles
    """

    def get(self, request):
        """
        Get request to retrieve all profile objects
        and return serialized data
        """
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileDetail(APIView):
    """
    Display details of specific profile based on primary key
    """
    serializer_class = ProfileSerializer
    def get_object(self, pk):
        """
        Get request to retrieve single profile object
        based upon id
        """
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Gets and returns serialized data
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Put method to allow for editing of profile, name, content, image
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
