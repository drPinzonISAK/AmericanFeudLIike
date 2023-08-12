from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

warm_up = [
    ["Com Sci", 94, False, "Computer science is like magic for machines! The best science"],
    ["Socializing with Friends", 3, False, "I'll really miss seeing my friends every day and just hanging out with them"],
    ["Summer Break", 2, False, "I'll miss the super long break we get during summer. No more worry about school stuff for a while!"],
    ["Lunchtime Chats:", 1, False, "Lunch breaks with my friends are the best. We eat together, chat, and have a great time"]
]

reasons_for_academic_integrity = [
    ["Actually Learning Stuff", 23, False, "Ever felt that \"aha\" moment? Upholding integrity in your studies brings about those lightbulb moments, leading to genuine understanding."],
    ["Being True to You", 14, False, "It's about supporting yourself and staying true to your values. Demonstrating integrity through honesty in your work showcases your commitment to ethical principles."],
    ["Winning in the Long Run", 12, False, "Think marathon, not sprint. Upholding integrity helps you develop skills that lead to winning in the long haul."],
    ["Getting Ready for the Real World", 11, False, "High school is like training for the big leagues (college or whatever's next for you). Integrity now sets you up for success later."],
    ["Building Your Character", 9, False, "Picture it as leveling up in the journey of life. Practicing integrity by being honest portrays you as someone with strong principles and a sense of responsibility"],
    ["Getting Ready for What's Next", 8, False, "High school is like training for the big leagues (college or whatever's next for you). Upholding integrity now sets you up for success later."],
    ["Playing Fair for All", 7, False, "Imagine a fair game where everyone has the same shot. Upholding integrity ensures that nobody's trying to bend the rules."],
    ["Trust Rules", 6, False, "Maintaining integrity fosters trust with your teachers and friends. Trust acts as the magical ingredient that enhances relationships in wonderful ways."],
    ["Being a Cool Citizen", 5, False, "In a world full of choices, choosing Integrity shows you're a responsible and awesome member of society."]
]

score_warmup = [0, 0]
score = [0, 0]

@app.route('/index')
def index():
    return render_template('menu.html')

@app.route('/host')
def host():
    global reasons_for_academic_integrity
    options = reasons_for_academic_integrity
    return render_template('host.html', options=options)

@app.route('/host_warmup')
def host_warmup():
    global warm_up
    options = warm_up
    return render_template('host_warmup.html', options=options)

@app.route('/')
def player():
    global reasons_for_academic_integrity, score
    options = reasons_for_academic_integrity
    return render_template('player.html', options=options, score=score)

@app.route('/warmup')
def warmup():
    global warm_up , score_warmup
    options = warm_up
    return render_template('warmup.html', options=options, score=score_warmup)

@socketio.on('reveal')
def reveal(data):
    global reasons_for_academic_integrity
    id = data['button_id']
    reasons_for_academic_integrity[id][2] = True
    emit('option_updated', {'button_id': id, 'explanation':reasons_for_academic_integrity[id][3]}, broadcast=True)

@socketio.on('revealWarmUp')
def revealWarmUp(data):
    global warm_up
    id = data['button_id']
    warm_up[id][2] = True
    emit('option_updated_warmup', {'button_id': id, 'explanation':warm_up[id][3]}, broadcast=True)


@socketio.on('toggleError')
def toggleError():
    emit('flipError', broadcast=True)

@socketio.on('hideExplanation')
def hideExplanation():
    emit('hideExplanation', broadcast=True)

@socketio.on('addScore')
def addScore(data):
    global score
    score[data['team']] += data['score']
    emit('updateScore',  {'score': score}, broadcast=True)

@socketio.on('addScore_warmup')
def addScore_warmup(data):
    global score_warmup
    score_warmup[data['team']] += data['score']
    emit('updateScore_warmup',  {'score': score_warmup}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
