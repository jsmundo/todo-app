# routes/learn.py
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Sentence, Flashcard

bp = Blueprint("learn", __name__, url_prefix="/api/learn")

# ---------- GET /next-batch ----------
@bp.route("/next-batch")
@jwt_required()
def next_batch():
    uid   = get_jwt_identity()
    limit = int(request.args.get("limit", 20))
    now   = datetime.now()

    cards = (Flashcard.query
                      .filter_by(user_id=uid)
                      .filter(Flashcard.next_review <= now)
                      .order_by(Flashcard.next_review) 
                      .limit(limit)
                      .all())

    if len(cards) < limit:
        seen = [c[0] for c in
                Flashcard.query.with_entities(Flashcard.sentence_id)
                               .filter_by(user_id=uid)]
        new_sentences = (Sentence.query
                         .filter(~Sentence.id.in_(seen))
                         .order_by(db.func.random())
                         .limit(limit - len(cards))
                         .all())
        for s in new_sentences:
            fc = Flashcard(user_id=uid, sentence_id=s.id)
            db.session.add(fc)
            cards.append(fc)
            if new_sentences:     
               db.session.commit()

    return jsonify([c.serialize() for c in cards])

# ---------- POST /answer ----------
@bp.route("/answer", methods=["POST"])
@jwt_required()
def answer():
    data    = request.get_json(force=True)
    card_id = data["flashcardId"]
    quality = int(data["quality"])     # 0-5

    card = Flashcard.query.get_or_404(card_id)
    card.schedule(quality)
    db.session.commit()
    return jsonify(card.serialize())
