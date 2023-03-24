from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.orm import relationship
from connector import Base


class Author(Base):
    __tablename__ = 'quotesapp_author'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False, unique=True)
    born_date = Column(DateTime())
    born_location = Column(String(150))
    description = Column(String(1000))


class Tag(Base):
    __tablename__ = 'quotesapp_tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Quote(Base):
    __tablename__ = 'quotesapp_quote'
    id = Column(Integer, primary_key=True)
    author_id = Column('author_id', ForeignKey('quotesapp_author.id', ondelete='CASCADE'))
    quote = Column(String(500))
    author = relationship('Author', back_populates='quotesapp_quote')


class Quote_tags(Base):
    __tablename__ = 'quotesapp_quote_tags'
    id = Column(Integer, primary_key=True)
    quote_id = Column('quote_id', ForeignKey('quotesapp_quote.id', ondelete='CASCADE'))
    quote = relationship('Quote', back_populates='quotesapp_quote_tags')
    tag_id = Column('tag_id', ForeignKey('quotesapp_tag.id', ondelete='CASCADE'))
    tag = relationship('Tag', back_populates='quotesapp_quote_tags')
