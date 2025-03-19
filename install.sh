#!/bin/bash

# Ensure the script is run with sudo
if [[ "$EUID" -ne 0 ]]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    
    # Scary!
    rm -rf ./.venv
    
    python3 -m venv ./.venv
    source ./.venv/bin/activate
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    python -m venv .\.venv
    source .\.venv\Scripts\activate
else
    echo "Unsupported OS."
    exit 1
fi

pip install -r ./requirements.txt --quiet
echo '#!/bin/bash' > /bin/mdl
echo 'Automatically setting up the /bin/mdl command. Please make sure you ran as sudo.'
chmod +x /bin/mdl
echo "python3 $(pwd)/main.py \"\$@\"" >> /bin/mdl
echo "Created link: $(realpath ./main.py)"
echo ""
echo "Setup complete. Use 'mdl --help' to run the program."