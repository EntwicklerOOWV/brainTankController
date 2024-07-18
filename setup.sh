#!/bin/bash

# Ensure the script is run with root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Get the username of the user running the script
USER=$(logname)

# Define the project and virtual environment directories
USER_DIR="/home/$USER"
PROJECT_ROOT_DIR="/home/$USER/brainTankController"
VENV_DIR="/home/$USER/venv"
FINAL_PROJ_ROOT_DIR="/home/$USER/venv/brainTankController"

# Navigate to the directory containing the project
cd $USER_DIR

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

# Copy the entire repo into the venv directory
echo "Moving the project to the virtual environment directory..."
mv $PROJECT_ROOT_DIR $FINAL_PROJ_ROOT_DIR

#Navigate to the virtual environment directory
cd $VENV_DIR

#Activate the virtual environment
source bin/activate

# Install requirements in the virtual environment
echo "Installing requirements..."
cd $FINAL_PROJ_ROOT_DIR
pip install -r requirements.txt

# Replace <ersetzen> with the user name in the service file
echo "Configuring the service file..."
sed -i "s|<ersetzen>|$USER|g" oowv-controller.service

# Move the service file to the systemd directory
echo "Moving the service file to /etc/systemd/system..."
mv oowv-controller.service /etc/systemd/system/oowv-controller.service

# Reload systemd daemon and enable the service
echo "Reloading systemd daemon and enabling the service..."
systemctl daemon-reload
systemctl enable oowv-controller.service

# Start the service
echo "Starting the service..."
systemctl start oowv-controller.service

echo "Setup completed successfully!"
