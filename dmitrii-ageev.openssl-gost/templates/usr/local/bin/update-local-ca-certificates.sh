#!/bin/bash

CA_DIR="/usr/local/share/ca-certificates"
mkdir -p $CA_DIR
cd ${CA_DIR}-ru
ls * | while read file; do
    hashname="$(openssl x509 -hash -in "${CA_DIR}-ru/$file" -inform DER -noout 2>/dev/null)" || \
    hashname="$(openssl crl -hash -in "${CA_DIR}-ru/$file" -inform DER -noout 2>/dev/null)"
    if [ $? -ne 0 ]; then
      cp -f "${CA_DIR}-ru/$file"  "${CA_DIR}/"
    else
      rm -f "${CA_DIR}/${hashname}*" &>/dev/null
      openssl x509 -in "${CA_DIR}-ru/$file" -inform DER -outform PEM -out "${CA_DIR}/${hashname}" &>/dev/null && \
	      mv "${CA_DIR}/$hashname" "${CA_DIR}/${hashname}.crt" && \
	      ln -sf "${CA_DIR}/${hashname}.crt" "${CA_DIR}/${hashname}.0"

      openssl crl -in "${CA_DIR}-ru/$file" -inform DER -outform PEM -out "${CA_DIR}/${hashname}" &>/dev/null && \
	      mv "${CA_DIR}/$hashname" "${CA_DIR}/${hashname}.crl" && \
	      ln -sf "${CA_DIR}/${hashname}.crl" "${CA_DIR}/${hashname}.r0"
    fi
done
/usr/sbin/update-ca-certificates --fresh &>/dev/null
