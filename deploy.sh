#!/bin/sh
# Builds the site and copies only what belongs on the server into dist/.
# Sources (build.py, make-assets.py, READMEs, .DS_Store) stay behind.
set -e
cd "$(dirname "$0")"

python3 build.py

rm -rf dist
mkdir -p dist/en dist/assets/img

cp index.html progetti.html chi-sono.html case-study.html moire.html algosynth.html \
   robots.txt sitemap.xml dist/
cp en/index.html en/projects.html en/about.html \
   en/moire.html en/algosynth.html en/case-studies.html          dist/en/
cp assets/site.css assets/site.js                               dist/assets/
cp assets/img/mark.svg assets/img/favicon-32.png \
   assets/img/apple-touch-icon.png assets/img/og-image.png \
   assets/img/alessandro.jpg assets/img/moire.jpg \
   assets/img/algosynth.jpg                                     dist/assets/img/

mkdir -p dist/lab
cp -R lab/moire dist/lab/

find dist -name '.DS_Store' -delete

echo "dist/ ready — $(find dist -type f | wc -l | tr -d ' ') files"
