# FEATURE FOR CRAWL DATA ABOUT HaUI

## How to use

> [!IMPORTANT]
>***Install the necessary libraries:***<br>
>``` bash pip install request ```<br>
>``` bash pip install beautifulsoup4 ```<br>

> [!NOTE]
>You need to provide a url_root (ex: https://fit.haui.edu.vn/vn ) to access. :shipit: <br>
>All urls contained in url_root will be collected by [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) and saved to list_link.txt. :cowboy_hat_face:<br>
>All content in the url will be retrieved by [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) and saved into data_proces.txt. :white_check_mark:<br>