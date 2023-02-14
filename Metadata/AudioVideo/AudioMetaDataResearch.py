#mp3 tags
#Title
#Subtitle
#Rating
#Comments
#Contributing artists
#Album artist
#Album
#Year
#Genre
#Length
#Bit Rate
#Publisher
#Name
#Item type
#Folder path
#Date created
#Date modified
#Size

from mutagen.mp3 import MP3

audio = MP3("Walk Like An Egyptian.mp3")
# print (audio.info)
print (audio.tags.values())

# for frames in audio.tags.values():
#     frame_name = audio.get(frames.FrameID, frames.FrameID)
#     # print(frame_name)
#     desc = getattr(frames, 'desc', "N/A")
#     text = getattr(frames, 'text', ["N/A"])[0]
#     value = getattr(frames, 'value', "N/A")

#     print('Description: ' + str(desc))
#     print('Text: ' + str(text))
#     print('Value: ' + str(value))