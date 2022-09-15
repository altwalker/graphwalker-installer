import platform
import logging
import shutil
import sys
import os
import re


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pattern = re.compile('^([0-9]+\.){2}([0-9]+)$')


def validate_graphwalker_version(version):
    if version == 'latest':
        return

    if not pattern.match(version):
        raise Exception("Invalid GraphWalker version '{}'. The version must use a 'major.minor' pattern (e.g 3.2.1, 3.4.0).".format(version))


def get_files_by_extension(path, extension):
    return [filename for filename in os.listdir(path) if filename.endswith(extension)]


def clone_graphwalker(path):
    url = "https://github.com/GraphWalker/graphwalker-project.git"

    logger.debug("Clone the GraphWalker repo from: {}".format(url))
    os.system("git clone {} {}".format(url, path))


def build_graphwalker(path, version):
    os.chdir(path)

    if version != "latest":
        status = os.system("git checkout {}".format(version))

        if not status == 0:
            raise Exception("No matching version found for GraphWalker version '{}'.".format(version))

    status = os.system("mvn package -pl graphwalker-cli -am")
    logger.debug("Build status: {}".format(status))

    if not status == 0:
        raise Exception("The GraphWalker build processes failed with status code: '{}'.".format(status))

    build_path = "graphwalker-cli/target/"
    return get_files_by_extension(build_path, ".jar")[0]


def create_graphwalker_script(path, jar_file):
    logger.debug("Create the GraphWalker script.")


def main(version):
    if not version:
        version = "latest"
    validate_graphwalker_version(version)

    path = os.path.expanduser("~/.graphwalker") if platform.system() != "Windows" else os.path.expanduser("C:\graphwalker")
    logger.debug("GraphWalker home directory: {}".format(path))

    os.makedirs(path, exist_ok=True)

    repo_path = os.path.join(path, "graphwalker-project")
    logger.debug("GraphWalker repo directory: {}".format(repo_path))

    clone_graphwalker(repo_path)

    try:
        jar_file = build_graphwalker(repo_path, version)
        logger.debug("GraphWalker jar file: {}".format(jar_file))

        create_graphwalker_script(path, jar_file)
    finally:
        logger.debug("Remove the GraphWalker repo from: {}".format(repo_path))
        shutil.rmtree(repo_path)


if __name__ == '__main__':
    version = ""
    if len(sys.argv) >= 2:
        version = sys.argv[1]

    main(version)
