from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    album_id = Column(String, unique=True)
    album_name = Column(String)
    artist_id = Column(String)
    artist_name = Column(String)
    track_count = Column(Integer)
    last_checked = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True)
    artist_id = Column(String, unique=True)
    artist_name = Column(String)
    track_count = Column(Integer)
    last_checked = Column(DateTime, server_default=func.now(), onupdate=func.now())
