for file in $(ls -1 | egrep '(kb.mp3)$');
do
  echo "Cutting "$file
  file_name=${file%.*}
  file_ext=${file#*.}
  new_filename="$file_name-p.$file_ext"
  #mpgsplit $file [00:00:06-00:00:18] -o $new_filename 
  ffmpeg -t 11 -ss 00:00:08.000 -i $file -acodec copy $new_filename
done
