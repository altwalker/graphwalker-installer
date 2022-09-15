"""A simple python script for installing GraphWalker CLI on Linux, MacOS and Windows."""

import subprocess
import platform
import logging
import shutil
import shlex
import sys
import os
import re


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pattern = re.compile('^([0-9]+\.){2}([0-9]+)$')


class Command:

    def __init__(self, command, cwd=None):
        self.command = command
        self.args = shlex.split(command)
        self.cwd = cwd

        logger.info("Command: {}".format(self.command))
        logger.info("Args: {}".format(self.ards))
        logger.info("CWD: {}".format(self.cwd))

        try:
            logging.info("Running subprocess: '{}'.".format(self.command))
            process = subprocess.Popen(
                self.args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            outs, errs = process.communicate()
        except TimeoutExpired:
            process.kill()
            outs, errs = proc.communicate()
            self._log_output(outs, errs)

            raise
        except Exception as exception:
            logger.error("An unexpected error ocurred while running: '{}'.".format(self.command))
            logger.error(exception)

            raise
        else:
            logger.info("Subprocess '{}' finished.".format(self.command))
            self._log_output(outs, errs)

            exitcode = self.process.returncode
            if not exitcode == 0:
                raise Exception("The command '{}' failed with exit code: {}.".format(self.command, exitcode))

    def _log_output(self, outs, errs):
        for line in outs.split('\n'):
            logger.debug("[STDOUT] >>> {}".format(line))

        for line in errs.split('\n'):
            logger.debug("[STDERR] >>> {}".format(line))


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
    # os.system("git clone {} {}".format(url, path))
    Command("git clone {} {}".format(url, path))


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
    jar_file = get_files_by_extension(build_path, ".jar")[0]

    return os.path.join(path, build_path, jar_file)


def create_graphwalker_script(path, jar_path):
    logger.info("Create the GraphWalker CLI script file...")
    logger.debug("Path: {!r}".format(path))
    logger.debug("JAR path: {!r}".format(jar_path))

    jar_file = os.path.basename(jar_path)
    dst = os.path.join(path, jar_file)

    logger.info("Move {} to {}...".format(jar_file, dst))
    shutil.move(jar_path, dst)

    if platform.system() == "Windows":
        script_file = os.path.join(path, "gw.bat")
        logger.info("Create {}...".format(script_file))

        with open(script_file, "w") as fp:
            fp.write("java -jar {} %*".format(dst))
    else:
        script_file = os.path.join(path, "gw.sh")
        logger.info("Create {}...".format(script_file))

        with open(script_file, "w") as fp:
            fp.writelines([
                "#!/bin/bash",
                "java -jar ~/.graphwalker/{} \"$@\"".format(dst)
            ])

        os.system("chmod +x {}".format(script_file))
        os.system("ln -s {} /usr/local/bin/gw".format(script_file))


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
        jar_path = build_graphwalker(repo_path, version)
        logger.debug("GraphWalker jar file: {}".format(jar_path))

        create_graphwalker_script(path, jar_path)
    finally:
        logger.debug("Remove the GraphWalker repo from: {}".format(repo_path))
        shutil.rmtree(repo_path)


if __name__ == '__main__':
    version = ""
    if len(sys.argv) >= 2:
        version = sys.argv[1]

    main(version)