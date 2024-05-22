from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client
import os
import gotrue.errors
from dotenv import load_dotenv


load_dotenv()  # Tải các biến môi trường từ file .env


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/signin", methods=["GET", "POST"])
def signin():
    # Lấy dữ liệu từ form HTML
    if request.method == "POST":
        action = request.form.get("action")

        if action == "signin":
            email = request.form["si_email"]
            password = request.form["si_password"]
            try:
                response = supabase.auth.sign_in_with_password(
                    {"email": email, "password": password}
                )
                # app.logger.info(response)
                user_info = response.user
                if user_info:
                    session["email"] = user_info.email  # Lưu email vào session
                    user_id = user_info.id
                    app.logger.info("User id: %s", user_id)
                    # data = supabase.table("test").select("*").execute()
                    # app.logger.info("Table test: %s", data.data)
                    return redirect(url_for("home"))
            except gotrue.errors.AuthApiError as e:
                return f"Đăng nhập thất bại: {e}"
            except Exception as e:
                return f"Lỗi server: {e}"
        elif action == "signup":
            email = request.form["su_email"]
            password = request.form["su_password"]
            try:
                response = supabase.auth.sign_up({"email": email, "password": password})
                user_info = response.user
                app.logger.info(user_info)
                if user_info:
                    return redirect(url_for("home"))
            except gotrue.errors.AuthApiError as e:
                return f"Đăng ký thất bại: {e}"
            except Exception as e:
                return f"Lỗi server: {e}"

    # Xử lý dữ liệu tại đây, ví dụ: in ra console
    return render_template("signin.html")




@app.route("/", methods=["GET", "POST"])
def home():
    print(session)
    movies = (
        supabase.table("phim")
        .select("ten_phim, url_poster, trailer, id")
        .execute()
        .data
    )
    phimsapchieu = (
        supabase.table("phimsapchieu")
        .select("ten_phim, url_poster, trailer, id")
        .execute()
        .data
    )
    app.logger.info(movies)
    if "email" not in session:
        return redirect(url_for("signin"))
    if request.method == "POST":
        action = request.form.get("action")
        # Kiểm tra xem nút "book_tickets" có trong yêu cầu hay không
        if action == "book_ticket":
            # Nếu nút "Đặt vé ngay" được nhấn, chuyển hướng đến tuyến đường "book_ticket"
            return redirect(url_for("book_tickets"))
    return render_template("index.html", movies=movies, phimsapchieu=phimsapchieu)
@app.route("/book_tickets/<int:id_phim>", methods=["GET", "POST"])
def book_tickets(id_phim):
    # Xử lý việc đặt vé ở đây
    return render_template("index2.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    supabase.auth.sign_out()
    session.clear()
    print(session)
    return redirect(url_for("signin"))


if __name__ == "__main__":
    app.run(debug=True)
