# Steps to memorialise dads website

- wget the site

'''wget -mirror --no-cookies --page-requisites --convert-links --header="User_Agent: Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2" --header="Referer: https://www.google.com" -e robots=off -w 1 --debug www.tecks.co.nz'''

- cut all the unnessessary html from pages with search and replace e.g.

'''(?=<div id="viewlet-below-content-body">)((.|\n)*)(?=<\/html>)'''