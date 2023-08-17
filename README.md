# pyqt-google-image-crawler
Crawling image files from Google search result with Python and icrawler

## Requirements
* PyQt5 >= 5.14 - for GUI support
* icrawler - main package which used for crawling
* beautifulsoup4 - essential package for using icrawler

You can run this with clone this repo and install all packages with run
```
pip install -r requirements.txt
```
and run
```
python main.py
```

That's it, then you can see the result like below.

## Explanation
![image](https://github.com/yjg30737/pyqt-google-image-crawler/assets/55078043/cd064872-58fc-4342-9201-87dee505608a)

As you see you can set parameters such as maximum length, color(including transparent), language.

For who don't understand "color" item of the color parameter - "color" means "any color" here.

Bottom portion of the window, you can add your crawling image's topic to the list. Then pressing the run button, it will keep crawling until task is over!

![image](https://github.com/yjg30737/pyqt-google-image-crawler/assets/55078043/3115a6c0-650e-4f7d-abea-3b98f310429e)

![image](https://github.com/yjg30737/pyqt-google-image-crawler/assets/55078043/d9d0db86-71f0-4efb-a4c1-c912074acb31)

You can run this as a background application too. Crawling is very time-consuming job usually so i decided to support that feature 

for who wants to get rid of this from foreground.

By the way i'm using icrawler in very basic way. It's not good for collecting massive amount of image, but i'm sure this can give you an idea.

After all Google Image search is one of the accessible image storage in the Internet. Even though this icrawler has some flaws.
