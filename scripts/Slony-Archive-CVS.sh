#!/bin/sh
ARCHIVEHOME=${HOME}/PostgreSQL/slony-backups
mkdir -p $ARCHIVEHOME
cd $ARCHIVEHOME
git fetch origin
git pull origin master

if [[ -d ${ARCHIVEHOME}/slony1-www ]]; then
    echo "CVS Repository already available"
else
    echo "No CVS material found at ${ARCHIVEHOME}/slony1-www - setting up anonymous login"
    CVSROOT=":pserver:anonymous:@main.slony.info:/slony1" cvs login
fi

git rm -r slony1-www
CVSROOT=":pserver:anonymous@main.slony.info:/slony1" cvs co slony1-www
echo "CVS" >> $ARCHIVEHOME/slony1-www/.gitignore
git add slony1-www
git commit -m "Check in CVS updates - run of scripts/Slony-Archive-CVS.sh"
git push origin master
