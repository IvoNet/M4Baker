# TODO

## POCs

* √ Event emitter tests / Singleton? / Module? -> Implemented.
* √ wxGlade gui builder -> Works fine -> prefer it (bit more intuitive for me)
* √ wxFormBuilder gui builder -> Works fine!

## GUI

* √ ToolBar
* √ Create MainPanel
* √ Create Log Dialog
* √ Create process dialog
* √ Create About dialog
* Application Settings Panel (ini file)
  * √ where to save this? ~/Library/Application Support/m4baker or something?
  * √ Save Screen size
  * √ Save Screen position
  * Default work base dir location
* √ Drag and Drop panel for mp3
* √ Drag and Drop panel for Cover art

## Business logic

* √ Dirty check for images (if stuff was done manually)
* Save project?!
* √ Clean project
* √ Set track
* Extract Chapters
* Calculate chapters
* Create chapter file
* √ Set chapter text (Default = chapter)
* Set target dir (default = dir where mp3 came from unless there are more locations otherwise Music folder)
* √ Get bitrate mp3
* √ Get sample rate mp3
* √ Set Fixed length chapter (default = 10 minutes)
* X Set output quality (default = copy)
* Extract number of processors
  * default all -1 for concurrent processes
  * overridable with "just do it"
* √ Extract / Set Artist
* √ Extract / Set CoverArt
* Set Temp dir (work dir)
* √ Set Fixed length (default is calculate but override checkbox)
* X Convert cover to png
* √ wrap mp3s into one file
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
* √ Create model
* Create queue
* √ PyDoc
* Unit tests for business logic.
* Recent file history
  * √ max 9 entries
  * √ Save Settings when history added
  * √ Read history on startup
  * Delete history item if not exists anymore (on selecting it)
  * Remove history item if wanted
* GUI enable/disable buttons and menu items if project not ready to
  * Process
  * already clean
  * Can't stop what not has been started
  * ?
* When loading a saved project check if all is still in order
  * Do the mp3 file references still exist?
