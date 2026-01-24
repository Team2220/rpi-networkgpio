#!/bin/bash

# Prompt the user for the software they want to set up
echo "Which software do you want to set up? (ledout, sensorin, stacklights)"
read -r software

# Validate the input
if [[ "$software" != "ledout" && "$software" != "sensorin" && "$software" != "stacklights" ]]; then
    echo "Invalid choice. Please choose from ledout, sensorin, or stacklights."
    exit 1
fi

# Define the folder path
software_folder="/Users/schristianson/Documents/GitHub/rpi-networkgpio/$software"

# Create the virtual environment
echo "Setting up virtual environment in $software_folder..."
python3 -m venv "$software_folder/venv"

# Activate the virtual environment and install dependencies
source "$software_folder/venv/bin/activate"
if [[ -f "$software_folder/requirements.txt" ]]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r "$software_folder/requirements.txt"
else
    echo "No requirements.txt found in $software_folder. Skipping dependency installation."
fi
deactivate

# Set up the start.sh script in the main folder
start_script="./start.sh"
echo "Creating start.sh in the main folder..."
cat > "$start_script" <<EOL
#!/bin/bash
source "$software_folder/venv/bin/activate"
python "$software_folder/main.py"
deactivate
EOL

# Make start.sh executable
chmod +x "$start_script"

echo "Setup complete. You can now run ./start.sh to start the $software software."