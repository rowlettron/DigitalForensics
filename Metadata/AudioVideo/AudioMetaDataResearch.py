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

audio = MP3("C:\\Projects\\Python\\DigitalForensics\\EmbeddedMetaData\\Walk Like An Egyptian.mp3")
print (audio.info)

