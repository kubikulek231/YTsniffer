from googleapiclient.discovery import build


class YoutubeManager:
    error_num = 0

    @staticmethod
    def get_channel_details(dev_key: str, channel_id: str):
        youtube = build('youtube', 'v3', developerKey=dev_key)
        request = youtube.channels().list(part='contentDetails', id=channel_id)
        response = request.execute()
        return response

    @staticmethod
    def get_playlist_details(dev_key: str, channel_id: str):
        youtube = build('youtube', 'v3', developerKey=dev_key)
        request = youtube.playlists().list(part='id', channelId=channel_id)
        response = request.execute()
        return response

    @staticmethod
    def get_playlist_items(dev_key: str, playlist_id: str):
        youtube = build('youtube', 'v3', developerKey=dev_key)
        request = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id)
        response = request.execute()
        return response

    @staticmethod
    def get_latest_video_id(dev_key: str, playlist_id: str):
        try:
            return YoutubeManager.get_playlist_items(dev_key, playlist_id)['items'][0]['contentDetails']['videoId']
        except Exception as e:
            print(e)
            YoutubeManager.error_num += 1
            if YoutubeManager.error_num == 10:
                input("Critical error, press enter to exit...")
                exit(1)
