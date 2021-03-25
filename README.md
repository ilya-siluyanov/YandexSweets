<h1>Yandex Sweets project</h1>
<h2>REST API for working with couriers and orders</h2>

<h2>How to install this application?</h2>
<ol>
    <h3>I configured these files on virtual machine so that it works and restarts automatically, but in case of problems...</h3>
    <li>
        download the repository from github
        (git clone https://github.com/ilya-siluyanov/YandexSweets)
    </li>
    <li>
        configure gunicorn_config.py inside YandexSweetsProject directory
        (there are detailed explanation of each line of code)
    </li>
    <li>
        configure start_gunicorn.sh (there are detailed explanation of each line of code)
    </li>
    <li>
        Check whether start_gunicorn.sh is marked as executable  (or mark it by chmod +x start_gunicorn.sh)
    </li>
    <li>
        configure Nginx or use the template in config directory, copy the content of default to /etc/nginx/sites-enabled/default
    </li>
    <li>
        copy gunicorn.service from config directory to /etc/systemd/system directory
    </li>
    <li>
        for postgres user set password postgres
    </li>
    <li>
        create database yandex_database
    </li>
</ol>
<h2>How to launch service?</h2>
Actually, if everything is okay, then it should start on system startup 
<ol>
    <li>
        restart (or start) gunicorn.service
    </li>
    <li>
        restart (or start) nginx.service
    </li>
<h2>How to launch tests?</h2>
<p>Inside of the YandexSweets package execute <code>python3 manage.py test</code></p>
</ol>








<h2>Dependencies</h2>
Nginx, postgresql must be installed
<p>
aiohttp==3.4.4
asgiref==3.3.1
async-timeout==3.0.1
attrs==20.3.0
beautifulsoup4==4.6.3
certifi==2020.12.5
chardet==3.0.4
Django==3.1.7
django-environ==0.4.5
djangorestframework==3.12.2
gunicorn==20.0.4
idna==2.10
multidict==4.7.6
pkg-resources==0.0.0
psycopg2-binary==2.8.6
pydantic==1.8.1
pytz==2021.1
requests==2.25.1
sqlparse==0.4.1
typing-extensions==3.7.4.3
urllib3==1.26.4
yarl==1.6.3
</p>