#!/bin/bash


# ==================================================
# compile project
# ==================================================

cp lib/*.jar WebContent/WEB-INF/lib/
find src \
    -name "*.java" \
    -exec \
        javac -g \
            -d WebContent/WEB-INF/classes \
            -sourcepath src \
            -cp "lib/*:WebContent/WEB-INF/lib/*" \
            {} +


# ==================================================
# copy files to tomcat dir and restart
# ubuntu only
# ==================================================

sudo rm -rf /opt/tomcat9/webapps/jaltantra/
sudo cp -r WebContent /opt/tomcat9/webapps/jaltantra/

# ubuntu
sudo -E /opt/tomcat9/bin/shutdown.sh
sleep 3
# sudo -E /opt/tomcat9/bin/startup.sh
export JPDA_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=8123"  # debugger can attach on port 8213 (jdb -attach 8123)
sudo -E /opt/tomcat9/bin/catalina.sh jpda start  # start in debug mode


# ==================================================
# copy files to tomcat dir and restart
# arch only
# ==================================================

# sudo rm -rf /usr/share/tomcat9/webapps/jaltantra/
# sudo cp -r WebContent /usr/share/tomcat9/webapps/jaltantra/
# sudo chown -R tomcat9:tomcat9 /usr/share/tomcat9/webapps/jaltantra/

# sudo -E /usr/share/tomcat9/bin/shutdown.sh
# sleep 3
# # sudo /usr/share/tomcat9/bin/startup.sh
# export JPDA_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=8123"  # debugger can attach on port 8213 (jdb -attach 8123)
# sudo -E /usr/share/tomcat9/bin/catalina.sh jpda start  # start in debug mode
