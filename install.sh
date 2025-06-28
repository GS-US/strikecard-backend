
set -e

# no run as root
if [ "$EUID" -eq 0 ]; then
    echo "You should not run install scripts as root"
    exit 1
fi

# check if we are running by piped input by seeing if $0 exists
if [ -f "$0" ]; then
    # check if git is installed, and clone the repo down
    if ! command -v git &> /dev/null; then
        echo "Git could not be found, please install it"
        exit 1
    fi

    # clone the repo down
    git clone https://github.com/GS-US/strikecard-backend.git
    cd strikecard-backend
else
    # cd to the directory of the script
    cd "$(dirname "$0")"
fi

# ACTUAL INSTALLATION

# check if docker and docker-compose are installed
if ! command -v docker &> /dev/null; then
    echo "Docker could not be found, please install it"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose could not be found, please install it"
    exit 1
fi

# run starfish/install.sh 
./starfish/install.sh

# build the docker image
docker-compose build

# make postgres_data and chown it to nobody:nogroup
mkdir -p postgres_data
chown -R nobody:nogroup postgres_data


    