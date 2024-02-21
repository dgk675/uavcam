for file in captures/*.h264; do
    ffmpeg -i ${file%.*}.h264 -vcodec libx264 -acodec aac ${file%.*}.mp4
done