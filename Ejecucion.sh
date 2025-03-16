#!/usr/bin/bash

PYTHON="${HOME}/anaconda3/bin/python3"
fecha_hora=$(date +"%Y%m%d_%H%M")

cd Python_Core

$PYTHON Exe.py

cd ..
cd LaTeX_Core
ls -l
pdflatex General.tex

mv General.pdf Informe.pdf
cp Informe.pdf ..
cd ..

nombre="${fecha_hora}.pdf"

mv Informe.pdf Informe_$nombre

