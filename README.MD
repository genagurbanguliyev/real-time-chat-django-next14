# This is real time chat app
Used:
 - `next.js - 14`
 - `Django - 4`
 - `python - ^3.11`
 - `PostgreSQL`

### Front-end:
##### inside `chat_client` folder run commands:
```shell
cd chat_client
npm install
npm run dev
```
***

### Back-end:
##### To Run back-end you need installed to your system:
 - `poetry`
 - `docker`

***

##### If you don't have `poetry`:
 - you can use simple python venv:
    - create python_venv and install all dependencies inside `poetry.toml`


##### If you don't have `docker`:
 - you can install redis to you system and use
***

##### inside `chat_server` folder run commands:
```shell
    cd chat_server
    poetry shell
    poetry install
    ./run.sh
```