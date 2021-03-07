# M4B Baker

This audiobook maker is an attempt to make a gui application as more beautiful macOS replacement for my
[m4b](https://github.com/IvoNet/docker-mediatools/blob/master/bin/m4b) command-line tool

# Requirements

- Python 3.9 (brew install python)

To be placed in src/resources:

- ffmpeg (brew install ffmpeg)
- mp4chaps (brew install mp4v2)
- mp4art (brew install mp4v2)
- AtomicParsley (brew install AtomicParsley)
- mp3binder (build from source: https://github.com/crra/mp3binder)

how...

```shell
cp -vf "$(which ffmpeg)" "./src/resources"
cp -vf "$(which ffprobe)" "./src/resources"
cp -vf "$(which mp4chaps)" "./src/resources"
cp -vf "$(which mp4art)" "./src/resources"
cp -vf "$(which AtomicParsley)" "./src/resources"
```

Not yet sure if I need them all but will adjust as needed :-)

## Create environment

To create and activate the environment

```shell
python3.9 -m venv venv
source venv/bin/activate
pip install poetry 
poetry install
```

## Usage

```shell
cd PROJECT
source venv/bin/activate
python src/m4baker.py
```

## Build Mac App

```shell
source venv/bin/activate
./build.sh [clean]
```

The clean option will first remove the build and dist folder before rendering all the images to the
ivonet/image/images.py file and building the application

See also the build.sh script

## Rendering the images

```shell
./images.sh
```

This script will convert all the ./images/*.{bmp,png} images to a format easily understood by wxPython.
