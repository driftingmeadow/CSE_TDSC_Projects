#!/bin/bash


# ==================================================
# install ubuntu packages
# ubuntu only
# ==================================================

# sudo apt update

sudo apt install -y default-jdk

sudo apt install -y mysql-server
sudo systemctl enable mysql --now

sudo apt install -y unzip


# ==================================================
# install tomcat9 to /opt/
# ubuntu only
# ==================================================

# downloads tomcat 9 binaries
# extracts and installs them to /opt/tomcat9/

if [ ! -d /opt/tomcat9 ] || [ -z "$(ls -A /opt/tomcat9)" ]; then
    tomcat_tmpdir=$(mktemp -d)

    wget -O "$tomcat_tmpdir/tomcat.tar.gz" \
        https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.109/bin/apache-tomcat-9.0.109.tar.gz

    sudo mkdir -p /opt/tomcat9/

    sudo tar -xzf "$tomcat_tmpdir/tomcat.tar.gz" \
        -C /opt/tomcat9 \
        --strip-components=1

    rm -rf "$tomcat_tmpdir"
fi


# ==================================================
# install or-tools to /usr/local/
# ==================================================

# downloads or-tools binaries from https://developers.google.com/optimization/install/java/binary_linux
# extracts and copies them to /usr/local/lib/ortools-linux-x86-64/

if [ ! -d /usr/local/lib/ortools-linux-x86-64 ] || [ -z "$(ls -A /usr/local/lib/ortools-linux-x86-64)" ]; then
    ortools_tmpdir=$(mktemp -d)

    wget -O "$ortools_tmpdir/or-tools.tar.gz" \
        https://github.com/google/or-tools/releases/download/v9.12/or-tools_amd64_ubuntu-24.10_java_v9.12.4544.tar.gz

    tar -xzf "$ortools_tmpdir/or-tools.tar.gz" \
        -C "$ortools_tmpdir" \
        or-tools_x86_64_Ubuntu-24.10_java_v9.12.4544/ortools-linux-x86-64-9.12.4544.jar

    unzip -qq -d "$ortools_tmpdir" \
      "$ortools_tmpdir/or-tools_x86_64_Ubuntu-24.10_java_v9.12.4544/ortools-linux-x86-64-9.12.4544.jar" \
      "ortools-linux-x86-64/*"

    sudo cp -r "$ortools_tmpdir/ortools-linux-x86-64" \
        /usr/local/lib/

    rm -rf "$ortools_tmpdir"
fi


# ==================================================
# set up mysql database
# ==================================================

sudo mysql -u root -p < db.sql  # password for mysql root user is blank by default (if unset)
