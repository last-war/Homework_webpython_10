from datetime import datetime

from connector import session
from sqlalchemy import select
import json
from models import Tag, Author, Quote, Quote_tags


def fill_db():
    with open('json/authors.json', 'r', encoding='utf-8') as fh:
        rez = json.load(fh)
        for itr in rez:
            new_author = Author(description=itr['description'],
                                born_date=datetime.strptime(itr['born_date'], '%B %d, %Y').date(),
                                born_location=itr['born_location'], fullname=itr['fullname'])
            session.add(new_author)
        session.commit()
    # tags
    with open('json/quotes.json', 'r', encoding='utf-8') as fh:
        rez = json.load(fh)
        unique_tags = set()
        for itr in rez:
            for cur_tag in itr['tags']:
                unique_tags.add(cur_tag)
    for unique_tag in unique_tags:
        session.add(Tag(name=unique_tag))
    session.commit()

    with open('json/quotes.json', 'r', encoding='utf-8') as fh:
        rez = json.load(fh)
        for itr in rez:
            id_author = session.scalars(select(Author.id).where(Author.fullname == itr['author'])).all()
            new_quote = Quote(author_id=id_author, quote=itr['quote'])
            session.add(new_quote)
            session.commit()
            id_quote = session.scalars(select(Quote.id).where(Quote.quote == itr['quote'])).all()
            for cur_tag in itr['tags']:
                ids_tag = session.scalars(select(Tag.id).where(Tag.name == cur_tag)).all()
                session.add(Quote_tags(quote_id=id_quote, tag_id=ids_tag))
            session.commit()

    session.close()

fill_db()