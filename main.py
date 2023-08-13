import time
import webbrowser

from playsound import playsound

from config_manager import ConfigManager
from youtube_manager import YoutubeManager

if __name__ == '__main__':
    config_manager = ConfigManager()
    tag_cfg = f"{time.strftime('%H:%M:%S')} [CFG]: "
    spacer_cfg = " " * len(tag_cfg)

    if not config_manager.load():
        print("\n" + f"{tag_cfg}Config file is incorrect/unreadable or does not exist")
        print(f"{spacer_cfg}Please fill in the config file at the following path: " + config_manager.config_file_name)
        input(f"{spacer_cfg}Press enter to exit ...")
        exit(1)

    if not config_manager.is_config_valid():
        print("\n" + f"{tag_cfg}Entries in config file are incorrect")
        print(f"{spacer_cfg}Please fill in the config file at the following path: " + config_manager.config_file_name)
        input(f"{spacer_cfg}Press enter to exit ...")
        exit(1)

    print("\n" + f"{tag_cfg}Config file was loaded successfully:")
    print(f"{spacer_cfg}-----------------------------------")
    print(f"{spacer_cfg}Youtube OAuth key: " + config_manager.oauth_key)
    print(f"{spacer_cfg}Youtube upload playlist ID: " + config_manager.upload_playlist_id)
    print(f"{spacer_cfg}Play sound on new Video: " + str(config_manager.play_sound_on_new_video))
    print(f"{spacer_cfg}Open new video: " + str(config_manager.open_new_video_url))
    print(f"{spacer_cfg}Open additional URL on new video: " + str(config_manager.open_additional_url_on_new_video))
    print(f"{spacer_cfg}Additional URL to open: " + config_manager.additional_url)
    print(f"{spacer_cfg}Refresh delay: " + str(config_manager.refresh_delay) + " seconds")
    print(f"{spacer_cfg}-----------------------------------" + "\n")

    old_video_id = YoutubeManager.get_latest_video_id(config_manager.oauth_key,
                                                      config_manager.upload_playlist_id)
    while True:
        tag_run = f"{time.strftime('%H:%M:%S')} [YTS]: "
        spacer_run = " " * len(tag_run)

        new_video_id = YoutubeManager.get_latest_video_id(config_manager.oauth_key,
                                                          config_manager.upload_playlist_id)
        if new_video_id != old_video_id:
            old_video_id = new_video_id
            print(f"{tag_run}NEW VIDEO UPLOADED!")
            if config_manager.play_sound_on_new_video is True:
                print(f"{spacer_run}playing sound ...")
                playsound('notification_sound.mp3')
            if config_manager.open_new_video_url is True:
                print(f"{spacer_run}opening: https://www.youtube.com/watch?v={new_video_id}")
                webbrowser.open(f"https://www.youtube.com/watch?v={new_video_id}")
            if config_manager.open_additional_url_on_new_video is True:
                print(f"{spacer_run}opening: {config_manager.additional_url}")
                webbrowser.open(config_manager.additional_url)
            input("Press enter to continue ...")
        else:
            print(f"{tag_run}Video ID is still the same ({new_video_id})")
        time.sleep(config_manager.refresh_delay)
