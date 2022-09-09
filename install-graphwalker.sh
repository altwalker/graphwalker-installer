#!/bin/bash

validate_grapwalker_version() {
    VERSION=$1
    VERSION_REGEX='^([0-9]+\.){2}([0-9]+)$'

    if [[ ! $VERSION =~ $VERSION_REGEX ]]; then
        echo "Invalid GraphWalker version '$VERSION'."
        echo "The version must use a 'major.minor' pattern (e.g 3.2.1, 3.4.0)."
        exit 1
    fi
}

install_grapwalker() {
    GRAPWALKER_VERSION=$1

    echo "Installing GraphWalker CLI $GRAPWALKER_VERSION..."

    echo ">>> Clone the GraphWalker repository..."
    git clone https://github.com/GraphWalker/graphwalker-project.git
    cd graphwalker-project
    CHECKOUT_STATUS=0

    if [[ ! "$GRAPWALKER_VERSION" == "latest" ]]; then
        echo ">>> Checkout to v$GRAPWALKER_VERSION..."
        git checkout "v$GRAPWALKER_VERSION"
        CHECKOUT_STATUS=$?
    fi

    BUILD_STATUS=1
    if [[ $CHECKOUT_STATUS == 0 ]]; then
        echo ">>> Build GraphWalker CLI..."
        mvn package -pl graphwalker-cli -am
        BUILD_STATUS=$?
    fi

    if [[ $BUILD_STATUS == 0 ]]; then
        echo ">>> Create the gw command...."
        $JAR_PATH = ls graphwalker-cli/target/*.jar | head -n 1
        $JAR_FILE = basename $JAR_PATH

        mkdir -p ~/.graphwalker
        mv $JAR_PATH ~/.graphwalker/

        echo -e '#!/bin/bash\njava -jar ~/.graphwalker/$JAR_FILE "$@"' > ~/.graphwalker/graphwalker-cli.sh
        chmod +x ~/.graphwalker/graphwalker-cli.sh
        ln -s ~/.graphwalker/graphwalker-cli.sh /usr/local/bin/gw
    fi

    echo ">>> Remove the GraphWalker repository..."
    cd ..
    rm -rf graphwalker-project
}


GRAPWALKER_VERSION=$1
if [[ "$GRAPWALKER_VERSION" == "" ]]; then
    GRAPWALKER_VERSION="latest"
elif [[ ! "$GRAPWALKER_VERSION" == "latest" ]]; then
    validate_grapwalker_version $GRAPWALKER_VERSION
fi

install_grapwalker $GRAPWALKER_VERSION


# echo "Download GraphWalker CLI jar..."
# wget https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.0/graphwalker-cli-4.3.0.jar

# echo "Install GraphWalker CLI..."
# mkdir -p ~/.graphwalker
# mv graphwalker-cli-4.3.0.jar ~/.graphwalker/

# echo -e '#!/bin/bash\njava -jar ~/.graphwalker/graphwalker-cli-4.3.0.jar "$@"' > ~/.graphwalker/graphwalker-cli.sh
# chmod +x ~/.graphwalker/graphwalker-cli.sh
# ln -s ~/.graphwalker/graphwalker-cli.sh /usr/local/bin/gw
