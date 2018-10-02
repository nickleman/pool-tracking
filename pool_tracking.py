from app import app, db
from app.models import Player, Match, Game

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Player': Player, 'Match': Match,
            'Game': Game}
