#!/bin/sh
export TEXMFHOME=/data/texmfhome
tlmgr init-usertree
tlmgr --usermode install mdframed zref needspace libertine titling
pandoc --pdf-engine=xelatex tuto_python_astro.md -o tuto_python_astro.pdf
