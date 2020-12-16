from app import db, headers
from models import Bill, Member, Subject, PolicyArea, State, Position, BillFollows, User, Party, Session 
from fileread import FileRead
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)

db.drop_all()
# db.create_all()