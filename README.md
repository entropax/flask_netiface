<h1>Flask netiface</h1>

>*Преа́мбула: в связи со спецификой условий выполнения задачи, код далее написан исходя из  следующих принципов:*
>   - *Сначала функционал, потом оптимизация.*
>   - *Есть недостатки о которых будет написано ниже*
>   - *Стили настолько ужасны, насколько это может быть*
>
> *Автор репозитОрия понимет, что его код далек от идеала и во многом не соответствет принципу DRY поэтому будет рад воспринимать любою критику кода.*

<!-- [_TOC_] -->
- [Description](#description)
- [Install](#install)
- [Usage](#usage)
- [Note](#note)

## Description ##
### The code is written according to the task by [«АЭРОДИСК»](https://aerodisk.ru/)
**Задание:**<br>
Необходимо реализовать веб-приложение на Python для управления сетевыми
интерфейсами локальной машины с установленной ОС Linux посредством
команды ip addr. \
Фреймворк можно использовать на выбор (Django/Flask/FastAPI).
Приложение должно содержать следующий набор функционала.
(Для веб, использовать можно любой фреймворк, или нативный JS):
- Авторизация пользователя;
- Включение/выключение сетевого интерфейса;
- Добавление IP адреса;
- Удаление IP адреса;
- Изменение IP адреса;
- Изменение маски подсети.
- Разместить публичный проект с приложением на своём аккаунте Github. Приветствуется документация по развертке и эксплуатации  приложения.*

## Install ##
<br>
**To install run one of these block in terminal emulator on Linux-machine**

- with *venv* and *pip* requirements:
```
git clone https://github.com/entropax/flask_netiface && \
cd flask_netiface && \
python3 -m venv ./.venv && source .venv/bin/activate && \
python3 -m pip install --user --upgrade pip && pip install -r requirements.txt`
```
- if you use poetry:
```
git clone https://github.com/entropax/flask_netiface && \
cd flask_netiface && \
poetry install
```

## Usage ##
**To start web-ap run one of these block in terminal emulator on Linux-machine**
1.
- with poetry:
```sh
poetrry run flask --app flask_netiface run -p 5050
```
- OR with make:
```sh
make run
```
NEXT open this [link](`http://127.0.0.1:5005/`) in web-browser<br>

Here You can see Network-interfaces table,<br>
For further manipulation with Network interfaces You need to authorize in the App.<br>
For authorization You need to input Your sudo password into correspondig login form.<br>
After that You're about to control Network interfaces with buttons<br>
### Authorization

### **You could**
- turn ON/OFF Network Interface;
- add IP address;
- delete IP adress;
- change IP adress;
- change Subnetwork; WITH LIMITATIONS




----
----
### Note
Изменение маски подсети работает некорректно.
