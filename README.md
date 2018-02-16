# Code used to acquire and process the corpus

## Extracting the corpus
[`https://www.poemas-del-alma.com/`](https://www.poemas-del-alma.com/) is a database of anotated poems in Spanish.

Using the [`Scrapy`](https://docs.scrapy.org/en/latest/index.html) Python library, I downloaded 13,167 poems, each one consisting of a title, an author, a body, and a set of related poems.

## `XPath` expressions used for `Scrapy` spider
* **Title of the poem**
`//h2[@class='title-poem']/text()`

* **Body of the poem**
`//div[@class='poem-entry']/p/text()`

* **Author**
`//h3[@class='title-content']/text()`. (Note: use `extract_first()`)

* **Related Poems**
`//div[contains(h3,'Poemas relacionados')]/ul/li/a/text()`

* **Author URLs for a given letter**
`//ul[@class="list-poems"]/li/a/@href`
