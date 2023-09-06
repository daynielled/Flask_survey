from flask import Flask, render_template, redirect, request,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



@app.route('/')
def show_survey_start():
    """Show the survey start page"""

    return render_template('survey.html', survey=survey)

@app.route("/begin", methods= ["POST"])
def start_survey():
    """Clear any responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route('/answer', methods = ["POST"])
def handle_question():
    """Save answer and move to next question"""


    choice = request.form['answer']

    # Adding responses to session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/thankyou")
    
    else:
        return redirect(f"/questions/{len(responses)}")
    


@app.route('/questions/<int:question_idx>')
def show_question(question_idx):
    """Show questions"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
         return redirect("/thankyou")
    
    if (len(responses) != question_idx):
        flash(f"Invalid question id: {question_idx}.")
        return redirect(f"/questions/{len(responses)}")
      
    question = survey.questions[question_idx]
    return render_template('question.html', question=question, question_idx=question_idx)


@app.route('/thankyou')
def thankyou():
    """Survey completion  page"""
    return "Thank you for completing the survey!"

