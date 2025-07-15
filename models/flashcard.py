# models/flashcard.py  ── progreso individual
from datetime import datetime, timedelta
from models import db

class Flashcard(db.Model):
    __tablename__ = "flashcard"
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    sentence_id  = db.Column(db.Integer, db.ForeignKey("sentence.id"), nullable=False)

    # repetición espaciada (SM-2)
    ease         = db.Column(db.Float, default=2.5)
    interval     = db.Column(db.Integer, default=1)   # días
    repetitions  = db.Column(db.Integer, default=0)
    next_review  = db.Column(db.DateTime, default=datetime.now)

    user     = db.relationship("User", back_populates="flashcards")
    sentence = db.relationship("Sentence")

    # utilidades opcionales
    def schedule(self, quality: int):
        """Actualiza ease/interval/next_review según la puntuación 0-5."""
        if quality < 3:
            self.repetitions = 0
            self.interval = 1
        else:
            self.repetitions += 1
            self.ease = max(1.3, self.ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
            if self.repetitions == 1:
                self.interval = 1
            elif self.repetitions == 2:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease)
        self.next_review = datetime.now() + timedelta(days=self.interval)

    def serialize(self):
        """Devuelve la flashcard con los campos de Sentence a nivel superior."""
        s = self.sentence        # alias corto
        return {
            "id":           self.id,
            # 👇  campos que el frontend espera
            "text_en":      s.text_en,
            "text_es":      s.text_es,
            "audio_url":    s.audio_url,
            # 👇  resto de datos de repetición espaciada
            "ease":         self.ease,
            "interval":     self.interval,
            "repetitions":  self.repetitions,
            "next_review":  self.next_review.isoformat(),
        }
