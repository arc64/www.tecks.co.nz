# Steps to memorialise dads website

- wget the site
  -'''wget -mirror --no-cookies --page-requisites --convert-links --header="User_Agent: Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2" --header="Referer: https://www.google.com" -e robots=off -w 1 --debug www.tecks.co.nz'''
- cut all the unnessessary html from pages with search and replace e.g.
  -'''(?=<div id="viewlet-below-content-body">)((.|\n)*)(?=<\/html>)'''
- crawl site and grab all breadcrumbs in order to create a file of leaf notes to automate folder and file creation for new structure (files in data-processing)
  - create site map (https://www.xml-sitemaps.com/)
  - crawl url list and grab the breadcrummbs for each page (https://www.octoparse.com/)
  - slugify paths to create list of folders to create (google sheets)
  - remove weird line endings when exporting from google sheets
  	-'''dos2unix -n ./file.csv ./modified.csv'''
  - create all files
	  -'''mkdir -p $(<./file-paths.csv)'''
  - create all files
    -'''touch $(<./file-list.csv)'''
- install python (https://medium.com/geekculture/setting-up-python-environment-in-macos-using-pyenv-and-pipenv-116293da8e72)
   - brew install pyenv
   - pyenv install 3.12
   - pyenv local 3.12
   - python --version
   - '''"$(pyenv init --path)"'''
   - ''''pip3 install PyYaml'''
- add yaml to old folder and file structure
- create nav order
- add nav order to old folder and file structure
- copy to new folder and file structure
- seems to be an issue with such deep navigation



- install locally

- run locally

'''bundle exec jekyll serve'''


the-conditions-upon-which-learning-depends/respondent-processes/how-fears-and-anxieties-are-learned-and-unlearned/conditions-necessary-for-the-acquisition-of-a-new-anxiety/fear-response.md

the-conditions-upon-which-learning-depends/respondent-processes/how-fears-and-anxieties-are-learned-and-unlearned/conditions-which-may-affect-the-acquisition-of-new-fear/anxiety-responses.md

the-conditions-upon-which-learning-depends/respondent-processes/how-fears-and-anxieties-are-learned-and-unlearned/conditions-necessary-for-the-extinction-of-conditioned-anxiety/fear-responses.md

the-conditions-upon-which-learning-depends/respondent-processes/how-fears-and-anxieties-are-learned-and-unlearned/conditions-which-may-affect-the-extinction-of-a-conditioned-fear/anxiety-response.md

