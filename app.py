from flask import Flask, render_template, redirect, request, url_for, flash,session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def index():
    return render_template('survey.html', survey=satisfaction_survey)

@app.route('/questions/<int:question_idx>', methods=['GET', 'POST'])
def question(question_idx):
    if question_idx == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    
    if request.method == 'POST':
        response = request.form['response']
        responses.append(response)

    question = satisfaction_survey.questions[question_idx]
    return render_template('survey.html', survey=satisfaction_survey, question=question, question_idx=question_idx)

@app.route('/thankyou')
def thankyou():
    return "Thank you for completing the survey!"

if __name__ == '__main__':
    app.run(debug=True)