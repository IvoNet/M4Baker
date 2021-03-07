# TODO

## POCs

* √ Event emitter tests / Singleton? / Module? -> Implemented.
* √ wxGlade gui builder -> Works fine -> prefer it (bit more intuitive for me)
* √ wxFormBuilder gui builder -> Works fine! -> But used wxGlade

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

* Set target dir (default = dir where mp3 came from unless there are more locations otherwise Music folder)
* Extract number of processors
  * default all -1 for concurrent processes
  * overridable with "just do it"
* Recent file history
  * √ max 9 entries
  * √ Save Settings when history added
  * √ Read history on startup
  * Delete history item if not exists anymore (on selecting it)
  * Remove history item if wanted
* When loading a saved project check if all is still in order
  * Do the mp3 file references still exist?
* Save queue on exit for continuation on restart
* Remove from Queue when done
* Choose output folder
  * per project?
  * default output folder?
* Clean up GUI
* Clean dbg() statements
* Improve Log statements
* Clean log on to big?!
* Save project form queue
  * if forgotten on double click?
* Refactor code.
  * Give own places
  * Process TODO's
  * Documentation
  * clean code
* Replace current chapter duration with ffprod because it is more accurate now sometimes a few seconds off.
* √ Dirty check for images (if stuff was done manually)
* √ Save project?!
* √ Clean project
* √ Set track
* √ Extract Chapters
* √ Calculate chapters
* √ Create chapter file
* √ Set chapter text (Default = chapter)
* √ Get bitrate mp3
* √ Get sample rate mp3
* √ Set Fixed length chapter (default = 10 minutes)
* X Set output quality (default = copy)
* √ Extract / Set Artist
* √ Extract / Set CoverArt
* √ Set Temp dir (work dir) -> Default now and removal too
* √ Set Fixed length (default is calculate but override checkbox)
* X Convert cover to png
* √ wrap mp3s into one file
* √ Convert to m4a
  * √ parse stats for progress
* √ add Tags
  *
  √ `AtomicParsley "${AUDIOBOOK}.m4a" --title "${TITLE}" --grouping "${GROUPING}" --sortOrder album "${GROUPING}" --album "${ALBUM}" --artist "${AUTHOR}" --genre "${GENRE}" --tracknum "${TRACK}" --disk "${TRACK}" --comment "${COMMENT}" --year "${YEAR}" --stik Audiobook --overWrite`
* √ convert to m4b (see add Tags `--stik Audiobook --overWrite`)
* √ Set Chapter info on m4b
  * √ if chapter file: `mp4chaps -i "${AUDIOBOOK}.m4b"`
  * √ if fixed length: `mp4chaps -e "${CHAPTER_LENGTH}" "${AUDIOBOOK}.m4b"`
* √ Add CoverArt to m4b
  * √ `mp4art --add "$(find . -name '*.jpg' | head -n 1)" "${AUDIOBOOK}.m4b"`
* √ Move finished audiobook to target location
* √ Clean temp space
* √ Create model
* √ Create queue
* √ PyDoc
* Unit tests for business logic.
* √ GUI enable/disable buttons and menu items if project not ready to
  * √ Process
  * √ already clean
  * √ Can't stop what not has been started
