# Сообщить серверу что команда python тоже самое что команда python3
sudo apt-get install python-is-python3
# Создать в проекте bash файл (start.sh) в котором прописать команды запуска
start.sh
# Создать супер пользователя
adduser userapp  # создать пользователя userapp и группу userapp
sudo usermod -aG sudo username # добавить пользователя в группу суперпользователей
# Создать системного пользователя для запуска служб
sudo adduser --system --no-create-home app_user_demon
# Создать группу для системного пользователя
sudo groupadd app_user_demon # Создать системного пользователя
getent group app_user_demon # Проверить была ли группа создана
# Добавьте системного пользователя в группы
sudo usermod -aG app_user_demon app_user_demon
sudo usermod -aG userapp app_user_demon # Добавить ситемного пользоваателя в группу userapp
# Поcмотреть идентификаторы пользователя и группы
id app_user_demon
id userapp
---------------------------------------------------------------------------
# Зайти на сервер под пользователем userapp
- Установить pyenv
- В pyenv установить python необходимой версии
- Загрузить файлы на сервер
- Создать виртуальное окружение
    python -m venv venv
- Активировать виртуальное окружение
    source venv/bin/activate
- Установить PIP Tools
    pip install pip-tools
- Утсановить зависимости
    pip install -r requirements.txt
---------------------------------------------------------------------------
# В каталоге /etc/systemd/system/ создать файл:
botdemo.service
---------------------------------------------------------------------------
# Проверить права пользователей на файлы и директории проекта
ls -ld /home/DemoTelgramBot  # права доступа к рабочему каталогу
ls -l /home/DemoTelgramBot/venv/bin/python  # права доступа к Python
ls -l /home/DemoTelgramBot/run.py  # права доступа к скрипту
---------------------------------------------------------------------------
# Установите владельца каталога в зависимости от того кого вы прописали в файле сервиса botdemo.service
# Системного пользователя использовать при окончательной публикации проекта
sudo chown -R userapp:userapp /home/DemoTelgramBot 
sudo chown -R app_user_demon:app_user_demon /home/DemoTelgramBot  
---------------------------------------------------------------------------
# предоставьте права чтения/выполнения коталогу проекта
sudo chmod -R u+rX /home/DemoTelgramBot
---------------------------------------------------------------------------
# Перезагрузите конфигурацию systemd
# Включите службу
# Запустите службу
sudo systemctl daemon-reload
sudo systemctl enable botdemo.service
sudo systemctl start botdemo.service
# Остановка службы
sudo systemctl disable botdemo.service
sudo systemctl stop botdemo.service
# Проверка статуса службы
sudo systemctl status botdemo.service

------------------------------------------------------------
# Содержимое файла start.sh

#!/bin/bash
cd /home/DemoTelgramBot/
source venv/bin/activate
python3 run.py

# Содержимое файла botdemo.service

[Unit]
Description=Demo telegram bot
After=network.target

[Service]
Type=simple
User=userapp
WorkingDirectory=/home/DemoTelgramBot/
ExecStart=/home/DemoTelgramBot/start.sh
Restart=on-failure
PrivateTmp=true
ProtectSystem=strict
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target

# Описание содержимого

[Unit]
Description: Описание вашего сервиса, не вызывает конфликтов.
After: Этот параметр указывает, что ваш сервис должен запускаться после определенных таргетов или сервисов. Указание network.target говорит о том, что ваш сервис запускается после подготовки сетевых интерфейсов. Конфликтов здесь нет.
[Service]
Type=simple: Тип запуска процесса. Поскольку этот тип предполагает, что процесс будет рассматриваться как запущенный сразу после старта, убедитесь, что скрипт start.sh не вызывает долгих блокирующих операций, которые могут привести к задержке при запуске сервиса.
User=userapp: Сервис будет запущен от имени определенного пользователя. Нет явных конфликтов, но убедитесь, что пользователь имеет необходимые права доступа к требуемым ресурсам.
WorkingDirectory=/home/DemoTelgramBot/: Рабочий каталог, который используется сервисом. Убедитесь, что пользователь userapp имеет права доступа к этому каталогу и что каталог существует.
ExecStart=/home/DemoTelgramBot/start.sh: Команда для запуска сервиса. Проверьте, что скрипт start.sh имеет правильные права на выполнение и функционирует должным образом.
Restart=on-failure: Указывает, что сервис должен перезапускаться при сбое. Это обычная практика, конфликтов нет.
PrivateTmp=true: Создает отдельный временный каталог для этого сервиса. Это обеспечивает дополнительный уровень безопасности, предотвращая доступ к общим временным файлам. Это хороший параметр, но убедитесь, что сервис не полагается на общие временные файлы с другими сервисами.
ProtectSystem=strict: Ограничивает доступ к системным файлам, разрешая только чтение. Это также хорошая практика для безопасности, но убедитесь, что вашему сервису не требуется записывать системные файлы или каталоги, так как это может вызвать сбои.
NoNewPrivileges=true: Запрещает сервису повышать свои привилегии, что также повышает безопасность. Убедитесь, что вашему сервису не требуется запускать процессы с повышенными привилегиями.
[Install]
WantedBy=multi-user.target: Определяет таргет, который определяет условия запуска сервиса. Нет конфликтов.