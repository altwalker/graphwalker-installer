"""A simple python script for installing GraphWalker CLI on Linux, MacOS and Windows."""

from pathlib import Path
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

        # if platform.system() == "Windows":
        #     self.args.insert(0, "cmd")

        logger.info("Command: {}".format(self.command))
        logger.info("Args: {}".format(self.args))
        logger.info("CWD: {}".format(self.cwd))

        try:
            logging.info("Running subprocess: '{}'.".format(self.command))
            process = subprocess.Popen(
                self.command if platform.system() == "Windows" else self.args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self.cwd,
                shell=platform.system() == "Windows"
            )
            outs, errs = process.communicate()
        except subprocess.TimeoutExpired:
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

            exitcode = process.returncode
            if not exitcode == 0:
                raise Exception("The command '{}' failed with exit code: {}.".format(self.command, exitcode))

    def _log_output(self, outs, errs):
        if outs:
            for line in outs.decode("utf-8").splitlines():
                logger.debug("[STDOUT] >>> {}".format(line))

        if errs:
            for line in errs.decode("utf-8").splitlines():
                logger.debug("[STDERR] >>> {}".format(line))


def validate_graphwalker_version(version):
    if version == 'latest':
        return

    if not pattern.match(version):
        raise Exception("Invalid GraphWalker version '{}'. The version must use a 'major.minor' pattern (e.g 3.2.1, 3.4.0).".format(version))


def get_files_by_extension(path, extension):
    return [filename for filename in path.iterdir() if filename.suffix == extension]


def clone_graphwalker(path):
    url = "https://github.com/GraphWalker/graphwalker-project.git"

    logger.debug("Clone the GraphWalker repository from: {}".format(url))
    Command("git clone {} {}".format(url, path))


def build_graphwalker(path, version):
    logger.info("Build GraphWalker CLI...")
    logger.debug("Path: {}".format(path))
    logger.debug("Version: {}".format(version))

    if version != "latest":
        logger.info("Checkout to version {}...".format(version))
        try:
            Command("git checkout {}".format(version), cwd=path)
        except:
            raise Exception("No matching version found for GraphWalker version '{}'.".format(version))

    try:
        Command("mvn package -pl graphwalker-cli -am -Dmaven.test.skip", cwd=path)
    except:
        raise Exception("The GraphWalker build processes failed.")

    build_path = path / "graphwalker-cli" / "target"
    jar_file = get_files_by_extension(build_path, ".jar")[0]

    return build_path / jar_file


def create_graphwalker_script(path, jar_path):
    logger.info("Create the GraphWalker CLI script file...")
    logger.debug("Path: {!r}".format(path))
    logger.debug("JAR path: {!r}".format(jar_path))

    jar_file = jar_path.name
    dst = path / jar_file

    logger.info("Move '{}' to '{}'...".format(jar_path, dst))
    shutil.move(jar_path, dst)

    if platform.system() == "Windows":
        script_file = path / "gw.bat"
        logger.info("Create {}...".format(script_file))

        with open(script_file, "w") as fp:
            script_content = [
                "@echo off",
                "java -jar {} %*".format(dst)
            ]
            fp.write('\n'.join(script_content) + '\n')

        Command("setx PATH \"%PATH%;{}\"".format(path))
    else:
        script_file = path / "gw.sh"
        logger.info("Create {}...".format(script_file))

        with open(script_file, "w") as fp:
            script_content = [
                "#!/bin/bash",
                "java -jar ~/.graphwalker/{} \"$@\"".format(dst)
            ]
            fp.write('\n'.join(script_content) + '\n')

        Command("chmod +x {}".format(script_file), cwd=path)
        Command("ln -s {} /usr/local/bin/gw".format(script_file), cwd=path)


def main(version):
    if not version:
        version = "latest"
    validate_graphwalker_version(version)

    if platform.system() == "Windows":
        # path = Path(Path.cwd().anchor) / "graphwalker"
        path = Path.home() / "graphwalker"
    else:
        path = Path.home() / ".graphwalker"

    logger.debug("GraphWalker home directory: {}".format(path))

    path.mkdir(exist_ok=True)
    # os.makedirs(path, exist_ok=True)

    repo_path = path / "graphwalker-project"
    logger.debug("GraphWalker repo directory: {}".format(repo_path))

    clone_graphwalker(repo_path)

    try:
        jar_path = build_graphwalker(repo_path, version)
        logger.debug("GraphWalker jar file: {}".format(jar_path))

        create_graphwalker_script(path, jar_path)
    finally:
        logger.debug("Remove the GraphWalker repo from: {}".format(repo_path))
        # Ignore errors as a quick fix for windows
        shutil.rmtree(repo_path, ignore_errors=True)


if __name__ == '__main__':
    version = ""
    if len(sys.argv) >= 2:
        version = sys.argv[1]

    main(version)
