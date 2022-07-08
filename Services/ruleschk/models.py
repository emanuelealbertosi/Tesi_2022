from app import db

class Rules(db.Model):
    __tablename__ = "rules"
    
    id = db.Column(db.Integer, primary_key=True)
    rule = db.Column(db.String(300), unique=False, nullable=False)
    isvalid= db.Column(db.Boolean, nullable=False, unique=True)

    def __repr__(self):
        return '%r' % self.rule