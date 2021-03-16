<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** marvelman3284, Python-Password-Manager, marvelman3284, jedimaster2384@gmail.com, Python Password Manager, A CLI based password manager created with python and mysq
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
    <a href="https://github.com/marvelman3284/Python-Password-Manager">
        <img src="images/logo.png" alt="Logo" width="80" height="80">
    </a>
    <h3 align="center">Python Password Manager</h3>
    <p align="center">
        A CLI based password manager
        <br />
        <a href="https://github.com/marvelman3284/Python-Password-Manager"><strong>Explore the docs »</strong></a>
        <br />
        <br />
        <a href="https://github.com/marvelman3284/Python-Password-Manager">View Demo</a>
        ·
        <a href="https://github.com/marvelman3284/Python-Password-Manager/issues">Report Bug</a>
        ·
        <a href="https://github.com/marvelman3284/Python-Password-Manager/issues">Request Feature</a>
    </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
    <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#built-with">Built With</a></li>
            </ul>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li><a href="#installation">Installation</a></li>
            </ul>
        </li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#roadmap">Roadmap</a></li>
        <li><a href="#contributing">Contributing</a></li>
        <li><a href="#license">License</a></li>
        <li><a href="#contact">Contact</a></li>
        <li><a href="#acknowledgements">Acknowledgements</a></li>
    </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### Built With

* [Python](https://python.org)
* [MySQL](https://www.mysql.com/)
* [Stack Overflow](https://stackoverflow.com/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* pip
    ```sh
    python3 -m pip install --upgrade pip
    ```

### Installation

1. Clone the repo
     ```sh
     git clone https://github.com/marvelman3284/Python-Password-Manager.git
     ```
2. Create your virutal enviorment
     ```sh
     python3 -m venv env
     ```
3. Install python packages
     ```sh
     pipenv install && pipenv install-dev
     ```
4. Insert the necessary information to the config file
Make a copy of `config.example.ini` and name it `config.ini`. Fill in each spot.
   * `[Email]`
     * `Email` is the actual email you want to use (example@example.com)
       * This is built to use a gmail email, for anything else you will have to make your own configurations.
       *   > If you are using gmail you __must__ turn on **_Allow Access for Less Secure Apps_** in your email settings
     * `Password` is the password for your email
   * `[MySql]`
     * `Host` is the ip for the server where you are hosting the database. Use `localhost` if the server is hosted on your computer.
     * `User` is the username you use to log into the server.
     * `Password` is the password for your username to log into the server.
     * `Database` is the database which your tables are going to be stored.

5. Duplicate the example files in /data/
    * Copy the files:
      * ```cp /data/key.example.key data/key.key && cp /data/save.example.pickle save.pickle```
      * Or: 
        * ```cd /data```
        * ```cp key.example.key key.key```
        * ```cp save.example.pickle save.pickle```
    * Remove the old ones
      * ```rm data/key.example.key && rm data/save.example.pickle```
      * Or:
        * ```cd /data/```
        * ```rm key.example.key```
        * ```rm save.example.pickle```
6. Generate the needed tables in your MySQL server
    ```sh
    python /src/server.py
    ```


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/marvelman3284/Python-Password-Manager/issues) for a list of known issues.
There is also [The TODO File](https://github.com/marvelman3284/Python-Password-Manager/TODO) which contains a list of features that need to be worked on or are in development. (TODO file is using the [TODO+](https://marketplace.visualstudio.com/items?itemName=fabiospampinato.vscode-todo-plus) vscode extension.) 


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@marvelman3284](https://twitter.com/marvelman3284) - jedimaster2384@gmail.com - Marvelman3284#6554
Project Link: [https://github.com/marvelman3284/Python-Password-Manager](https://github.com/marvelman3284/Python-Password-Manager)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [othneildrew for the README.md template](https://github.com/othneildrew/Best-README-Template/blob/master/BLANK_README.md)
* [Credit to Luiz Rosa on hackernoon for the code in `/src/totp.py`](https://hackernoon.com/implementing-2fa-how-time-based-one-time-password-actually-works-with-python-examples-cm1m3ywt)
* [Credit to Sci Prog on stackoverflow for the validate function in `src/passManager.py`](https://stackoverflow.com/questions/35857967/python-password-requirement-program)
* [Credit to PyTutorials on nitratine for the code snippetes in `src/encrypt.py`](https://nitratine.net/blog/post/encryption-and-decryption-in-python/)
* [Credit to TheOtherUnkown for the flake8 workflow in `/.github/workflows/flake8.yml`](https://github.com/TheOtherUnknown/Malcolm-next/blob/master/.github/workflows/flake8.yml)
* [`.gitignore` from toptal.com](https://www.toptal.com/developers/gitignore/api/python,vscode,archlinuxpackages)
)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/marvelman3284/Python-Password-Manager.svg?style=for-the-badge
[contributors-url]: https://github.com/marvelman3284/Python-Password-Manager/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/marvelman3284/Python-Password-Manager.svg?style=for-the-badge
[forks-url]: https://github.com/marvelman3284/Python-Password-Manager/network/members
[stars-shield]: https://img.shields.io/github/stars/marvelman3284/Python-Password-Manager.svg?style=for-the-badge
[stars-url]: https://github.com/marvelman3284/Python-Password-Manager/stargazers
[issues-shield]: https://img.shields.io/github/issues/marvelman3284/Python-Password-Manager.svg?style=for-the-badge
[issues-url]: https://github.com/marvelman3284/Python-Password-Manager/issues
[license-shield]: https://img.shields.io/github/license/marvelman3284/Python-Password-Manager.svg?style=for-the-badge
[license-url]: https://github.com/marvelman3284/Python-Password-Manager/blob/master/LICENSE.txt
