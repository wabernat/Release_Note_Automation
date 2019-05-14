#! /bin/bash

cat HEAD.html > index.html
printf "<body>\n" >> index.html
printf "<html>\n" >> index.html
cat introduction.html >> index.html
cat dependencies.html >> index.html
cat known_issues.html >> index.html
cat fixed.html >> index.html
printf "</body>" >> index.html
printf "</html>" >> index.html