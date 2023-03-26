# Needed Files

- ffmpeg
- mp4v2: mp4art / mp4chaps
- AtomicParsley
- mp3binder (https://github.com/crra/mp3binder)

The license files explain the constraints. In this application only binary
versions are distributed build from an unchanged codebase.

# ffmpeg

* Version: 4.4
* get it from [here](https://evermeet.cx/ffmpeg/) (you need a static binary)

# AtomicParsley

* Version: 20210124.204813.840499f
* download from [here](https://github.com/wez/atomicparsley/releases/)

# mp4v2

* Version: 2.1.2

now build from source:

- you need the xcode command line tools installed

```shell
git clone git@github.com:enzo1982/mp4v2.git
cd mp4v2
autoreconf -i
./configure --enable-shared=no --enable-static=yes
make
```

# mp3binder

* Version used: 3.0.0-1-g7e2e54c
* Build from source

# Installation

NOTE: Sometimes if done this way you will lose the dynamic links... it is better
to get static binaries

I installed all these components by installing them on my mac
with [brew](https://brew.sh)

and then copying the specific binaries I needed to the src/resources folder

something like:

```shell
cp -v "$(which mp4chaps)" "src/resources/"
cp -v "$(which mp4art)" "src/resources/"
cp -v "$(which ffmpeg)" "src/resources/"
cp -v "$(which ffprobe)" "src/resources/"
cp -v "$(which AtomicParsley)" "src/resources/"
```
