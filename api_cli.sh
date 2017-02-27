#!/bin/bash

COOKIES_FILE="tks.cookies"
CSRF_TOKEN_FILE="tks.token"
HEADERS=

function apicall()
{
    URI=$2
    METHOD=$1
    DATA=$3
    curl -X $METHOD\
	 -d "$DATA"\
	 -c "$COOKIES_FILE" -b "$COOKIES_FILE"\
	 -H "$HEADERS"\
	 -s\
	 http://localhost:8000/api/$URI
}

function setCSRFToken()
{
    if ! [ -z "$CSRF_TOKEN" ]
    then
	HEADERS="X-CSRFToken: $CSRF_TOKEN"
    else
	if [ -f $CSRF_TOKEN_FILE ]
	then
	    	HEADERS="X-CSRFToken: `cat $CSRF_TOKEN_FILE`"
	fi
    fi
}

case $1 in
    login)
	CSRF_TOKEN=`apicall GET login/challenge | sed -r 's|.*csrf.*:.*"(.*).}|\1|g'`

	setCSRFToken

	apicall POST login 'creds={"username":"'$2'","password":"'$3'"}'

	#Save new token after login
	CSRF_TOKEN=`apicall GET login/challenge | sed -r 's|.*csrf.*:.*"(.*).}|\1|g'`
	echo $CSRF_TOKEN > $CSRF_TOKEN_FILE
	;;
    logout)
	apicall GET logout
	;;
    *)
	CMD=$1
	
	case $4 in
	    datapoint)
		case $CMD in
		    get)
			apicall GET serie/$3/datapoint/$5
			;;
		    add)
			setCSRFToken
			apicall POST serie/$3/datapoint "value=$5"
			;;
		    delete)
			setCSRFToken
			apicall DELETE serie/$3/datapoint/$5
			;;
		esac
		;;
	    *)
		case $CMD in
		    get)
			apicall GET serie/$3
			;;
		    add)
			setCSRFToken
			apicall POST serie "name=$3&time_type=$4&value_type=$5"
			;;
		    delete)
			setCSRFToken
			apicall DELETE serie/$3
			;;
		esac
		;;
	esac
	;;
esac

echo
