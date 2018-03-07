# Coursera Dump

The program collects information about 20 random courses on coursera.org and saves it in an xlsx file.

# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# Quickstart

Example of script launch on Linux and Windows, Python 3.5:

```bash
$ python coursera.py
```

The program displays a processed links of courses in the console:

```bash
1. https://www.coursera.org/learn/transitions-energetiques-pays-du-sud
2. https://www.coursera.org/learn/leadership-skills
3. https://www.coursera.org/learn/internet-of-things-history
4. https://www.coursera.org/learn/ekonomika-dlya-neekonomistov
5. https://www.coursera.org/learn/professional-identity
```

The program saves the name, language, the nearest start date, the number of weeks and the average assessment of the courses in the xlsx-file.
After processing all the links, to save information about the courses, the program will ask for the file name.

```bash
Enter the file name: #Default courses_info.xlsx
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
