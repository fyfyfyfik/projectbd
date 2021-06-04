# https://ru.wikibooks.org/wiki/SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html
DeclarativeBase = declarative_base()


class keys(DeclarativeBase):
    tablename = "keys"

    id = Column('id', Integer, primary_key=True)
    Akey = Column('Akey', String)
    Cname = Column('Cname', String)
    Edate = Column('Edate', String)
    Ktype = Column('Ktype', String)

    def init(self, Akey, Cname, Edate, Ktype):
        self.Akey = Akey
        self.Cname = Cname
        self.Edate = Edate
        self.Ktype = Ktype


def add_keys(file_name="add_key.json"):
    # Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
    # engine = create_engine('postgresql://test:password@localhost:5432/project13')
    engine = create_engine('sqlite:///db.sqlite')
    # Метод create_all создает таблицы в БД , определенные с помощью  DeclarativeBase
    DeclarativeBase.metadata.create_all(engine)
    # Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе
    # bind передаем объект engine
    Session = sessionmaker(bind=engine)
    # Создаем объект сессии из вышесозданной фабрики Session
    session = Session()

    # функция для получения историй из файла, созданного администратором или модератором
    def get_keys():
        with open(file_name, 'r') as f:
            # Парсим джейсон
            keys = json.loads(f.read())
        # Возвращаем данные
        return keys['Akey'], keys['Cname'], keys['Edate'], keys['Ktype']

    # Получаем истории из файла
    keys = get_keys()
    # Создаем новый объект из модели История
    new_key = keys(keys[0], keys[1], keys[2], keys[3])
    # Добавляем
    session.add(new_key)
    # Сохраняем
    session.commit()
    # Закрываем
    session.close()

    print('New keys added')


if __name__ == "main":
    add_keys()