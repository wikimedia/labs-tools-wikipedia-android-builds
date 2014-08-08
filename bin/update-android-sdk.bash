SDK_HOME_PATH="$HOME"
SDK_PATH="$SDK_HOME_PATH/android-sdk-linux"
SDK_PACKAGES="tools,platform-tools,build-tools-20.0.0,android-19,extra-android-m2repository"
export _JAVA_OPTIONS="-Xmx256m"
export ANDROID_SWT="/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/ext:/usr/java/packages/lib/ext"
 
# Just install platform-tools, build-tools & Android-19
# Filter names are from `android list sdk -e -a`
expect -c "
set timeout -1;
spawn $SDK_PATH/tools/android update sdk -u --filter "$SDK_PACKAGES"

expect {
    \"Do you accept the license\" { exp_send \"y\r\"; exp_continue }
    eof
}
"
