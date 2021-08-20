#!/bin/bash
# fetchbin.sh

set -euo pipefail


NAME=$1
URL=$2
DEST_DIR=/usr/local/sbin
TEMP_DIR=/tmp/fetchbin.tmp

# Dont reinstall.
which "$NAME" > /dev/null 2>&1 && exit

mkdir -p $TEMP_DIR && cd $TEMP_DIR

# Fetch release.
wget -nv -c "$URL"

# Extract and guess binary name.
case $URL in
  *.tar.gz)
    tar -xzf $NAME*.tar.gz ;
    BIN=$NAME ;
    ;;
  *.tgz)
    tar -xzf $NAME*.tgz ;
    BIN=$NAME ;
    ;;
  *.zip)
    unzip -qo $(basename $URL) ;
    BIN=$NAME ;
    ;;
  *)
    BIN=$(basename $URL) ;
    ;;

esac


# Pick and install.
sudo install "$TEMP_DIR/$BIN" "$DEST_DIR/$NAME"
