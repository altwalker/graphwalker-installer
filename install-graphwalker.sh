#!/bin/bash

validate_grapwalker_version() {
    VERSION=$1
    VERSION_REGEX='^([0-9]+\.){2}([0-9]+)$'

    if [[ ! $VERSION =~ $VERSION_REGEX ]]; then
        echo "ERROR: Invalid GraphWalker version '$VERSION'."
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

    CHECKOUT_STATUS=1
    BUILD_STATUS=1

    if [[ ! "$GRAPWALKER_VERSION" == "latest" ]]; then
        echo ">>> Checkout to v$GRAPWALKER_VERSION..."
        git checkout "$GRAPWALKER_VERSION"
        CHECKOUT_STATUS=$?
    else
        # Build the version from the master branch
        CHECKOUT_STATUS=0
    fi

    if [[ ! $CHECKOUT_STATUS == 0 ]]; then
        echo "ERROR: No matching version found for GraphWalker version '$VERSION'."
        exit 1
    else
        echo ">>> Build GraphWalker CLI..."
        mvn package -pl graphwalker-cli -am
        BUILD_STATUS=$?
    fi

    if [[ ! $BUILD_STATUS == 0 ]]; then
        echo "ERROR: An unexpected error occured while building the GraphWalker CLI."
        exit 1
    else
        echo ">>> Create the gw command...."
        JAR_PATH=`ls graphwalker-cli/target/*.jar | head -n 1`
        JAR_FILE=`basename $JAR_PATH`

        mkdir -p ~/.graphwalker
        mv $JAR_PATH ~/.graphwalker/
        ls ~/.graphwalker/

        echo '#!/bin/bash' > ~/.graphwalker/graphwalker-cli.sh
        echo "java -jar ~/.graphwalker/$JAR_FILE" '"$@"' >> ~/.graphwalker/graphwalker-cli.sh

        chmod +x ~/.graphwalker/graphwalker-cli.sh
        cat ~/.graphwalker/graphwalker-cli.sh
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
