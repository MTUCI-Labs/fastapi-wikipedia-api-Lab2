from fastapi import FastAPI
from models import PageOptions
import wikipedia
import uvicorn


app = FastAPI()
wikipedia.set_lang("ru")


@app.get('/search/{object}')
async def search(object: str, number_of_answers: int = 2):
    """
    Обрабатывает GET-запрос и возвращает результаты поиска.
    Передайте объект поиска в object (path) и количество результатов в number_of_answers (query).
    """
    return wikipedia.search(object, results=number_of_answers)


@app.get('/summary/{object}')
async def summary(object: str):
    """
    Извлекает резюме статьи из Википедии, используя метод summary().
    Статья, для которой необходимо извлечь сводку, передается в path.
    """
    try:
        return ' '.join(wikipedia.summary(object).split('\n'))
    except Exception as e:
        c = str(e).split(
            "lis = BeautifulSoup(html).find_all('li')")[-1].split('\n')[1:]
        return f'{object} may refer to: ' + ', '.join(c)


@app.post('/')
async def page(option: PageOptions):
    """
    Извлекает различные элементы страницы.
    В параметр PageName передайте название нужной вам страницы.
    Вы можете использовать content, url, references, title, categories, links для параметра PageOption, получая разные фрагменты страницы.
    По умолчанию content.
    """

    if option.PageOption == 'content':
        return ' '.join(wikipedia.page(option.PageName).content.split('\n'))
    elif option.PageOption == 'url':
        return wikipedia.page(option.PageName).url
    elif option.PageOption == 'references':
        return wikipedia.page(option.PageName).references
    elif option.PageOption == 'title':
        return wikipedia.page(option.PageName).title
    elif option.PageOption == 'categories':
        return wikipedia.page(option.PageName).categories
    elif option.PageOption == 'links':
        return wikipedia.page(option.PageName).links
    else:
        return "Произошла ошибка"


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
