#!/usr/bin/env bash

if [ -z "${VIRTUAL_ENV}" ]; then
  echo "Make sure you run this script from within the"
  echo "Python Virtual environment of this project"
  exit 1
fi

source="./images"
target="src/ivonet/image/images.py"

echo "Rendering all the images to be python code..."
rm -f "${target}"
unset img_opt

for img in ${source}/*.{bmp,png}; do
  filename="$(basename "${img}")"
  base_name="${filename%.*}"
  img2py ${img_opt} -i -c -n "${base_name}" "${source}/${filename}" "${target}"
  if [ -z "$img_opt" ]; then
    img_opt="-a"
  fi
done
