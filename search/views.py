import requests
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render,redirect


# Create your views here.

def index(request):
    
    videos = []

    if request.method == 'POST':

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST["search"],
            'key':settings.YOUTUBE_DATA_API_KEY,
            'maxResults':9,
            'type':'video'
        }


        result = requests.get(search_url,search_params)
        results = result.json()['items']
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        
        if request.POST["submit"] == "lucky":
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')

        video_params = {
            'part': 'snippet,contentDetails',
            'key':settings.YOUTUBE_DATA_API_KEY,
            'id': ','.join(video_ids)

        }

        video_results = requests.get(video_url,video_params).json()['items']


        for result in video_results:

            video_data={
                'title':result['snippet']['title'],
                'id':result['id'],
                'url':f'https://www.youtube.com/watch?v={result["id"]}',
                'duration':int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbnail':result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)

    context = {
        'videos':videos
    }
    return render(request, 'search/index.html',context)