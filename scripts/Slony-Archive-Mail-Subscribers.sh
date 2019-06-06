#!/bin/sh
ARCHIVEHOME=${HOME}/PostgreSQL/slony-backups/Slony-Mail-Archives
mkdir -p $ARCHIVEHOME
cd $ARCHIVEHOME
git fetch origin
git pull origin master

# Set up password for Mailman
MAILMANPASSFILE=${MAILMANPASSFILE:-"${HOME}/GitConfig/InitFiles/Slony/slony-mailman-password"}
MAILMANSUBTOOL=${MAILMANSUBTOOL:-"${HOME}/GitStuff/mailman-subscribers/mailman-subscribers.py"}

GPGKEYS=${GPGKEYS:-"--recipient 6aa6a713 --recipient 5e1e4739 "}

# another was ... --recipient 5E1E4739"}

for list in bugs commit general hackers patches; do
    listname=slony1-${list}
    listfile=${ARCHIVEHOME}/${listname}/subscribers.asc
    templocation=`mktemp`
    echo "Grabbing subscribers of Slony list ${listname} into data file: [${templocation}]"
    python ${MAILMANSUBTOOL} -o ${templocation} --password-file=${MAILMANPASSFILE} lists.slony.info ${listname} 
    echo "Encrypt [${templocation}] into [${listfile}] for GPG user list ${GPGKEYS}"
    gpg --encrypt --armor  `echo ${GPGKEYS}` --batch --yes --trust-model always -o ${listfile} ${templocation}
    rm -f ${templocation}
    git add ${listfile}
done

git commit -m "Check in mailing list subscribers - run of scripts/Slony-Archive-Mail-Subscribers.sh"
git push origin master
