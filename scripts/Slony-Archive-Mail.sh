#!/bin/sh
ARCHIVEHOME=${HOME}/PostgreSQL/slony-backups/Slony-Mail-Archives
mkdir -p $ARCHIVEHOME
cd $ARCHIVEHOME
git fetch
git pull

for l in bugs commit general hackers patches; do
    list=slony1-${l}
    listdir=${ARCHIVEHOME}/${list}
    mkdir -p ${listdir}
    
    rm -f ${listdir}/latest.gz
    currenturl=`date +"http://lists.slony.info/pipermail/slony1-${l}/%Y-%B.txt.gz"`
    currentfile=`date +"%Y-%B.txt"`
    wget -O ${listdir}/latest.gz $currenturl
    zcat ${listdir}/latest.gz > ${listdir}/${currentfile}
    git add ${listdir}/${currentfile}

    for year in 2007 2008 2009 2010 2011 2012 2013; do
	for month in January February March April May June July August September October November December; do
	    currenturl=`date +"http://lists.slony.info/pipermail/slony1-${l}/${year}-${month}.txt.gz"`
	    currentfile=${year}-${month}.txt
	    wget -O ${listdir}/temp.gz $currenturl
	    zcat ${listdir}/temp.gz > ${listdir}/${currentfile}
	    git add ${listdir}/${currentfile}
	done
    done
done

git commit -m "Check in mail archive updates - run of scripts/Slony-Archive-Mail.sh"
