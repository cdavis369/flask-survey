from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<78412310>'
toolbar = DebugToolbarExtension(app)

SURVEY = satisfaction_survey
RESPONSES = []

@app.route('/')
def landing_page():
  RESPONSES.clear()
  return render_template('start.html', survey=SURVEY)

@app.route('/questions/<int:q>')
def survey(q):
  if q is not len(RESPONSES):
    q = len(RESPONSES)
  if q is len(SURVEY.questions):
    return render_template('/thanks.html')
  return render_template('survey.html', survey=SURVEY, q=q)

@app.route('/next-question/<int:q>')
def next_question(q):
  for choice in SURVEY.questions[q].choices:
    answer = request.args.get(choice)
    if answer:
      RESPONSES.append(choice)
  if len(RESPONSES) < len(SURVEY.questions):
    return render_template('survey.html', survey=SURVEY, q=q+1)
  return render_template('/thanks.html')

@app.route('/thanks')
def answers():
  return render_template('thanks.html')

