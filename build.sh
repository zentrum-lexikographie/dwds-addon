#!/bin/bash
set -xe

cd src
rm -Rf web-ext-artifacts/
version=$(grep -E "\"version\": \"" manifest.json | grep -o "[0-9]*\.[0-9]*\.[0-9]*")

mv manifest-chrome.json ../manifest-chrome.json
web-ext build
mv web-ext-artifacts/im_dwds_nachschlagen-$version.zip ../im_dwds_nachschlagen-$version-firefox.zip

mv manifest.json ../manifest-firefox.json
mv ../manifest-chrome.json manifest.json

web-ext build
mv web-ext-artifacts/im_dwds_nachschlagen-$version.zip ../im_dwds_nachschlagen-$version-chrome.zip

mv manifest.json manifest-chrome.json
mv ../manifest-firefox.json manifest.json