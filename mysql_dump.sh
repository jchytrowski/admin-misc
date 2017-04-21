#!/bin/bash

DBNAME=Audition
MAXIMUM=7
BACKUPDIR=db\ backups/
USER=jchytrowski
PASS="password with spaces"
ADMIN='your@email.com'

# not best practice to keep a root password in an unencrypted file, but this script is pretty locked down; The alternative is creating
# a user just for downloading backups, but that would have read/write permission on the backups it's creating, which is nearly as bad
# as having permissions on the live database.  

#reformat in case user added trailing slash to the directory
BACKUPDIR=$(echo $BACKUPDIR | sed 's|/$||g')


# Uncomment below when you've configured a mail client- I'd set it up for you, but loosely configured mail clients 
# can get your machines blacklisted as suspected spammers, and I don't have time to do it correctly right now.

function alert_admin {
#    echo "DANGER, something went wrong with the $DBNAME backup at $(date)" | mail -s "$DBNAME BACKUP PROBLEM" $admin
    echo 'something went wrong'
    exit 1
}
trap alert_admin ERR

# create backupdir if not exists and restrict permissions
if [ ! -e "${BACKUPDIR}" ]
then
	 mkdir "${BACKUPDIR}" && chmod 700 "${BACKUPDIR}" || alert_admin
fi

# brackets in case the password has spaces
mysqldump --lock-tables ${DBNAME} -p"${PASS}" -u $USER > "${BACKUPDIR}"/${DBNAME}.sql.$(date +%s) || alert_admin



while [ True ];
do

	# I know that evaluating every single loop is very inefficient;
	# but it's also logically simple and maintanable.

	# The regex is just to prevent us from accidentally deleting similarly named backups, like '$DBNAME.sql.07092017';
	# This will just delete files with a 10-digits suffix created by 'date +%s'.
        CHOPPING_BLOCK=$(find "${BACKUPDIR}" -regextype sed -regex "${BACKUPDIR}/${DBNAME}.sql.[0-9]\{10\}" | head -1)

        BACKUPCOUNT=$(find "${BACKUPDIR}" -regextype sed -regex "${BACKUPDIR}/${DBNAME}.sql.[0-9]\{10\}" | wc -l)


        if [ $BACKUPCOUNT -le $MAXIMUM ];
        then
                exit
	# It's generally good practice to make sure the thing you think you're deleting actually exists, and is a regular file;
	# [ Primarily a risk for recursive deletion, where rm -rf $emptyvar deletes everything in cwd ]
        elif [ $BACKUPCOUNT -gt $MAXIMUM ] && [ -f "${CHOPPING_BLOCK}" ];
        then
                rm "${CHOPPING_BLOCK}"
        fi
done
