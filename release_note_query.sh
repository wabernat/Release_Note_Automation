#! /bin/bash

curl --request POST\
  --user <DEV_USER>:<DEV_KEY_CHANGE_ME>\
  --header 'Accept: application/json'\
  --header 'Content-Type: application/json'\
  --data '{ "jql" : "project = S3C AND fixVersion >= 7.4.0 AND status = done AND \"Release notes\" = \"Yes as Fixed Issue only (please fill Release Note)\" "}' \
  --url 'https://scality.atlassian.net/rest/api/2/search' | jq  '.issues[] | {"key": .key, "Severity": .fields.customfield_10800.value, "Component(s)": [.fields.components[].name], "Release note description": .fields.customfield_12102}' > jq-formatted.json

echo '<?xml version="1.0" encoding="utf-8"?>' > fixed_table.htm
echo '<html xmlns:MadCap="http://www.madcapsoftware.com/Schemas/MadCap.xsd" MadCap:lastBlockDepth="2" MadCap:lastHeight="311" MadCap:lastWidth="648">' >> fixed_table.htm
echo '<head> </head>' >> fixed_table.htm
echo '<body>' >> fixed_table.htm
echo '<h2 MadCap:autonum="1.1 &#160;">Fixed Issues</h2>' >> fixed_table.htm
echo "<table style=\"mc-table-style: url('Resources/TableStyles/DetailedwithPadding.css');\" class=\"TableStyle-DetailedwithPadding\" cellspacing=\"0\">" >> fixed_table.htm
echo '<thead>' >> fixed_table.htm
echo '<tr>' >> fixed_table.htm
echo '<td>Key</td><td>Severity</td><td>Component(s)</td><td>Description</td>' >> fixed_table.htm
echo '</tr>' >> fixed_table.htm
echo '</thead>' >> fixed_table.htm

while read line ; do
    if [[ $line == *"\"key\":"* ]] ;
    then
        line=${line%\"*}
        line=${line##*\"}
        printf "<tr><td>$line</td>" >> fixed_table.htm
#        printf "key = $line\n"
    fi

    if [[ $line == *"\"Severity\":"* ]] ;
    then
        line=${line%\"*}
        line=${line##*\"}
        printf "<td>$line</td>" >> fixed_table.htm
        printf '<td>&#160;</td>' >> fixed_table.htm
#        printf "Severity = $line\n"
    fi

    if [[ $line == *"Component(s)"* ]] ;
      then
      printf '<td><p>' >> fixed_table.htm
      printf '&#160;</p></td>' >> fixed_table.htm
    fi

#    until [[ $line == *'],'* ]] ;
#    do
#      echo $line
#      printf "$line " >> fixed_table.htm ;
#    done

#    printf '</p></td>' >> fixed_table.htm

    if [[ $line == *"Release\ note\ description:"* ]] ;
    then
	line=${line%\"*}
	line=${line##*\"}
	printf "<td>$line</td>" >> fixed_table.htm
	printf '</tr>\n' >> fixed_table.htm ;
    fi

done < jq-formatted.json ;

echo '</table>' >> fixed_table.htm
echo '</body>' >> fixed_table.htm
echo '</html>' >> fixed_table.htm
