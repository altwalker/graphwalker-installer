#!/bin/bash

echo "Install GraphWalker..."

wget https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.0/graphwalker-cli-4.3.0.jar
mkdir -p ~/.graphwalker
mv graphwalker-cli-4.3.0.jar ~/.graphwalker/
echo -e '#!/bin/bash\njava -jar ~/graphwalker/graphwalker-cli-4.3.0.jar "$@"' > ~/.graphwalker/graphwalker-cli.sh
chmod +x ~/.graphwalker/graphwalker-cli.sh
ln -s ~/.graphwalker/graphwalker-cli.sh /usr/local/bin/gw
