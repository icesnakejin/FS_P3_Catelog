from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Item, User
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

Tom = User(name="Tom Cat")
session.add(Tom)

Jerry = User(name="Jerry Mice")
session.add(Jerry)

Basketball = Category(name="Basketball")
session.add(Basketball)

Football = Category(name="Football")
session.add(Football)

Soccer = Category(name="Soccer")
session.add(Soccer)

Boxing = Category(name="Boxing")
session.add(Boxing)

Tennis = Category(name="Tennis")
session.add(Tennis)

NBA = Item(name="NBA",category=Basketball,owner=Jerry)
session.add(NBA)

NCAA = Item(name="NCAA",category=Basketball,owner=Jerry)
session.add(NCAA)

BO = Item(name="BO",
	category=Boxing,
	owner=Tom,
	description="BO is kind of boxing winner wins a number out of a number")
session.add(BO)

KnockDown = Item(name="KnockDown",category=Boxing,owner=Tom)
session.add(KnockDown)

WC = Item(name="World Cup",category=Soccer,owner=Jerry)
session.add(WC)

SB = Item(name="Super Bowl",
	category=Football,
	owner=Tom,
    description="Super Bowl is the final of American Football.")
session.add(SB)

session.commit()

