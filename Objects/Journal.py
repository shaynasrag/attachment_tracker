from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from Objects.Submission import Submission
from Objects.Exceptions import IncorrectResponse
from Static.static import add_and_commit
from Objects.Entry import Base

class Journal(Base):
    __tablename__ = "journal"
    _submissions = relationship("Submission")
    _id = Column(Integer, primary_key = True)
    _people = relationship("People")
    _name = Column(String)
    _start_date = Column(String)
 
    def add_submission(self, session):
        new_submission = Submission()
        self._submissions.append(new_submission)
        add_and_commit(session, [new_submission])
        return new_submission
    
    def get_submissions(self):
        return self._submissions
    
    def get_submission(self, index):
        return self._submissions[index]
    
    def get_people(self):
        return [p._person for p in self._people]
    
    def add_person(self, name):
        if name not in self.get_people():
            person = People(name)
            self._people.append(person)
            return person
        return None

    def person_exists(self, person):
        if person in self.get_people():
            return person
        elif person.lower() == "new person":
            return False
        else:
            raise IncorrectResponse(self.get_people())    
    
class People(Base):
    __tablename__ = "people"
    _journal_id = Column(Integer, ForeignKey("journal._id"))
    _people_id = Column(Integer, primary_key = True)
    _person = Column(String)

    def __init__(self, person):
        self._person = person