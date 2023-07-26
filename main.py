from googleapiclient.discovery import build
import webbrowser
import time
from playsound import playsound
import configparser
import os


class ConfigManager:
    def __init__(self, config_file_name: str = 'config.cfg'):
        self.config_file_name = config_file_name
        self.youtube_oauth_key = None
        self.youtube_upload_playlist_id = None
        self.url_to_open = None
        self.refresh_delay = None

    def _create(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'youtube_oauth_key': '', 'youtube_upload_playlist': '',
                             'url_to_open': '', 'refresh_delay': ''}
        with open(self.config_file_name, 'w+') as configfile:
            config.write(configfile)

    def _check_entries(self):
        config = configparser.ConfigParser()
        config.read(self.config_file_name)

        entries_with_empty_value = []
        for key, value in config['DEFAULT'].items():
            if not value.strip():
                entries_with_empty_value.append(key)

        return entries_with_empty_value

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file_name)

        self.youtube_oauth_key = config['DEFAULT']['youtube_oauth_key']
        self.youtube_upload_playlist_id = config['DEFAULT']['youtube_upload_playlist']
        self.url_to_open = config['DEFAULT']['url_to_open']
        self.refresh_delay = int(config['DEFAULT']['refresh_delay'])

    def run(self):
        try:
            if not os.path.exists(self.config_file_name) or os.path.getsize(self.config_file_name) == 0 \
                    or self._check_entries():
                self._create()
                return False
            self._read_config()
            return True
        except Exception as e:
            print(e)
            input("press enter to exit")
            exit(1)


class YoutubeManager:

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
            input("press enter to exit")
            exit(1)


if __name__ == '__main__':
    config_manager = ConfigManager()
    if not config_manager.run():
        print("config file is not correct or not exists")
        print("please fill in the config file at the following path: " + config_manager.config_file_name)
        input("press enter to exit")
        exit(1)
    print("config file is loaded successfully:")
    print("-----------------------------------")
    print("Youtube OAuth Key: " + config_manager.youtube_oauth_key)
    print("Youtube Upload Playlist ID: " + config_manager.youtube_upload_playlist_id)
    print("URL to open: " + config_manager.url_to_open)
    print("Refresh Delay: " + str(config_manager.refresh_delay))
    print("-----------------------------------")
    old_video_id = YoutubeManager.get_latest_video_id(config_manager.youtube_oauth_key,
                                                      config_manager.youtube_upload_playlist_id)
    while True:
        new_video_id = YoutubeManager.get_latest_video_id(config_manager.youtube_oauth_key,
                                                          config_manager.youtube_upload_playlist_id)
        if new_video_id != old_video_id:
            old_video_id = new_video_id
            print(f"{time.ctime()} / NEW VIDEO UPLOADED ALERT!")
            print(f"opening: https://www.youtube.com/watch?v={new_video_id}")
            webbrowser.open(f"https://www.youtube.com/watch?v={new_video_id}")
            webbrowser.open("https://eu.wargaming.net/shop/redeem/")
            playsound('notification_sound.mp3')
            input("press enter to continue")
        else:
            print(f"{time.ctime()} / video id is still the same ({new_video_id})")
        time.sleep(config_manager.refresh_delay)
