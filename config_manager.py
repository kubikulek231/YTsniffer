import configparser
import os
from enum import Enum


class ConfigDefaults(Enum):
    youtube_oauth_key = 'YOUR_OAUTH_KEY'
    youtube_upload_playlist_id = 'ID_OF_PLAYLIST_TO_SCAN'
    additional_url = 'ADDITIONAL_URL_TO_OPEN'
    play_sound_on_new_video = True
    open_new_video_url = False
    open_additional_url_on_new_video = False
    refresh_delay = 5


class ConfigManager:
    def __init__(self, config_file_name: str = 'config.cfg'):
        self.config_file_name = config_file_name
        self.oauth_key = None
        self.upload_playlist_id = None
        self.additional_url = None
        self.play_sound_on_new_video = None
        self.open_new_video_url = None
        self.open_additional_url_on_new_video = None
        self.refresh_delay = None

    def is_config_valid(self):
        cd = ConfigDefaults
        if self.oauth_key is None or cd.youtube_oauth_key.value == self.oauth_key:
            return False
        if self.upload_playlist_id is None or cd.youtube_upload_playlist_id.value == self.upload_playlist_id:
            return False
        if self.play_sound_on_new_video is None:
            return False
        if self.open_new_video_url is None:
            return False
        if self.open_additional_url_on_new_video is True:
            if self.additional_url is None:
                return False
            if self.additional_url == cd.additional_url.value:
                return False
        if self.refresh_delay is None or self.refresh_delay < 1:
            return False
        return True

    def _create(self):
        config = configparser.ConfigParser()
        config['CFG'] = {'youtube_oauth_key': ConfigDefaults.youtube_oauth_key.value,
                         'youtube_upload_playlist': ConfigDefaults.youtube_upload_playlist_id.value,
                         'additional_url': ConfigDefaults.additional_url.value,
                         'open_new_video_url': ConfigDefaults.open_new_video_url.value,
                         'open_additional_url_on_new_video': ConfigDefaults.open_additional_url_on_new_video.value,
                         'play_sound_on_new_video': ConfigDefaults.play_sound_on_new_video.value,
                         'refresh_delay': ConfigDefaults.refresh_delay.value}
        with open(self.config_file_name, 'w+') as configfile:
            config.write(configfile)

    def _check_entries(self):
        config = configparser.ConfigParser()
        config.read(self.config_file_name)

        entries_with_empty_value = []
        for key, value in config['CFG'].items():
            if not value.strip():
                entries_with_empty_value.append(key)

        return entries_with_empty_value

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file_name)

        self.oauth_key = config['CFG']['youtube_oauth_key']
        self.upload_playlist_id = config['CFG']['youtube_upload_playlist']
        self.refresh_delay = int(config['CFG']['refresh_delay'])
        self.play_sound_on_new_video = config['CFG']['play_sound_on_new_video']
        self.open_new_video_url = config['CFG']['open_new_video_url']
        self.open_additional_url_on_new_video = config['CFG']['open_additional_url_on_new_video']
        self.additional_url = config['CFG']['additional_url']

    def load(self):
        try:
            if not os.path.exists(self.config_file_name) or os.path.getsize(self.config_file_name) == 0 \
                    or self._check_entries():
                self._create()
                return False
            self._read_config()
            return True
        except Exception as e:
            print(e)
            input("Press enter to exit ...")
            exit(1)
