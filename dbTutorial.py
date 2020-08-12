from sqlalchemy import create_engine, Column, Integer, String, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///temporary.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="addresses")

User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

Base.metadata.create_all(engine)

johnUser = User(name="John", fullname = "John Smith", nickname = "Johnny Boy")
alex = User(name="Alex", fullname = "Alex Deus", nickname = "Al")
mila = User(name="Mila", fullname = "Mila Deus", nickname = "butthead")

addList = [johnUser, alex, mila]

session.add_all(addList)
session.commit()