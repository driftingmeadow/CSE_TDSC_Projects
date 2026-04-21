#!/bin/bash

# ==================================================
# JalTantra Local Installation Script
# Uses bundled jaltantra_dependencies from jaltantra_dependencies/ folder
# ==================================================

set -e  # Exit on any error

echo "=========================================="
echo "JalTantra Installation (Bundled Mode)"
echo "=========================================="
echo ""

# Check if jaltantra_dependencies folder exists
if [ ! -d "jaltantra_dependencies" ]; then
    echo "ERROR: jaltantra_dependencies/ folder not found!"
    echo "Please ensure jaltantra_dependencies/ folder exists with:"
    echo "  - tomcat9.tar.gz"
    echo "  - ortools-complete.tar.gz"
    exit 1
fi

# ==================================================
# Install system packages
# ==================================================
echo "Step 1: Installing system packages..."
sudo apt update
sudo apt install -y default-jdk
sudo apt install -y mysql-server
sudo systemctl enable mysql --now
sudo apt install -y unzip
echo " System packages installed"
echo ""

# ==================================================
# Install Tomcat from bundled archive
# ==================================================
echo "Step 2: Installing Tomcat from bundled archive..."

if [ -f "jaltantra_dependencies/tomcat9.tar.gz" ]; then
    # Check if /opt/tomcat9 already exists
    if [ -d "/opt/tomcat9" ] && [ "$(ls -A /opt/tomcat9)" ]; then
        echo "WARNING: /opt/tomcat9 already exists!"
        read -p "Remove and reinstall? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo rm -rf /opt/tomcat9
        else
            echo "Skipping Tomcat installation"
        fi
    fi
    
    if [ ! -d "/opt/tomcat9" ] || [ ! "$(ls -A /opt/tomcat9)" ]; then
        # Extract to /tmp first, then move to correct location
        TEMP_DIR=$(mktemp -d)
        sudo tar -xzf jaltantra_dependencies/tomcat9.tar.gz -C "$TEMP_DIR"
        
        # Move from temp location to /opt/tomcat9
        sudo mv "$TEMP_DIR/opt/tomcat9" /opt/tomcat9
        
        # Clean up temp directory
        sudo rm -rf "$TEMP_DIR"
        
        echo " Tomcat installed to /opt/tomcat9/"
    fi
else
    echo " ERROR: jaltantra_dependencies/tomcat9.tar.gz not found!"
    exit 1
fi
echo ""

# ==================================================
# Install OR-Tools from bundled archive
# ==================================================
echo "Step 3: Installing OR-Tools from bundled archive..."

if [ -f "jaltantra_dependencies/ortools-complete.tar.gz" ]; then
    # Check if already exists
    if [ -d "/usr/local/lib/ortools-linux-x86-64" ]; then
        echo "WARNING: /usr/local/lib/ortools-linux-x86-64 already exists!"
        read -p "Remove and reinstall? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo rm -rf /usr/local/lib/ortools-linux-x86-64
        else
            echo "Skipping OR-Tools installation"
        fi
    fi
    
    if [ ! -d "/usr/local/lib/ortools-linux-x86-64" ]; then
        sudo mkdir -p /usr/local/lib/
        sudo tar -xzf jaltantra_dependencies/ortools-complete.tar.gz -C /usr/local/lib/
        echo " OR-Tools installed to /usr/local/lib/ortools-linux-x86-64/"
    fi
else
    echo " ERROR: jaltantra_dependencies/ortools-complete.tar.gz not found!"
    exit 1
fi
echo ""

# ==================================================
# Set up MySQL database
# ==================================================
echo "Step 4: Setting up MySQL database..."
if [ -f "db.sql" ]; then
    echo "Creating database and user..."
    echo "When prompted for MySQL root password, press ENTER (blank password)"
    sudo mysql -u root < db.sql && echo "✓ Database created successfully" || echo " Database setup may have failed"
else
    echo " WARNING: db.sql not found, skipping database setup"
fi
echo ""

# ==================================================
# Verify installations
# ==================================================
echo "=========================================="
echo "Verifying Installation"
echo "=========================================="

echo "Java version:"
java -version 2>&1 | head -1

echo ""
echo "Tomcat:"
if [ -d "/opt/tomcat9/bin" ]; then
    echo "✓ /opt/tomcat9/ exists"
    sudo /opt/tomcat9/bin/version.sh 2>/dev/null | grep "Server version" || echo "  (version check failed)"
else
    echo "✗ /opt/tomcat9/ NOT found"
fi

echo ""
echo "OR-Tools:"
if [ -d "/usr/local/lib/ortools-linux-x86-64" ]; then
    echo "✓ /usr/local/lib/ortools-linux-x86-64/ exists"
    ls /usr/local/lib/ortools-linux-x86-64/libjniortools.so >/dev/null 2>&1 && echo "  ✓ libjniortools.so found" || echo "  ✗ libjniortools.so NOT found"
else
    echo "✗ /usr/local/lib/ortools-linux-x86-64/ NOT found"
fi

echo ""
echo "MySQL:"
systemctl is-active --quiet mysql && echo " MySQL is running" || echo " MySQL is NOT running"

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Set JAVA_HOME:"
echo "   export JAVA_HOME=/usr/lib/jvm/default-java"
echo "   export PATH=\$PATH:\$JAVA_HOME/bin"
echo ""
echo "2. Configure Tomcat for OR-Tools:"
echo "   sudo bash -c 'echo \"export CATALINA_OPTS=\\\"\\\$CATALINA_OPTS -Djava.library.path=/usr/local/lib/ortools-linux-x86-64\\\"\" > /opt/tomcat9/bin/setenv.sh'"
echo "   sudo chmod +x /opt/tomcat9/bin/setenv.sh"
echo ""
echo "3. Add your Google Maps API key for Maps functionalities"
echo ""
echo "4. Compile and deploy:"
echo "   sudo ./compile_and_deploy.sh"
echo ""
echo "5. Access at: http://localhost:8080/jaltantra/"
echo ""
echo "=========================================="