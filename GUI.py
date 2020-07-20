from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from APPYoutubeVideoDownloader import *
from functools import partial
import threading
import subprocess
import sys
import time
import traceback


#disk full error missing
root = Tk()
root.title('Youtube Video Downloader')
if sys.platform == 'linux':
    root.geometry('660x820')
else:
    root.geometry('560x720')
root.resizable(False,True)
back_color = '#515151'
front_color = '#313131'
text_color = '#e5e7e9'

index_res = StringVar()
index_res.set('0')
file_extension = StringVar()
file_extension.set('mp4')

link = StringVar()
if sys.platform == 'win32':
    if not os.path.exists(os.path.expanduser('~')+'\\Documents\\YoutubeVideoDownloader'):
        os.mkdir(os.path.expanduser('~')+'\\Documents\\YoutubeVideoDownloader')
        if not os.path.exists(os.path.expanduser('~')+'\\Documents\\YoutubeVideoDownloader\\output_path.txt'):
            with open(os.path.expanduser('~')+'\\Documents\\YoutubeVideoDownloader\\output_path.txt','w') as f:
                f.write(os.path.expanduser('~')+'\\Downloads\\')
    else:
        if not os.path.exists(os.path.expanduser('~') + '\\Documents\\YoutubeVideoDownloader\\output_path.txt'):
            with open(os.path.expanduser('~') + '\\Documents\\YoutubeVideoDownloader\\output_path.txt', 'w') as f:
                f.write(os.path.expanduser('~') + '\\Downloads\\')
elif sys.platform == 'linux':
    if not os.path.exists(os.path.expanduser('~')+'/YoutubeVideoDownloader'):
        os.mkdir(os.path.expanduser('~')+'/YoutubeVideoDownloader')
        if not os.path.exists(os.path.expanduser('~')+'/YoutubeVideoDownloader/output_path.txt'):
            with open(os.path.expanduser('~')+'/YoutubeVideoDownloader/output_path.txt','w') as f:
                f.write(os.path.expanduser('~')+'/Downloads/')
    else:
        if not os.path.exists(os.path.expanduser('~') + '/YoutubeVideoDownloader/output_path.txt'):
            with open(os.path.expanduser('~') + '/YoutubeVideoDownloader/output_path.txt', 'w') as f:
                f.write(os.path.expanduser('~') + '/Downloads/')


def pressVideoTab():
    video_tab['state'] = DISABLED
    video_tab['bg'] = '#212121'

    audio_tab['state'] = NORMAL
    audio_tab['bg'] = front_color

    audio_download_frame.pack_forget()
    video_download_frame.pack(expand=True, fill='both')



def pressAudioTab():
    audio_tab['state'] = DISABLED
    audio_tab['bg'] = '#212121'


    video_tab['state'] = NORMAL
    video_tab['bg'] = front_color

    video_download_frame.pack_forget()
    audio_download_frame.pack(expand=True, fill='both')


def remove_signs(string):  # this removes signs that doesnt work with file names and spaces to make it work always
    newstring = ''
    for char in string:
        if char in '\/<>*:?"|':
            char=' '
        newstring = newstring + char
    return newstring



def videoDownloadButtonThreaded(i):

    def videoDownloadButton(i):
        res_list = []
        for res,stream in app.video_streams_dict.items():
            res_list.append(res)
        app.desired_stream = app.video_streams_dict[res_list[i]]
        app.filesize = app.desired_stream.filesize
        if app.desired_stream.is_progressive:
            global progress_window
            progress_window = Toplevel()
            progress_window.transient(root)
            progress_window.focus_set()
            def deleteProgressWindow():
                enableAll()
                progress_window.destroy()
            progress_window.protocol("WM_DELETE_WINDOW",deleteProgressWindow)
            disableAll()
            progress_window.title("Video Download Progress Bar")
            progress_window.geometry('400x75')
            progress_window.resizable(False, False)
            progress_window.configure(bg='#212121')
            progress_label = Label(progress_window, text='Video Progress:'
                                   , bg='#212121', fg=text_color, font='TkFixedFont 14')
            progress_label.pack()
            global progress
            progress = Progressbar(progress_window, orient=HORIZONTAL, length=100, mode='determinate')
            progress.pack(fill = 'both')
            empty_frame4 = Frame(progress_window, bg=back_color, height=25)
            empty_frame4.pack()
            global percent_label
            global speed_label
            percent_label = Label(empty_frame4, text='    0%'
                                  , bg='#212121', fg=text_color, font='TkFixedFont 14')
            speed_label = Label(empty_frame4, text='0 KB/s    '
                                , bg='#212121', fg=text_color, font='TkFixedFont 14')
            speed_label.grid(row=0, column=0)
            percent_label.grid(row=0, column=1)
            try:
                app.download(app.desired_stream)
            except Exception as e:
                deleteProgressWindow()
                if e.__str__() == "<urlopen error [Errno 11001] getaddrinfo failed>":
                    errorWindow('Network Error:\nCheck Your Internet Connection\n')
                else:
                    print(e)
                    traceback.print_exc()
                return
            try:
                os.rename(app.downloaded_path, app.output_path + remove_signs(app.video_title) +'.'+file_extension.get())
            except:
                os.remove(app.output_path + remove_signs(app.video_title) +'.'+file_extension.get())
                os.rename(app.downloaded_path, app.output_path + remove_signs(app.video_title) +'.'+file_extension.get())
            progress_window.destroy()
            finishedWindow('Download Finished', ' Your Download is Complete',file_extension.get())
            enableAll()
        elif not app.desired_stream.is_progressive:
            infoPopup()



    thread = threading.Thread(target=partial(videoDownloadButton,i))
    thread.daemon = True
    thread.start()

def audioDownloadButtonThreaded(j):
    def audioDownloadButton(j):

        def deleteProgressWindow():
            enableAll()
            progress_window.destroy()
        global progress_window
        progress_window = Toplevel()
        progress_window.focus_set()
        progress_window.transient(root)
        progress_window.protocol("WM_DELETE_WINDOW", deleteProgressWindow)
        disableAll()
        progress_window.title("Audio Download Progress Bar")
        progress_window.geometry('400x75')
        progress_window.resizable(False, False)
        progress_window.configure(bg='#212121')
        progress_label2 = Label(progress_window, text='Audio Progress:'
                                , bg='#212121', fg=text_color, font='TkFixedFont 14')

        progress_label2.pack()
        global progress
        progress = Progressbar(progress_window, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(fill = 'both')
        empty_frame4 = Frame(progress_window, bg=back_color, height=25)
        empty_frame4.pack()
        global percent_label
        global speed_label
        percent_label = Label(empty_frame4, text='    0%'
                              , bg='#212121', fg=text_color, font='TkFixedFont 14')
        speed_label = Label(empty_frame4, text='0 KB/s    '
                            , bg='#212121', fg=text_color, font='TkFixedFont 14')
        speed_label.grid(row=0, column=0)
        percent_label.grid(row=0, column=1)
        abr_list = [] #abr stands for audio bit rate
        for abr, stream in app.audio_streams_dict.items():
            abr_list.append(abr)
        app.filesize = app.audio_streams_dict[abr_list[j]].filesize
        try:
            app.download(app.audio_streams_dict[abr_list[j]])
        except Exception as e:
            deleteProgressWindow()
            if e.__str__() == "<urlopen error [Errno 11001] getaddrinfo failed>":
                errorWindow('Network Error:\nCheck Your Internet Connection\n')
            else:
                print(e)
                traceback.print_exc()
            return
        try:
            os.rename(app.downloaded_path,app.output_path + remove_signs(app.video_title) + '.' + file_extension.get())
        except:
            os.remove(app.output_path + remove_signs(app.video_title) + '.' + file_extension.get())
            os.rename(app.downloaded_path,app.output_path + remove_signs(app.video_title) + '.' + file_extension.get())
        progress_window.destroy()
        enableAll()
        finishedWindow('Download Finished', ' Your Download is Complete',file_extension.get())
    thread = threading.Thread(target=partial(audioDownloadButton,j))
    thread.daemon = True
    thread.start()


def downloadProgress(chunk, file_handle,remaining):

    if app.n == 0:
        app.time1 = time.time()
        app.old_remaining = remaining


    app.download_percent = round((1 - remaining / app.filesize) * 100, 3)
    progress['value'] = app.download_percent
    percent_label.configure(text="    "+str(app.download_percent).split(".")[0] + "%")




    app.n+=1
    if app.n==100:
        app.time2 = time.time()
        app.download_speed = round((app.old_remaining - remaining)/1000/(app.time2-app.time1),2)
        app.n=0


        if len(str(app.download_speed).split(".")[0])>3:
            unit = "MB/s"
            number = str(app.download_speed/1000).split(".")[0]
            if app.download_speed<=0:
                number = "0"
        else:
            unit = "KB/s"
            number =  str(app.download_speed).split(".")[0]
            if app.download_speed<=0:
                number = "0"
        speed_str = number + unit + "    "
        speed_label.configure(text = speed_str)

def downloadComplete(stream,file_path):
    app.download_percent = 0
def downloadProgress2(chunk, file_handle,remaining):
    if app.n == 0:
        app.time1 = time.time()
        app.old_remaining = remaining
    app.download_percent = round((1 - remaining / app.filesize) * 100, 3)
    progress2['value'] = app.download_percent
    percent_label.configure(text="    "+str(app.download_percent).split(".")[0] + "%")
    app.n+=1
    if app.n==100:
        app.time2 = time.time()
        app.download_speed = round((app.old_remaining - remaining)/1000/(app.time2-app.time1),2)
        app.n=0
        if len(str(app.download_speed).split(".")[0])>3:
            unit = "MB/s"
            number = str(app.download_speed/1000).split(".")[0]
            if app.download_speed<=0:
                number = "0"
        else:
            unit = "KB/s"
            number =  str(app.download_speed).split(".")[0]
            if app.download_speed<=0:
                number = "0"
        speed_str = number + unit + "    "
        speed_label.configure(text = speed_str)

def downloadComplete2(stream,file_path):
    merging_label.pack()
def downloadProgress3(chunk, file_handle,remaining):

    if playlist.n == 0:
        playlist.time1 = time.time()
        playlist.old_remaining = remaining


    playlist.download_percent = round((1 - remaining / playlist.filesize) * 100, 3)
    progress['value'] = playlist.download_percent
    percent_label.configure(text="    "+str(playlist.download_percent).split(".")[0] + "%")




    playlist.n+=1
    if playlist.n==100:
        playlist.time2 = time.time()
        playlist.download_speed = round((playlist.old_remaining - remaining)/1000/(playlist.time2-playlist.time1),2)
        playlist.n=0


        if len(str(playlist.download_speed).split(".")[0])>3:
            unit = "MB/s"
            number = str(playlist.download_speed/1000).split(".")[0]
            if playlist.download_speed<=0:
                number = "0"
        else:
            unit = "KB/s"
            number =  str(playlist.download_speed).split(".")[0]
            if playlist.download_speed<=0:
                number = "0"
        speed_str = number + unit + "    "
        speed_label.configure(text = speed_str)

def downloadComplete3(stream,file_path):
    playlist.k += 1
    if playlist.k+1 < playlist.video_count or playlist.k+1 == playlist.video_count:
        progress_label.configure(text = f'Progress: {str(playlist.k + 1)}/{str(playlist.video_count)}')
        video_title_label.configure(text=f'Video = {next(playlist.video_titles)}')
    else:
        playlist_window.destroy()
        enableAll()
        def finishedWindow2(title, text):
            finished_window = Toplevel()
            finished_window.title(title)
            finished_window.configure(bg='#212121')
            finished_window.resizable(False, False)

            def openDownloadFolder():
                finished_window.destroy()
                if sys.platform == "win32":
                    os.startfile(playlist.output_path + '\\'+remove_signs(playlist.playlist_title))
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, playlist.output_path + '\\'+remove_signs(self.playlist_title)])

            label = Label(finished_window, text=text
                          , bg='#212121', fg=text_color, font='TkFixedFont 16')
            finished_button_frame = Frame(finished_window, bg='#212121')

            finished_button_done = Button(finished_button_frame, text='Done', bg=front_color,
                                          activebackground='#616161', activeforeground=text_color,
                                          fg=text_color,
                                          borderwidth=0, highlightthickness=0, font='TkFixedFont 16',
                                          command=finished_window.destroy)
            finished_button_open_folder = Button(finished_button_frame, text='Open Folder', bg=front_color,
                                                 activebackground='#616161', activeforeground=text_color,
                                                 fg=text_color,
                                                 borderwidth=0, highlightthickness=0, font='TkFixedFont 16',
                                                 command=openDownloadFolder)

            label.pack()
            finished_button_frame.pack()
            finished_button_done.grid(row=1, column=0, sticky='we')
            finished_button_open_folder.grid(row=1, column=1, sticky='we')

        finishedWindow2('Playlist Download Finished' , 'Your playlist download has completed')
def displayVideoStreams():
    i = 0
    app.resetVideoLists()
    for resolution, stream in app.video_streams_dict.items():
        filesize = str(stream.filesize / 1_000_000)[:5] + 'MB'
        video_download_label = Label(video_download_frame, text=f'Filesize = {filesize}  Resolution = {resolution}  '
                                     , bg='#212121', fg=text_color, font='TkFixedFont 16')

        video_download_button = Button(video_download_frame, text='Download', bd=0, highlightthickness=0,
                                       bg=front_color, fg=text_color,
                                       activeforeground=text_color, activebackground=front_color,state = DISABLED,
                                       command=partial(videoDownloadButtonThreaded, i),font = 'TkFixedFont 14')

        app.video_buttons_list.append(video_download_button)
        app.video_labels_list.append(video_download_label)
        video_download_label.grid(row=i + 1, column=0, sticky='w', pady=10)
        video_download_button.grid(row=i + 1, column=1, sticky='e', pady=10)
        i += 1


def displayAudioStreams():
    j = 0
    app.resetAudioLists()
    for abr, stream in app.audio_streams_dict.items():
        filesize = str(stream.filesize / 1000000)[:4] + 'MB'
        audio_file_extension = stream.__str__().split()[2].split('/')[1][:-1]
        audio_download_label = Label(audio_download_frame,
                                     text=f'Filesize = {filesize}           BitRate = {abr}     '
                                     , bg='#212121', fg=text_color, font='TkFixedFont 16')
        audio_download_button = Button(audio_download_frame, text='Download', bd=0, highlightthickness=0,
                                       bg=front_color, fg=text_color,state = DISABLED,
                                       activeforeground=text_color, activebackground=front_color,font = 'TkFixedFont 14'
                                       ,command=partial(audioDownloadButtonThreaded, j))

        app.audio_buttons_list.append(audio_download_button)
        app.audio_labels_list.append(audio_download_label)
        audio_download_label.grid(row=j + 1, column=0, sticky='w', pady=10)
        audio_download_button.grid(row=j + 1, column=1, sticky='e', pady=10)

        j += 1
def getLink():  #THE FUNCTION THAT START IT ALL
    link.set(search_entry.get())
    if not '/playlist?list=' in link.get():
        try:
            loading_window = Toplevel()
            loading_window.title('!')
            disableAll()
            loading_window.configure(bg='#212121')
            loading_window.resizable(False, False)
            loading_window.focus_set()
            loading_window.transient(root)
            loading_label = Label(loading_window, text='Loading...'
                                             ,bg = '#212121' , fg = text_color ,
                                  font = 'TkFixedFont 14')
            loading_label.grid(row=0,column=0,ipadx = 10,ipady=10)
            def deleteLoadingWindow():
                enableAll()
                loading_window.destroy()


            loading_window.protocol("WM_DELETE_WINDOW", deleteLoadingWindow)
            global app
            app = YoutubeVideoDownloader(link.get(),downloadProgress,downloadComplete,downloadProgress2,downloadComplete2)
            app.resetAudioStreamsDict()
            app.resetVideoStreamsDict()
            title = app.video_title
            title_label = Message(video_download_frame, text=f'Title = {title}'
                                             ,bg = '#212121' , fg = text_color ,
                                  font = 'TkFixedFont 14',width = 500,justify = CENTER)
            title_label.grid(row = 0 , column = 0 , columnspan = 2 , sticky = 'w')

            title_label_2 = Message(audio_download_frame, text=f'Title = {title}'
                                            ,bg='#212121', fg=text_color,
                                  font='TkFixedFont 14',width = 500,justify=CENTER)
            title_label_2.grid(row=0, column=0, columnspan=2, sticky='w')

            app.getVideoStreams()
            app.applyFilterVideo(file_extension.get())
            displayVideoStreams()
            app.getAudioOnlyStreams()
            app.applyFilterAudio(file_extension.get())
            displayAudioStreams()
            deleteLoadingWindow()
        except Exception as e:
            deleteLoadingWindow()
            if e.__str__() == 'regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*':
                errorWindow("Invalid Youtube Link\n")
            elif e.__str__() == '<urlopen error [Errno 11001] getaddrinfo failed>':
                errorWindow('Network Error:\nCheck Your Internet Connection\n')
            else:
                traceback.print_exc()
                print(e)
            return
    else:
        try:
            global playlist
            playlist = PlaylistDownloader(link.get(),downloadProgress3,downloadComplete3)
            if not playlist.video_count == 0:
                global playlist_window
                playlist_window = Toplevel()
                playlist_window.title('Playlist Downloader')
                disableAll()
                playlist_window.configure(bg='#212121')
                playlist_window.geometry('500x300')
                playlist_window.resizable(False, False)
                playlist_window.focus_set()
                playlist_window.transient(root)

                def deletePlaylistWindow():
                    enableAll()
                    playlist_window.destroy()


                playlist_window.protocol("WM_DELETE_WINDOW", deletePlaylistWindow)

                i = index_res
                empty_frame6 = Frame(playlist_window, bg="#212121", height=10)
                empty_frame7 = Frame(playlist_window, bg="#212121", height=10)


                resolution_label = Label(empty_frame6, text='Resolution : '
                                        , bg='#212121', fg=text_color, font='TkFixedFont 14')
                res1 = Radiobutton(empty_frame6, text='720p', variable=i, value='0', bg='#212121', fg=text_color,
                                 activeforeground=text_color, activebackground=front_color, highlightthickness=0,
                                 selectcolor='#212121', font='TkFixedFont 14')
                res2 = Radiobutton(empty_frame6, text='360p', variable=i, value='1', bg='#212121', fg=text_color,
                                 activeforeground=text_color, activebackground=front_color, highlightthickness=0,
                                 selectcolor='#212121', font='TkFixedFont 14')
                audio = Radiobutton(empty_frame6, text='Audio', variable=i, value='audio', bg='#212121', fg=text_color,
                                 activeforeground=text_color, activebackground=front_color, highlightthickness=0,
                                 selectcolor='#212121', font='TkFixedFont 14')
                def downloadPlaylistThreaded():

                    def downloadPlaylist():
                        start_button['state'] = DISABLED
                        try:

                            playlist.downloadPlaylist(i.get())
                        except Exception as e:
                            if e.__str__() == "<urlopen error [Errno 11001] getaddrinfo failed>":
                                errorWindow('Network Error:\nCheck Your Internet Connection\n')
                                deletePlaylistWindow()

                            else:
                                print(e)
                                traceback.print_exc()
                            return
                    thread = threading.Thread(target=downloadPlaylist)
                    thread.daemon = True
                    thread.start()


                start_button = Button(playlist_window, text='Start', bd=0, highlightthickness=0,
                                               bg=front_color, fg=text_color,
                                               activeforeground=text_color, activebackground=front_color,
                                               font='TkFixedFont 14', command = downloadPlaylistThreaded)

                empty_frame6.pack()
                empty_frame7.pack()
                # empty_frame8.pack()


                resolution_label.grid(row=0, column=0)
                res1.grid(row=0,column=1)
                res2.grid(row=0, column=2)
                audio.grid(row=0,column = 3)
                playlist_title_label = Message(playlist_window, text=f'Playlist = {playlist.playlist_title}'
                                      , bg='#212121', fg=text_color,
                                      font='TkFixedFont 14', width=350, justify=CENTER)
                playlist_title_label.pack()
                global video_title_label
                video_title_label = Message(playlist_window, text=f'Video = {next(playlist.video_titles)}'
                                      , bg='#212121', fg=text_color,
                                      font='TkFixedFont 14', width=350, justify=CENTER)
                video_title_label.pack()
                global progress_label
                progress_label = Label(playlist_window, text=f'Progress: {str(playlist.k+1)}/{str(playlist.video_count)}'
                                       , bg='#212121', fg=text_color, font='TkFixedFont 14')
                progress_label.pack()
                global progress
                progress = Progressbar(playlist_window, orient=HORIZONTAL, length=100, mode='determinate')
                progress.pack(fill='both')
                empty_frame9 = Frame(playlist_window, bg="#212121", height=10)
                empty_frame9.pack()
                global percent_label
                global speed_label
                percent_label = Label(empty_frame9, text='    0%'
                                      , bg='#212121', fg=text_color, font='TkFixedFont 14')
                speed_label = Label(empty_frame9, text='0 KB/s    '
                                    , bg='#212121', fg=text_color, font='TkFixedFont 14')
                speed_label.grid(row=0, column=0)
                percent_label.grid(row=0, column=1)
                start_button.pack()
            else:
                errorWindow("Playlist is private or Invalid Link\n")
        except Exception as e:
            if e.__str__() ==  "KeyError: 'list'":
                errorWindow("Invalid Playlist Link\n")
            elif e.__str__() == "<urlopen error [Errno 11001] getaddrinfo failed>":
                errorWindow('Network Error:\nCheck Your Internet Connection\n')
            else:
                traceback.print_exc()
                print(e)
            return

def getLinkThreaded(*event_info):
    thread = threading.Thread(target=getLink)
    thread.daemon = True
    thread.start()

def unpackAll():
    for lbl in app.video_labels_list:
        lbl.destroy()
    for btn in app.video_buttons_list:
        btn.destroy()
    for lbl in app.audio_labels_list:
        lbl.destroy()
    for btn in app.audio_buttons_list:
        btn.destroy()
def disableAll():
    try:
        for btn in app.video_buttons_list:
            btn['state'] = DISABLED
        for btn in app.audio_buttons_list:
            btn['state'] = DISABLED
    except:
        pass
    search_button['state'] = DISABLED
    r1['state'] = DISABLED
    r2['state'] = DISABLED
    search_entry['state'] = DISABLED
    refresh_button['state'] = DISABLED
    settings_button['state'] = DISABLED
def enableAll():
    try:
        for btn in app.video_buttons_list:
            btn['state'] = NORMAL
        for btn in app.audio_buttons_list:
            btn['state'] = NORMAL
    except:
        pass
    search_button['state'] = NORMAL
    r1['state'] = NORMAL
    r2['state'] = NORMAL
    search_entry['state'] = NORMAL
    refresh_button['state'] = NORMAL
    settings_button['state'] = NORMAL


def redisplayStreams():
    unpackAll()
    app.resetAudioStreamsDict()
    app.resetVideoStreamsDict()
    app.applyFilterVideo(file_extension.get())
    app.applyFilterAudio(file_extension.get())
    displayVideoStreams()
    displayAudioStreams()
    enableAll()
def redisplayStreamsThreaded(*event_info):
    thread = threading.Thread(target=redisplayStreams)
    thread.daemon = True
    thread.start()




def finishedWindow(title, text,format):
    finished_window = Toplevel()
    finished_window.title(title)
    finished_window.configure(bg = '#212121')
    finished_window.resizable(False, False)
    finished_window.geometry('500x125')
    finished_window.focus_set()
    finished_window.transient(root)

    def openDownloadFolder():
        finished_window.destroy()
        if sys.platform == "win32":
            os.startfile(app.output_path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, app.output_path])
    def openFile():
        finished_window.destroy()
        if sys.platform == "win32":
            os.startfile(app.output_path + remove_signs(app.video_title)+'.'+format)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, app.output_path + remove_signs(app.video_title)+'.'+format])
    label = Label(finished_window, text=text
                  , bg='#212121', fg=text_color, font='TkFixedFont 16')
    finished_button_frame = Frame(finished_window, bg='#212121')

    finished_button_done = Button(finished_button_frame, text='Done', bg=front_color,activebackground = '#616161' , activeforeground = text_color, fg=text_color,
                                  borderwidth=0, highlightthickness=0, font='TkFixedFont 16',
                                  command=finished_window.destroy)
    finished_button_open_folder = Button(finished_button_frame, text='Open Folder', bg=front_color,activebackground = '#616161' , activeforeground = text_color, fg=text_color,
                                         borderwidth=0, highlightthickness=0, font='TkFixedFont 16',
                                         command=openDownloadFolder)
    finished_button_open_file = Button(finished_button_frame, text='Open File', bg=front_color,activebackground = '#616161' , activeforeground = text_color, fg=text_color,
                                         borderwidth=0, highlightthickness=0, font='TkFixedFont 16',
                                         command=openFile)
    label.pack()
    finished_button_frame.pack()
    finished_button_done.grid(row=1, column=0, sticky='we',ipady=10)
    finished_button_open_folder.grid(row=1, column=1, sticky='we',ipady=10)
    finished_button_open_file.grid(row=1,column=2,sticky='we',ipady=10)



def infoPopup():
    disableAll()
    def yesButtonThreaded():
        def yesButton():
            info_popup.destroy()
            global progress_window
            progress_window = Toplevel()
            progress_window.focus_set()
            progress_window.transient(root)
            def deleteProgressWindow():
                enableAll()
                progress_window.destroy()
            progress_window.protocol("WM_DELETE_WINDOW", deleteProgressWindow)
            progress_window.title("Video Download Progress Bar")
            progress_window.geometry('400x150')
            progress_window.resizable(False, False)
            progress_window.configure(bg='#212121')

            progress_label = Label(progress_window, text='Video Progress:'
                          ,bg = '#212121' , fg = text_color,font='TkFixedFont 14')
            progress_label.pack()
            global progress
            progress = Progressbar(progress_window, orient=HORIZONTAL, length=100, mode='determinate')
            progress.pack(fill='both')

            progress_label2 = Label(progress_window, text='Audio Progress:'
                                   , bg='#212121', fg=text_color, font='TkFixedFont 14')

            progress_label2.pack()
            global progress2
            progress2 = Progressbar(progress_window, orient=HORIZONTAL, length=100, mode='determinate')
            progress2.pack(fill='both')
            empty_frame4 = Frame(progress_window, bg=back_color, height=25)
            empty_frame4.pack()
            global percent_label
            global speed_label
            percent_label = Label(empty_frame4, text='    0%'
                                   , bg='#212121', fg=text_color, font='TkFixedFont 14')
            speed_label = Label(empty_frame4, text='0 KB/s    '
                                   , bg='#212121', fg=text_color, font='TkFixedFont 14')
            speed_label.grid(row=0, column=0)
            percent_label.grid(row=0,column=1)
            global merging_label
            merging_label = Label(progress_window, text='Merging...'
                                  , bg='#212121', fg=text_color, font='TkFixedFont 14')

            try:
                app.download(app.desired_stream)
            except Exception as e:
                deleteProgressWindow()
                if e.__str__() == "<urlopen error [Errno 11001] getaddrinfo failed>":
                    errorWindow('Network Error:\nCheck Your Internet Connection\n')
                else:
                    print(e)
                    traceback.print_exc()

                return
            try:
                app.downloadAudioDirectly()
            except Exception as e:
                deleteProgressWindow()
                if e.__str__() == "<urlopen error [Errno 11001] getaddrinfo failed>":
                    errorWindow('Network Error:\nCheck Your Internet Connection\n')
                else:
                    print(e)
                    traceback.print_exc()
                return
            try:
                app.mergeVideoAudio(app.output_path+'/video.'+file_extension.get() , app.output_path+'/audio.mp4')
                merging_label.configure(text='Done')
            except:
                errorWindow("FFMPEG was not found on your pc.\nPlease make sure :\nFFMPEG is in the same directory as the program.\n")
                deleteProgressWindow()
                return

            try:
                os.rename(app.merge_output, app.output_path + remove_signs(app.video_title) + '.mp4')
            except:
                os.remove(app.output_path + remove_signs(app.video_title) + '.mp4')
                os.rename(app.merge_output, app.output_path  + remove_signs(app.video_title) + '.mp4')

            deleteProgressWindow()
            finishedWindow('Download and Merging Finished' , 'Your Download and Merging is complete','mp4')
        thread = threading.Thread(target=yesButton)
        thread.daemon = True
        thread.start()

    def noButtonThreaded():
        def noButton():
            info_popup.destroy()
            def deleteProgressWindow():
                enableAll()
                progress_window.destroy()
            global progress_window
            progress_window = Toplevel()
            progress_window.transient(root)
            progress_window.focus_set()
            progress_window.protocol("WM_DELETE_WINDOW", deleteProgressWindow)
            progress_window.title("Video Download Progress Bar")
            progress_window.geometry('400x75')
            progress_window.resizable(False,False)
            progress_window.configure(bg='#212121')
            progress_label = Label(progress_window, text='Video Progress:'
                                   , bg='#212121', fg=text_color, font='TkFixedFont 14')
            progress_label.pack()
            global progress
            progress = Progressbar(progress_window, orient=HORIZONTAL, length=100, mode='determinate')
            progress.pack(fill='both')
            empty_frame4 = Frame(progress_window, bg=back_color, height=25)
            empty_frame4.pack()
            global percent_label
            global speed_label
            percent_label = Label(empty_frame4, text='    0%'
                                  , bg='#212121', fg=text_color, font='TkFixedFont 14')
            speed_label = Label(empty_frame4, text='0 KB/s    '
                                , bg='#212121', fg=text_color, font='TkFixedFont 14')
            speed_label.grid(row=0, column=0)
            percent_label.grid(row=0, column=1)

            try:
                app.download(app.desired_stream)
            except Exception as e:
                deleteProgressWindow()
                if e.__str__() == "<urlopen error [Errno 11001] getaddrinfo failed>":
                    errorWindow('Network Error:\nCheck Your Internet Connection\n')
                else:
                    print(e)
                    traceback.print_exc()
            try:
                os.rename(app.downloaded_path,app.output_path + remove_signs(app.video_title) + '.' + file_extension.get())
            except:
                os.remove(app.output_path  + remove_signs(app.video_title) + '.' + file_extension.get())
                os.rename(app.downloaded_path,app.output_path  + remove_signs(app.video_title) + '.' + file_extension.get())
            progress_window.destroy()
            finishedWindow('Download Finished' ,' Your Download is Complete',file_extension.get())
            enableAll()
        thread = threading.Thread(target=noButton)
        thread.daemon = True
        thread.start()

    def deleteInfoPopupWindow():
        enableAll()
        info_popup.destroy()
    info_popup = Toplevel()
    info_popup.transient(root)
    info_popup.focus_set()
    info_popup.protocol("WM_DELETE_WINDOW",deleteInfoPopupWindow)
    info_popup.title("!")
    info_popup.configure(bg = '#212121')
    download_size = (app.desired_stream.filesize + app.audio_stream.filesize)/ 1_000_000
    info_label = Label(info_popup,text = f'This video format does not include audio.\n The app can automatically download a separate audio file and merge them together.\n This process will take longer time.\nThe download size will become {str(download_size)[:5]}MB\nDo you wish to do this?',
                       fg = text_color ,bg = '#212121',font = 'TkFixedFont 14')
    info_label.pack()
    info_popup.resizable(False,False)
    info_button_frame = Frame(info_popup , bg = '#212121')
    info_button_frame.pack()
    info_button_yes = Button(info_button_frame,text = 'Yes' , bg = front_color , fg = text_color ,activebackground = '#616161' , activeforeground = text_color,
                             borderwidth=0, highlightthickness = 0,font = 'TkFixedFont 16',command = yesButtonThreaded)
    info_button_no = Button(info_button_frame,text = 'No' , bg = front_color , fg = text_color ,activebackground = '#616161' , activeforeground = text_color,
                             borderwidth=0, highlightthickness = 0,font = 'TkFixedFont 16', command = noButtonThreaded)
    info_button_cancel = Button(info_button_frame, text='Cancel', bg=front_color, fg=text_color,activebackground = '#616161' , activeforeground = text_color,
                            borderwidth=0, highlightthickness=0,font = 'TkFixedFont 16',command = deleteInfoPopupWindow)

    info_button_no.grid(row=1, column=0,sticky = 'e')
    info_button_cancel.grid(row=1, column=1 ,sticky = 'we')
    info_button_yes.grid(row=1, column=2 , sticky = 'w')
def errorWindow(error_message):
    error_window = Toplevel()
    error_window.transient(root)
    error_window.focus_set()
    error_window.title("!")
    error_window.configure(bg='#212121')
    error_window.geometry('500x100')
    error_label = Label(error_window, text=error_message
                               , bg='#212121', fg=text_color, font='TkFixedFont 14')
    error_label.pack()
    ok_button=Button(error_window, text = '   Ok   ',bd = 0 , fg = text_color , highlightthickness=0,
                       bg = front_color,activebackground = '#414141' , activeforeground = text_color,
                     font = 'TkFixedFont 14', command = error_window.destroy)
    ok_button.pack()
def settingsWindow():
    # def applyButton():
    #     path = default_path_entry.get()
    #     if  os.path.exists(path):

    #         settings_window.destroy()
    #     else:
    #         errorWindow("The directory does not exist. Please make one")
    def browseButton():
        path = filedialog.askdirectory(parent = root , initialdir = os.path.expanduser('~'))
        print(repr(path))
        if not path =='' and not path == ():
            if sys.platform =='linux':
                if not path == '/':
                    path = path + '/'
                with open(os.path.expanduser('~') + '/YoutubeVideoDownloader/output_path.txt', 'w') as f:
                    f.write(path)
            else:
                if not path == '\\':
                    path = path + '\\'
                with open(os.path.expanduser('~') + '\\Documents\\YoutubeVideoDownloader\\output_path.txt', 'w') as f:
                    f.write(path)
            try:
                app.output_path=path
            except:
                pass
            default_path_entry['state'] = NORMAL
            default_path_entry.delete(0,len(default_path_entry.get()))
            default_path_entry.insert(0,path)
            default_path_entry['state'] = DISABLED
    settings_window = Toplevel()
    settings_window.transient(root)
    settings_window.focus_set()
    settings_window.configure(bg='#212121')
    settings_window.geometry('500x100')
    default_path_label = Label(settings_window, text='Download Path : '
                                     , bg='#212121', fg=text_color, font='TkFixedFont 14')
    default_path_label.pack()
    default_path_frame = Frame(settings_window,bg="#212121",height = 50)
    default_path_entry = Entry(default_path_frame ,fg = front_color,bg = text_color , highlightcolor = front_color,bd = 0,disabledforeground = front_color)

    if sys.platform =='linux':
        with open(os.path.expanduser('~') + '/YoutubeVideoDownloader/output_path.txt', 'r') as f:
            path = f.read().strip()
    else:
        with open(os.path.expanduser('~') + '\\Documents\\YoutubeVideoDownloader\\output_path.txt', 'r') as f:
            path = f.read().strip()
    default_path_entry.insert(0,path)
    default_path_entry['state'] = DISABLED
    default_path_frame.grid_columnconfigure(0, weight=8)
    default_path_frame.grid_columnconfigure(1, weight=1)
    default_path_frame.pack(fill ='x')
    default_path_entry.grid(row=0,column=0,sticky = 'nsew')
    # apply_button=Button(default_path_frame , text = 'Apply',bd = 0 , fg = text_color , highlightthickness=0,
    #                    bg = front_color,activebackground = '#414141' , activeforeground = text_color,font = 'TkFixedFont 14', command = applyButton)
    # apply_button.grid(row = 0 , column = 1,sticky = 'nsew')
    browse_button=Button(default_path_frame , text = 'Browse',bd = 0 , fg = text_color , highlightthickness=0,
                       bg = front_color,activebackground = '#414141' , activeforeground = text_color,font = 'TkFixedFont 14', command = browseButton)
    browse_button.grid(row = 0 , column = 1,sticky = 'nsew')



main_frame = Frame(root , bg = back_color)


title = Label(main_frame,text = 'Youtube Video Downloader' , bg = '#212121', height = 2 , fg = text_color, font = 'TkFixedFont 25')


empty_frame = Frame(main_frame , bg =back_color , height = 10)
empty_frame2 = Frame(main_frame , bg =back_color , height = 10)
empty_frame3 = Frame(main_frame , bg ="#212121" , height = 10)
empty_frame5 = Frame(main_frame , bg ="#212121" , height = 5)


tab_frame = Frame(main_frame,bg = '#414141' , height = 50 )
tab_frame.grid_columnconfigure(0 , weight = 1)
tab_frame.grid_columnconfigure(1 , weight = 1)

video_tab = Button(tab_frame , bg = '#212121' , text = 'Video' , bd = 0, fg = text_color , highlightthickness = 0,activebackground = '#414141' ,
                   activeforeground = text_color,command = pressVideoTab,font = 'TkFixedFont 14',disabledforeground = text_color, state = 'disabled')

audio_tab = Button(tab_frame , bg = front_color , text = 'Audio' , bd = 0 , fg = text_color,highlightthickness = 0,activebackground = '#414141' ,
                   activeforeground = text_color,command = pressAudioTab,font = 'TkFixedFont 14',disabledforeground = text_color)



search_frame = Frame(main_frame , height = 50,bg =front_color)
search_entry = Entry(search_frame ,fg = front_color,bg = text_color , highlightcolor = front_color,bd = 0)
search_button = Button(search_frame , text = 'GO!',bd = 0 , fg = text_color , highlightthickness=0,
                       bg = front_color,activebackground = '#414141' , activeforeground = text_color,font = 'TkFixedFont 14', command = getLinkThreaded)
search_entry.bind("<Return>",getLinkThreaded)
search_entry.focus_set()
search_frame.grid_columnconfigure(0 , weight = 8)
search_frame.grid_columnconfigure(1 , weight = 1)
video_download_frame = Frame(main_frame,bg = '#212121')
audio_download_frame = Frame(main_frame,bg = '#212121')
r1 = Radiobutton(empty_frame3 , text = 'mp4' , variable = file_extension , value = 'mp4' ,bg = '#212121' , fg = text_color,
                 activeforeground=text_color, activebackground=front_color,highlightthickness=0,
                 selectcolor='#212121',font='TkFixedFont 14',command = redisplayStreamsThreaded)
r2 = Radiobutton(empty_frame3 , text = 'webm' , variable = file_extension , value = 'webm' ,bg = '#212121' , fg = text_color,
                 activeforeground=text_color, activebackground=front_color,highlightthickness=0,
                 selectcolor='#212121',font='TkFixedFont 14',command = redisplayStreamsThreaded)
extension_label  = Label(empty_frame3, text='File Extension : '
                                     , bg='#212121', fg=text_color, font='TkFixedFont 14')

refresh_button = Button(empty_frame3, text='Refresh', bd=0, highlightthickness=0,
                                       bg=front_color, fg=text_color,
                                       activeforeground=text_color, activebackground=front_color,
                                       command=redisplayStreamsThreaded,font='TkFixedFont 14')
settings_button = Button(empty_frame3, text='Settings', bd=0, highlightthickness=0,
                                       bg=front_color, fg=text_color,
                                       activeforeground=text_color, activebackground=front_color,
                                       command=settingsWindow,font='TkFixedFont 14')
empty_label =  Label(empty_frame3, text='           '
                                     , bg='#212121', fg=text_color, font='TkFixedFont 14')
empty_label2 =  Label(empty_frame3, text='    '
                                     , bg='#212121', fg=text_color, font='TkFixedFont 14')




#


#placement
# main_frame.pack(fill = 'both' , expand = True)
main_frame.pack(fill = 'both' ,expand = True)
title.pack(fill = 'x')
empty_frame.pack(fill = 'x')

search_frame.pack(fill = 'x' )
search_entry.grid(row = 0 , column = 0,sticky = 'nsew')
search_button.grid(row = 0 , column = 1,sticky = 'nsew')

#
empty_frame2.pack(fill = 'x')

tab_frame.pack(fill = 'x')
video_tab.grid(row = 0 , column = 0, sticky = 'nsew')
audio_tab.grid(row = 0 , column = 1,sticky = 'nsew')
empty_frame5.pack(fill='x')
empty_frame3.pack(fill = 'x')
extension_label.grid(row=0,column = 0 , sticky = 'nsew')

r1.grid(row=0,column = 1 , sticky = 'nsew')
r2.grid(row=0,column = 2 , sticky = 'nsw')
empty_label.grid(row=0,column=3,sticky="nsew")
empty_label2.grid(row=0,column=5,sticky = 'nsew')
refresh_button.grid(row=0,column =6  ,sticky = "nse" )
settings_button.grid(row=0,column = 4,stick = 'nsew')
video_download_frame.pack(fill ='both' , expand = True)
mainloop()
