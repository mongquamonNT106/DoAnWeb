from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client
import os
import gotrue.errors
from dotenv import load_dotenv
from ci9ma.forms import ShowtimeForm


load_dotenv()  # Tải các biến môi trường từ file .env


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


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
                user = response.user
                if user:
                    session["email"] = user.email  # Lưu email vào session
                    # data = supabase.table("test").select("*").execute()
                    # app.logger.info("Table test: %s", data.data)
                    user_data = (
                        supabase.table("users")
                        .select("*")
                        .eq("id", user.id)
                        .execute()
                        .data[0]
                    )
                    session["user"] = {
                        "id": user_data["id"],
                        "email": user_data["email"],
                        "role": user_data["role"],
                    }
                    app.logger.info(session["user"])
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
                user = response.user
                app.logger.info(user)
                if user:
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
    response = supabase.table("phim").select("*").eq("id", id_phim).execute()
    movie = response.data[0] if response.data else None
    return render_template("index2.html", movie=movie)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    supabase.auth.sign_out()
    session.clear()
    print(session)
    return redirect(url_for("signin"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    user = session.get("user")
    app.logger.info(user)
    if not user:
        return redirect(url_for("signin"))
    if user.get("role") != "admin":
        return "Bạn không có quyền truy cập trang này", 403
    form = ShowtimeForm()
    if form.validate_on_submit():
        movie_id = form.movie_id.data
        room_id = form.room_id.data
        start_time = form.start_time.data.strftime(
            "%H:%M:%S"
        )  # Chuyển đổi thời gian thành chuỗi HH:MM:SS
        ngay_chieu = form.ngay_chieu.data.strftime(
            "%Y-%m-%d"
        )  # Chuyển đổi ngày thành chuỗi YYYY-MM-DD
        print(movie_id)
        print(room_id)
        print(start_time)
        print(ngay_chieu)

        supabase.table("cachieu").insert(
            {
                "id_phim": movie_id,
                "id_phong": room_id,
                "gio_bat_dau": start_time,
                "ngay_chieu": ngay_chieu,
            },
        ).execute()

        return redirect(url_for("admin"))

    return render_template("admin.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
