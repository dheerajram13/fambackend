
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import logging
from youtube.celery import app
from yt_api_keys.models import YotubeApiKey
from search.models import Video
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


    
def save_video_to_db(videos):
    """A function to iterate through the list of videos from the 
       input, saves them in the database and returns the counter of
       the videos inserted.
    """
    counter = 0
    # iteraring through the vide list from the given input.
    for item in videos:
        # checking if video already exists in the DB.
        video_in_db = Video.objects.filter(youtube_id=item['id']['videoId'])
        # if exists we can skip that iteration
        if video_in_db.exists():
            continue
        # save the video object in the DB.
        video = Video.objects.create(
                youtube_id = item['id']['videoId'],
                title = item['snippet']['title'],
                description = item['snippet']['description'],
                channel_title = item['snippet']['channelTitle'],
                thumbnail_url = item['snippet']['thumbnails']['medium']['url'],
                published_at = item['snippet']['publishedAt'],
            )
        # if video exists then increamenting the counter by 1.
        if video is not None:
            counter = counter + 1
    
    return counter

@app.task
def retrieve_data():
    """
        A task function by celery to retrieve the data from Youtube-v3 API 
        asynchronously for every 10 seconds with pre-defined search and sends 
        the videos data to save_video_to_db function to save the videos in DB.
    """

    logger.info("%s: Retrieving the new videos from the youtube API.",retrieve_data.__name__)  
    
    # Getting all the API keys from the DB.
    all_api_keys = YotubeApiKey.objects.all() 
    current_api_key_index = 0
    
    # checking if api keys exists in the DB or not.
    if all_api_keys.exists():
        # if exists taking the first youtube api key from the DB.
        current_api_key = all_api_keys.first().youtube_api_key
    else:
        # setting api key to None
        current_api_key = 'none'
    
    # Getting all videos from the DB and ordering the videos data in 
    # descending order of their published time
    videos_data = Video.objects.all().order_by('-published_at')

    if videos_data.exists():
        # getting the latest video publish time from the DB.
        published_after = videos_data.first().published_at.replace(tzinfo=None)
    else:
        # if there are no videos then setting it to 20 minutes before current time
        published_after = datetime.utcnow() - timedelta(minutes=20)

    # converting the date time to ISO format.
    published_after_iso = published_after.isoformat("T") + "Z"
    
    # setting a boolean field for data fetch to False
    data_retrieved  = False
    failed_api_calls = 0

    # creating an empty response if the api call fails
    response = {'items':[]}

    # while loop to iterate through the all the api keys
    while data_retrieved  == False:
        # setting the data fetched to true
        data_retrieved  = True
        logger.info("%s: Retrieving the data with index: %s and api key: %s",
                retrieve_data.__name__,
                current_api_key_index,
                current_api_key)  

        # building a youube v3 api service     
        try:
            service = build(
                'youtube',
                'v3',
                developerKey= current_api_key
            )
        # searching with the pre-defined keyword from service search list
            collection = service.search().list(
                maxResults=30,
                part=['id','snippet'],
                q='music',
                type='video',
                order='date',
                publishedAfter=published_after_iso
            )

            response = collection.execute()
        except HttpError as e:
            logger.error("%s Found error: %s",retrieve_data.__name__,e)
            # increamenting the api key index and failed api calls by 1 
            current_api_key_index = current_api_key_index + 1 
            failed_api_calls = failed_api_calls + 1

            # If the total api keys is less than the curr index, taking mod 
            current_api_key_index = (current_api_key_index+1) % len(list(all_api_keys))
            current_api_key = all_api_keys[current_api_key_index].youtube_api_key

            data_retrieved  = False       
        
        # if the failed api call equal to the length of the api ksys in the DB.
        if failed_api_calls == len(list(all_api_keys)):
            # breaking from the loop
            logger.info("%s:  Youtube API quota limit exceded with tries: %s ",
                retrieve_data.__name__,
                failed_api_calls)
            break

    logger.info("%s: Successfully retrieved %s items from youtube",
                retrieve_data.__name__,
                len(response['items']))

    #if the list contains items, then saving it in the DB. 
    if len(response['items']) > 0:
        videos_count = save_video_to_db(response['items'])
        logger.info("%s: Successfully saved %s videos.",
                retrieve_data.__name__,
                videos_count)

    return False
