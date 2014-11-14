SDK_HOME_PATH="/srv/adk"
 
# Needs to be updated when new releases are made
SDK_DOWNLOAD_URL="http://dl.google.com/android/android-sdk_r23.0.2-linux.tgz"
 
curl --location $SDK_DOWNLOAD_URL | tar -xz -C $SDK_HOME_PATH
