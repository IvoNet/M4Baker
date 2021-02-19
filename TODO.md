# TODO

* ToolBar
* Create MainPanel
* Create Log Dialog
* Create process dialog
* √ Create About dialog
* Application properties Panel (ini file)
  * where to save this? ~/Library/Application Support/ivonet/m4baker or something?
* Set track
* Extract Chapters
* Calculate chapters
* Create chapter file
* Set chapter text (Default = chapter)
* Set target dir (default = dir where mp3 came from unless there are more locations otherwise Music folder)
* Get bitrate mp3
* Get sample rate mp3
* Set Fixed length chapter (default = 10 minutes)
* Set output quality (default = copy)
* Extract number of processors
  * default all -1 for concurrent processes
  * overridable with "just do it"
* Extract / Set Artist
* Extract / Set CoverArt
* Set Temp dir (work dir)
* Set Fixed length (default is calculate but override checkbox)
* Convert cover to png
* wrap mp3s into one file
* Convert to m4a
  * `ffmpeg -i "${GROUPED_MP3_NAME}" -v quiet -stats -threads 4 -vn -y -acodec aac -strict -2 -map_metadata 0 -map_metadata:s:a 0:s:a -ab "${BITRATE}"k -ar "${SAMPLERATE}" -ac 1 "${AUDIOBOOK}.m4a"`
  * parse stats for progress
* add Tags
  * `AtomicParsley "${AUDIOBOOK}.m4a" --title "${TITLE}" --grouping "${GROUPING}" --sortOrder album "${GROUPING}" --album "${ALBUM}" --artist "${AUTHOR}" --genre "${GENRE}" --tracknum "${TRACK}" --disk "${TRACK}" --comment "${COMMENT}" --year "${YEAR}" --stik Audiobook --overWrite`
* convert to m4b (see add Tags `--stik Audiobook --overWrite`)
* Set Chapter info on m4b
  * if chapter file: `mp4chaps -i "${AUDIOBOOK}.m4b"`
  * if fixed length: `mp4chaps -e "${CHAPTER_LENGTH}" "${AUDIOBOOK}.m4b"`
* Add CoverArt to m4b
  * `mp4art --add "$(find . -name '*.jpg' | head -n 1)" "${AUDIOBOOK}.m4b"`
* Move finished audiobook to target location
* Clean temp space
* Create model
* Create queue
