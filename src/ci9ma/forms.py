from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired


class ShowtimeForm(FlaskForm):
    movie_id = SelectField("Phim", coerce=int, validators=[DataRequired()])
    room_id = IntegerField("ID Phòng", validators=[DataRequired()])
    start_time = TimeField("Thời gian bắt đầu", validators=[DataRequired()])
    ngay_chieu = DateField("Ngày chiếu", validators=[DataRequired()])
    submit = SubmitField("Thêm ca chiếu")
