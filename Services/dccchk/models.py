from app import db

class Dcc(db.Model):
    __tablename__ = "dcc"
    
    id = db.Column(db.Integer, primary_key=True)
    regulation = db.Column(db.String(150), unique=False, nullable=False)
    isvalid= db.Column(db.Boolean, nullable=False, unique=True)

    def __repr__(self):
        return '<Dcc %r>' % self.username