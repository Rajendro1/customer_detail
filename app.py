from flask import Flask, session, render_template, url_for, redirect, jsonify, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, Optional, NumberRange

app = Flask(__name__)  # here you don't write __name__ so you got some error


class CustomerForm(FlaskForm):
    ssn_id = StringField('SSN Id',
                         validators=[DataRequired(),
                                     Regexp(r"^[0-9]{9}", message="That SSN ID is not correct! Please check again.")])
    name = StringField('Customer Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    address = TextField('Address', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()],
                        choices=[('', ''), ('mh', 'Maharashtra'), ('ap', 'Andhra Pradesh'),
                                 ('tn', 'Tamil Nadu')])
    city = SelectField('City', validators=[DataRequired()],
                       choices=[('', '')])
    submit = SubmitField('Submit')


city_option = {
    'Maharashtra': [('', ''), ('mb', 'Mumbai'), ('navi-m', 'Navi Mumbai'), ('pne', 'Pune'), ('nsk', 'Nashik')],
    'Andhra Pradesh': [('', ''), ('hyd', 'Hyderabad'), ('nzb', 'Nizamabad'), ('vizag', 'visakhapatnam')],
    'Tamil Nadu': [('', ''), ('ch', 'Chennai'), ('co', 'Coimbatore'), ('ma', 'Madurai')]
}


# @app.route("/")
@app.route('/create-customer', methods=['GET', 'POST'])
def create_customer():
    form = CustomerForm()
    session['state'] = form.state.choices
    if form.validate_on_submit():
        flash('Successfully created customer', 'success')  # here you have error because you don't import flash
        return redirect(url_for('exec.home'))
    return render_template('create_customer.html', form=form)


@app.route('/city/<state>')
def city(state):
    state_selected = dict(session['state']).get(state)
    cities = city_option[state_selected]
    for city in cities:
        cityObj = {}
        cityObj['id'] = city[0]
        cityObj['name'] = city[1]
        city.append(cityObj)
    return jsonify({'cities': city_option})


if __name__ == '__main__':
    app.run(debug=True)
