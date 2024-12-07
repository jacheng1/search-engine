# Zotsearch

## About this Project

A search engine, built from the ground up, that utilizes a corpus of over 55,000 web pages and achieves results in less than 300 ms. There are two main steps to our search engine: indexing and searching. Indexing is run as a preprocessing step, which creates a lookup table that stores all of the unique tokens found in the corpus, along with the page in which they were located and a weight associated with its relevancy to the page. The search component handles user-defined queries in the search bar, enabling the back-end to scour the index of 55,000 pages to deliver all relevant results to the front-end.



## Built With

* [![Python][python.com]][Python-url]
* [![JavaScript][javascript.com]][JavaScript-url]
* [![HTML][html.com]][HTML-url]
* [![CSS][css.com]][CSS-url]



## Get Started

### Search by Console Interface

```
cd backend
python search.py
```

### Search by Web Interface

In one terminal, execute:
```
cd backend
python api.py
```

In a second terminal, execute:
```
cd frontend
npm run dev
```



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python.com]: https://img.shields.io/badge/logo-python-yellow?logo=python
[Python-url]: https://www.python.org/
[javascript.com]: https://img.shields.io/badge/logo-javascript-blue?logo=javascript
[JavaScript-url]: https://www.javascript.com/
[html.com]: https://img.shields.io/badge/logo-html-blue?logo=html
[HTML-url]: https://www.w3schools.com/html/
[css.com]: https://img.shields.io/badge/logo-css-blue?logo=css
[CSS-url]: https://www.w3.org/Style/CSS/Overview.en.html