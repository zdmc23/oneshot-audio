import os
import glob
#import sys

# credit: https://stackoverflow.com/a/36461422
from pydub import AudioSegment
from pydub.silence import split_on_silence

#data_dir = sys.argv[1]
data_dir = os.getcwd()
paths = glob.glob(os.path.join(data_dir, '*-p.wav'))
for path in paths:
  #print(path)
  sound_file = AudioSegment.from_wav(path)
  audio_chunks = split_on_silence(sound_file, 
      # must be silent for at least half a second
      min_silence_len=500,
      # consider it silent if quieter than -16 dBFS
      silence_thresh=-32
  )
  path_parts = path.split("/")
  filename =  path_parts[-1]
  filename_p = filename.split(".")[0]
  
  for ii, chunk in enumerate(audio_chunks):
    out_file = os.path.join(data_dir,filename_p+str(ii)+'zz.wav')
    print("exporting: " + out_file)
    chunk.export(out_file, format="wav")
