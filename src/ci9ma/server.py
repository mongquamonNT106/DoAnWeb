from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()  # Tải các biến môi trường từ file .env


SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/signin', methods=["GET", "POST"])
def hello_world():
    # Lấy dữ liệu từ form HTML
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'signin':
            email = request.form['si_email']
            password = request.form['si_password']
            response = supabase.auth.sign_in_with_password(
                {"email": email, "password": password})
            user_info = response.user

            if user_info:
                session['email'] = user_info.email  # Lưu email vào session
                user_id = user_info.id
                print(user_id)
                data = supabase.table('test').select('*').execute()
                print(data.data)
                return redirect(url_for("hello"))
            return 'Đăng nhập thất bại'
            # try:
            #     user = supabase.auth.sign_in_with_password(
            #         {"email": email, "password": password})
            #     if user:
            #         user_info = user.get('user')
            #         user_id = user_info.get('id')
            #         print(user_id)
            #         data = supabase.table('test').select('*').execute()
            #         print(data)
            #         return redirect(url_for("hello"))
            # except:
            #     return 'Đăng nhập thất bại'

        elif action == 'signup':
            email = request.form['su_email']
            password = request.form['su_password']
            try:
                response = supabase.auth.sign_up(
                    {"email": email, "password": password})
                user_info = response.user

                print(user_info)
                if user_info:
                    return redirect(url_for(""))
            except Exception as e:
                return 'Đăng ký thất bại'

    # Xử lý dữ liệu tại đây, ví dụ: in ra console
    return render_template('signin.html')


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        action = request.form.get('action')
        # Kiểm tra xem nút "book_tickets" có trong yêu cầu hay không
        if action == 'book_ticket':
            # Nếu nút "Đặt vé ngay" được nhấn, chuyển hướng đến tuyến đường "book_ticket"
            return redirect(url_for('book_ticket'))
    return render_template('index.html')


@app.route("/book_ticket", methods=["GET", "POST"])
def book_tickets_route():
    # Xử lý việc đặt vé ở đây
    return render_template('index2.html')


if __name__ == '__main__':
    app.run(debug=True)
