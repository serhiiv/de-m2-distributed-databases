# delete old key
sudo rm -rf ${PWD}/rs_keyfile

# generate authentication key
openssl rand -base64 756 > ${PWD}/rs_keyfile

# set permissions 
chmod 0400 ${PWD}/rs_keyfile
sudo chown 999:999 ${PWD}/rs_keyfile
