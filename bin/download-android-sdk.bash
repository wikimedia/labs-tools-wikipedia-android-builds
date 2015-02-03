SDK_HOME_PATH="/srv/adk"
TMP_PATH="/tmp"
TMP_ADK_PATH="$TMP_PATH/android-sdk-linux"
 
# Needs to be updated when new releases are made
SDK_DOWNLOAD_URL="http://dl.google.com/android/android-sdk_r24.0.2-linux.tgz"

mkdir $TMP_ADK_PATH
curl --location $SDK_DOWNLOAD_URL | tar -xz -C $TMP_PATH

chown -R android-build:android-build $TMP_ADK_PATH
mv $TMP_ADK_PATH $SDK_HOME_PATH
