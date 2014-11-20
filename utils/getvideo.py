# This python script combines youtube-dl script and ffmpeg
# to obtain youtube video, and if it is 'flv', convert it to mp4

from sys import argv
from os import system
from os import path, access, R_OK

id = argv[1]

# Download the video:
system('python youtube-dl http://www.youtube.com/watch?v=%s' % id)

# If it is FLV, convert it to MP4, and delete FLV
PATH = './%s.flv' % id
if path.exists(PATH) and path.isfile(PATH) and access(PATH, R_OK):
    system('ffmpeg -i %s.flv -vcodec copy -acodec copy %s.mp4' % (id,id))
    system('rm %s.flv' % id)


#   if path.exists(PATH) and path.isfile(PATH) and access(PATH, R_OK):
#       system('ffmpeg -i %s.flv -vcodec copy -acodec copy %s.mp4' % id)
#       system('rm %s.flv' % id)
#   else:
#       system('python youtube-dl http://www.youtube.com/watch?v=%s' % id)
#       try:
#           system('ffmpeg -i %s.flv -vcodec copy -acodec copy %s.mp4' % id)
#           system('rm %s.flv' % id)
#       except:
#           pass
