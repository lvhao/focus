# -*- coding: utf-8 -*-

import json

from sqlalchemy import Column, Integer, BigInteger, DECIMAL, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://root:@localhost:3306/focus", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class House(Base):
    __tablename__ = "t_house"

    id = Column(BigInteger, primary_key=True)
    house_id = Column(BigInteger)
    house_url = Column(String)
    house_name = Column(String)
    house_price = Column(DECIMAL)
    house_visit_cnt = Column(Integer)
    house_follow_cnt = Column(Integer)
    house_type = Column(String)
    house_area = Column(DECIMAL)
    house_district = Column(String)
    house_build_info = Column(String)

    def __repr__(self):
        return json.dump(self)