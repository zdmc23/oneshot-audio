#!/bin/bash
for file in $(ls -1 | egrep '(-p.mp3)$');
do
  echo "Converting "$file" to wav"
  file_name=${file%.*}
  new_filename="$file_name.wav"
  lame --decode $file $new_filename
done
