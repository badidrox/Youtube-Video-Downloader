prolly youtube changed smth and it no longer works lmao
# Youtube-Video-Downloader
A Python Application to download Youtube videos and playlists made mainly with pytube3 and tkinter

This Application uses [ffmpeg](https://ffmpeg.org/). 
The version provided with this Application is lisenced under [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

### OS Support:
Currently supports both Windows and Linux

### Core Features:
-Ability to automatically download a separate audio file and merge it with a video file in case the choosen resolution (480p for example) does not have audio channel included.

-Supports Playlist downloading .

-Support download for both mp4 and webm file extensions.

-Support resolutions from 144p to 2160p(4K).


## Instructions:
### How to Install:
##### Windows:
1- Download the zip file for ffmpeg from [Releases](https://github.com/badidrox/Youtube-Video-Downloader/releases)

2- Download the .exe File of Youtube Video Downloader from [Releases](https://github.com/badidrox/Youtube-Video-Downloader/releases)

3- Unzip the ffmpeg-folder.zip and make sure that the ffmpeg-folder and the .exe file are in the SAME directory.

4-Create a shortcut to the .exe file in the desktop and Enjoy!

Note that you do not need to download the ffmpeg-folder if you have ffmpeg already added to your PATH variable
You can also download the latest version of ffmpeg from [ffmpeg](https://ffmpeg.org/).
Simply make sure that ffmpeg is added to PATH variable or the folder is renamed to ffmpeg-folder + in the same directory as the .exe file

##### Ubuntu:
1- Install ffmpeg by running the following commands: 

`sudo apt update`

`sudo apt install ffmpeg`

2- Download the Youtube Video Downloader for linux from [Releases](https://github.com/badidrox/Youtube-Video-Downloader/releases)


### How to Use:

Open the Settings to change the default download directory or enable MP3 Conversion for Audio Downloads including playlists

Paste a Youtube video link for Video or Audio Download.

Note that there is a lot of video streams(different resolutions and channels) that Youtube uses and a lot of them do not have audio channel included in them.
This app can automatically download a separate audio file and merge both the video without audio and the audio file together to give you the desired resolution.

Paste a Playlist link for Playlist Download.

The playlist downloader is limited to only files who have both video and audio channels (usually 720p and 360p resolutions) + audio only option



