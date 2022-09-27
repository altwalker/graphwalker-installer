# graphwalker-installer

Python scripts for installing [GraphWalker](https://graphwalker.github.io/) CLI on Linux, MacOS and Windows.

## Usage

To install GraphWalker on:

* **Linux/MacOS** you can run the following command:

    ```bash
    $ curl -L https://raw.githubusercontent.com/altwalker/graphwalker-installer/main/install-graphwalker.py
    $ python install-graphwalker.py
    ```

    Or:

    ```bash
    $ wget -q -O - https://raw.githubusercontent.com/altwalker/graphwalker-installer/main/install-graphwalker.sh | sh
    $ python install-graphwalker.py
    ```

    Or:

    ```bash
    $ git clone https://github.com/altwalker/graphwalker-installer.git
    $ cd graphwalker-installer
    $ python install-graphwalker.py
    ```

* **Windows** you can run the following commands:

    ```cmd
    > git clone https://github.com/altwalker/graphwalker-installer.git
    > cd graphwalker-installer
    > python install-graphwalker.py
    ```

After installing GraphWalker check that you installed the correct version:

```
$ gw --version
org.graphwalker version: 4.3.1-6273494
...
```

You can also install a specific version of GraphWalker by running `python install-graphwalker.py <version>` (e.g. `python install-graphwalker.py 4.3.1`).

## License

This project is licensed under the [MIT License](LICENSE).