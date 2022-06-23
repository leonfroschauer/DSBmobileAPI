# DSBmobile API-Wrapper
## About
This package provides a **Python interface** for gathering information from 
[**DSBmobile**](https://www.dsbmobile.de/Login.aspx) a service offered **heinekingmedia**. It is a **scraper** for 
information from the official dsbmobile.de interface.

DSBmobile is a service used by many **German schools** to provide a **substitution plan**, **postings** about 
school relevant information, or **news** published for students. The wrapper provides an easy way to interact with 
this information without directly interacting with the webpage.

## Information about terms used
The main information you can gather consists of these three categories. This table should help to understand how some 
German terms are translated into English and used in code.

| **German**          | **English**           | **Code**    |
|---------------------|-----------------------|-------------|
| **Vertretungsplan** | _substitution plan_   | `plan`      |
| **Aushang**         | _posting_             | `posting`   |
| **News**            | _news_                | `news`      |

