#!/bin/bash

CA_DIR={{ openssl__local_certs_dir }}
cd ${CA_DIR}-ru
ls * | while read file; do
    hashname="$(openssl x509 -hash -in "${CA_DIR}-ru/$file" -inform DER -noout 2>/dev/null).0"
    if [ $? -ne 0 ]; then
      cp -f "${CA_DIR}-ru/$file"  "$CA_DIR/$file"
    else
      openssl x509 -in "${CA_DIR}-ru/$file" -inform DER -outform PEM -out "$CA_DIR/$hashname" &>/dev/null
    fi
done
/usr/sbin/update-ca-certificates &>/dev/null
