import flask
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
from passcrack import PassCrack

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "try-to-crack-th1s-passw0rd"


class PasswordForm(FlaskForm):
    password = PasswordField("Enter password here", validators=[DataRequired()])
    submit = SubmitField("Submit Password")


@app.route("/", methods=["GET", "POST"])
def home():
    form = PasswordForm()
    if form.validate_on_submit():
        pass_crack = PassCrack()
        output = pass_crack.crack(form.password.data)
        flask.flash(output)
    return flask.render_template("home.html", form=form)


if __name__ == "__main__":
    app.run()
