#!/bin/sh
# Builds the site and copies only what belongs on the server into dist/.
# Sources (build.py, make-assets.py, READMEs, .DS_Store) stay behind.
set -e
cd "$(dirname "$0")"

python3 build.py

rm -rf dist
mkdir -p dist/en dist/assets/img

cp index.html progetti.html chi-sono.html privacy.html metodologia.html case-study.html \
   case-ai-adoption.html case-james.html case-cloud-scale.html \
   moire.html algosynth.html \
   robots.txt sitemap.xml dist/
cp en/index.html en/projects.html en/about.html en/privacy.html \
   en/moire.html en/algosynth.html en/case-studies.html \
   en/case-ai-adoption.html en/case-james.html \
   en/case-cloud-scale.html                                     dist/en/
cp assets/site.css assets/site.js assets/ai-maturity.css assets/ai-maturity.js dist/assets/
# the check is served at /ai-maturity, so it ships as a folder index
mkdir -p dist/ai-maturity
cp ai-maturity.html                                             dist/ai-maturity/index.html
cp assets/img/mark.svg assets/img/favicon-32.png \
   assets/img/apple-touch-icon.png assets/img/og-image.png \
   assets/img/alessandro.jpg assets/img/moire.jpg \
   assets/img/algosynth.jpg assets/img/og-priors.png \
   assets/img/og-algosynth.png assets/img/og-ai-maturity.png    dist/assets/img/

mkdir -p dist/lab
cp -R lab/moire dist/lab/

# Priors: standalone tool, deliberately not linked from the rest of the site
mkdir -p dist/priors/en
cp priors/index.html priors/priors.css priors/priors.js dist/priors/
cp priors/en/index.html                                 dist/priors/en/

# AlgoSynth: the original sequencer, restyled — also unlinked
mkdir -p dist/algosynth/en dist/algosynth/js
cp algosynth/index.html algosynth/algosynth.css dist/algosynth/
cp algosynth/js/*.js                            dist/algosynth/js/
cp algosynth/en/index.html                      dist/algosynth/en/

find dist -name '.DS_Store' -delete

echo "dist/ ready — $(find dist -type f | wc -l | tr -d ' ') files"
