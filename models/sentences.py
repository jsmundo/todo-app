

from models import db

class Sentence(db.Model):
    __tablename__ = "sentence"
    id = db.Column(db.Integer, primary_key=True)
    text_en = db.Column(db.String(255), nullable=False)
    text_es = db.Column(db.String(255), nullable=False)
    audio_url = db.Column(db.String(255), nullable=True)
   

    def serialize(self):
        return {
            "id": self.id,
            "text_en": self.text_en,
            "text_es": self.text_es,
            "audio_url": self.audio_url,
        }