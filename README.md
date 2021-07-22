<h1>Yandex Sweets project</h1>
<h2>REST API for working with couriers and orders</h2>
<p>The service uses PostgreSQL for storing data, Nginx for proxing requests to Gunicorn server</p>
<h2>How to install this application?</h2>
<ol>
    <li>
        Install docker on your machine
    </li>
    <li>
        download the repository from github
        (git clone https://github.com/ilya-siluyanov/YandexSweets)
    </li>
    
</ol>
<h2>How to launch service?</h2>
<p>Run docker compose in the project directory</p>
<code>docker compose up -d</code>
<h2>Dependencies</h2>
<ul>
    <li>Docker must be installed</li>
    <li>Server application dependencies are specified in ./server/requirements.txt file</li>
</ul>