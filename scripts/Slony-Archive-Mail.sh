#!/bin/sh
ARCHIVEHOME=${HOME}/PostgreSQL/slony-backups/Slony-Mail-Archives
mkdir -p $ARCHIVEHOME
cd $ARCHIVEHOME
git fetch origin
git pull origin master


pull_all_years () {
    local list=$1
    listname=slony1-${list}
    listdir=${ARCHIVEHOME}/${listname}
    mkdir -p ${listdir}
    #for year in 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017; do
    for year in 2017 2018; do
     	for month in January February March April May June July August September October November December; do
     	    currenturl=`date +"http://lists.slony.info/pipermail/${listname}/${year}-${month}.txt.gz"`
     	    currentfile=${year}-${month}.txt
     	    rm -f ${listdir}/temp.gz
     	    wget -O ${listdir}/temp.gz $currenturl
     	    zcat ${listdir}/temp.gz > ${listdir}/${currentfile}
    	    git add ${listdir}/${currentfile}
     	done
    done
}

for list in bugs commit general hackers patches; do
    listname=slony1-${list}
    listdir=${ARCHIVEHOME}/${listname}
    currenturl=`date +"http://lists.slony.info/pipermail/slony1-${list}/%Y-%B.txt.gz"`
    currentfile=`date +"%Y-%B.txt"`
    rm -f ${listdir}/latest.gz
    wget -O ${listdir}/latest.gz $currenturl
    zcat ${listdir}/latest.gz > ${listdir}/${currentfile}
    git add ${listdir}/${currentfile}

    #pull_all_years ${list}
done

git commit -m "Check in mail archive updates - run of scripts/Slony-Archive-Mail.sh"
git push origin master
