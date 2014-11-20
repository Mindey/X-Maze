from sys import argv
from os import system
system('python youtube-dl %s' % argv[1])
ID = argv[1].split('=')[-1]
system('ffmpeg -i %s.flv -acodec pcm_s16le -ac 2 -ab 128 -vn -y %s.wav' % (ID, ID))
system('oggenc -q 6 %s.wav -o %s.ogg' % (ID, argv[2]))
system('rm %s.flv %s.wav' % (ID, ID))
