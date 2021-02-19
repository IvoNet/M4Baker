# Needed Files

- ffmpeg / ffprobe
- mp4v2: mp4art / mp4chaps
- AtomicParsley

The license files explain the contraints. In this application only binary versions are distributed build from an
unchanged codebase.

# ffmpeg

* Version: 4.3.1

# AtomicParsley

* Version: 20210124.204813.840499f

# mp4v2

* Version: 2.0.0

# Installation

I installed all these components by installing them on my mac with [brew](https://brew.sh)

and then copying the specific binaries I needed to the src/resources folder

something like:

```shell
cp -v "$(which mp4chaps)" "src/resources/"
cp -v "$(which mp4art)" "src/resources/"
cp -v "$(which ffmpeg)" "src/resources/"
cp -v "$(which ffprobe)" "src/resources/"
cp -v "$(which AtomicParsley)" "src/resources/"
```
