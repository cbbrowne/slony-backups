#!/bin/sh

BUGHOME=${HOME}/PostgreSQL/slony-backups/Slony-Bugzilla
mkdir -p ${BUGHOME}
cd $BUGHOME
git fetch origin
git pull origin master
wget -O ${BUGHOME}/bugs-not-closed.html "http://www.slony.info/bugzilla/buglist.cgi?query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED"

wget -O ${BUGHOME}/bugs-closed.html "http://www.slony.info/bugzilla/buglist.cgi?query_format=advanced&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED"

mkdir -p ${BUGHOME}/individual-bugs
for i in `seq 250`; do
    wget -O ${BUGHOME}/individual-bugs/${i}.html "http://www.slony.info/bugzilla/show_bug.cgi?id=${i}"
done

git add ${BUGHOME}/bugs-not-closed.html
git add ${BUGHOME}/bugs-closed.html
git add ${BUGHOME}/individual-bugs/*.html

git commit -m "Check in bug updates - run of scripts/Slony-Archive-Bugzilla.sh"
git push origin master
