from .serializers import VideoSerializer
from .pagination import VideoPagination
from rest_framework import generics
from django.db.models import Q
from .models import Video
import logging


logger = logging.getLogger(__name__)


class VideoListAPIView(generics.ListAPIView):
    " A class to list the videos in descending order, search in videos and sort by published date ,title."

    serializer_class = VideoSerializer
    pagination_class = VideoPagination    

    def get_queryset(self):
        
        """ For query: (ex:search=cricket)
            For page number (default page value is 1)(ex:page=3)
            For sort_by: (ex:sort_by=title)
            returns JSON Response
        """

        videos_list = []

        # Checking if query provided in GET request or not.
        if 'search' in self.request.GET:
            # if query provided, then storing the query in a vairable. 
            search_query = self.request.GET.get('search')
            # Retrieving the videos with the search query for the video title, description. 
            videos_list = Video.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
            logger.info("%s: Successfully fetched videos with search %s.",
                    self.__class__.__name__,
                    search_query)  
        else:
            # if there are no videos found with the search query, then taking all the videos.
            videos_list = Video.objects.all()
        
        # Checking if orderby provided or not.
        if 'orderby' in self.request.GET:
            # Get the orderby query provided by user
            orderby = self.request.GET.get('orderby')

            if orderby in ['-published_at', '-title','published_at', 'title']:
                videos_list = videos_list.order_by(orderby)
                logger.info("%s: Successfully fetched videos with order_by %s.",
                    self.__class__.__name__,
                    orderby)
                return videos_list
        
        # If orderby not provided then taking the videos in the descending order of their published date
        videos_list = videos_list.order_by('-published_at')
        logger.info("%s: Successfully fetched videos in the reverse chronological order.",self.__class__.__name__)
        return videos_list      