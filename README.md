# Python 6 Web 
## HomeWork # 04

[![Language](https://img.shields.io/badge/language-python-blue)](https://www.python.org)
[![CodeFactor](https://www.codefactor.io/repository/github/vlodyakr/python-6-web-homework-04/badge)](https://www.codefactor.io/repository/github/vlodyakr/python-6-web-homework-04)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/VlodyaKr/Python-6-Web-HomeWork-04)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/VlodyaKr/Python-6-Web-HomeWork-04)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/VlodyaKr/Python-6-Web-HomeWork-04/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/VlodyaKr/Python-6-Web-HomeWork-04/?branch=main)
[![Build Status](https://scrutinizer-ci.com/g/VlodyaKr/Python-6-Web-HomeWork-04/badges/build.png?b=main)](https://scrutinizer-ci.com/g/VlodyaKr/Python-6-Web-HomeWork-04/build-status/main)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/VlodyaKr/Python-6-Web-HomeWork-04/badges/code-intelligence.svg?b=main)](https://scrutinizer-ci.com/code-intelligence)

---
#### Завдання:

Напишіть програму обробки папки "Хлам", яка сортує файли у вказаній папці по розширенням з використанням декількох потоків. Прискоріть обробку великих каталогів з великою кількістю вкладених папок та файлів за рахунок паралельного виконання обходу всіх папок в окремих потоках. Найбільш витратним за часом буде перенесення файлу та отримання списку файлів у папці (ітерація вмісту каталогу). Щоб прискорити перенесення файлів, його можна виконувати окремому потоці або пулі потоків. Це зручніше, що результат цієї операції ви в додатку не обробляєте і можна не збирати жодних результатів. Щоб прискорити обхід вмісту каталогу з кількома рівнями вкладеності, ви можете обробляти кожен підкаталог виконувати в окремому потоці або передавати обробку в пул потоків.

---
Реалізовано у модулі `file_parser.py`

---
#### Автор
[![GitHub Contributors Image](https://contrib.rocks/image?repo=VlodyaKr/Python-6-Web-HomeWork-04)](https://github.com/VlodyaKr)

#### Володимир Кравченко
[Написати автору листа](mailto:vlodya@gmail.com?subject=Python-6-Web-HomeWork-04)
