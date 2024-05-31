from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
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
                print(user)
                if user:
                    session["email"] = user.email  # Lưu email vào session
                    user_data = (
                        supabase.table("users")
                        .select("*")
                        .eq("id", user.id)
                        .execute()
                        .data[0]
                    )
                    print(session.get("email"))
                    session["user"] = {
                        "id": user_data["id"],
                        "email": user_data["email"],
                        "role": user_data["role"],
                    }
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
    if "email" not in session:
        return redirect(url_for("signin"))
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
    return render_template("index.html", movies=movies, phimsapchieu=phimsapchieu)


@app.route("/book_tickets/<int:id_phim>", methods=["GET", "POST"])
def book_tickets(id_phim):
    if "email" not in session:
        return redirect(url_for("signin"))
    response = supabase.table("phim").select("*").eq("id", id_phim).execute()
    movie = response.data[0] if response.data else None
    response_cachieu = (
        supabase.table("cachieu").select("*").eq("id_phim", id_phim).execute()
    )
    cachieu = response_cachieu.data
    app.logger.info(cachieu)
    return render_template(
        "index2.html", movie=movie, cachieu=cachieu, email=session["user"]["email"]
    )


@app.route("/api/get_seats/<int:id_cachieu>")
def get_seats(id_cachieu):
    response = supabase.table("ghe").select("*").eq("id_cachieu", id_cachieu).execute()
    seats = response.data
    return jsonify(seats)


@app.route("/api/get_tickets", methods=["GET"])
def get_tickets():
    if "email" not in session:
        return redirect(url_for("signin"))
    email = session.get("email")
    # Fetch all tickets
    tickets_response = supabase.table("ve").select("*").eq("email", email).execute()
    tickets = tickets_response.data

    # Fetch all showtimes
    showtimes_response = (
        supabase.table("cachieu")
        .select("id_cachieu, id_phim, ngay_chieu, gio_bat_dau")
        .execute()
    )
    showtimes = {
        showtime["id_cachieu"]: showtime for showtime in showtimes_response.data
    }

    # Fetch all movies
    movies_response = supabase.table("phim").select("id, ten_phim").execute()
    movies = {movie["id"]: movie for movie in movies_response.data}

    # fetch seats
    seats_response = supabase.table("ghe").select("id_ghe, hang, cot").execute()
    seats = {seat["id_ghe"]: seat for seat in seats_response.data}

    # Merge the data
    result = []
    for ticket in tickets:
        showtime = showtimes.get(ticket["id_cachieu"])
        if showtime:
            movie = movies.get(showtime["id_phim"])
            seat = seats.get(ticket["id_ghe"])
            if movie:
                ticket_info = {
                    "id_ve": ticket["id_ve"],
                    "id_ghe": ticket["id_ghe"],
                    "hang": seat["hang"],
                    "cot": seat["cot"],
                    "id_giave": ticket["id_giave"],
                    "thanh_tien": ticket["thanh_tien"],
                    "id_cachieu": ticket["id_cachieu"],
                    "ten_phim": movie["ten_phim"],
                    "id_phim": showtime["id_phim"],
                    "ngay_chieu": showtime["ngay_chieu"],
                    "gio_bat_dau": showtime["gio_bat_dau"],
                }
                result.append(ticket_info)
    print("vé: ", result)
    return jsonify(result)


@app.route("/api/delete_ticket", methods=["POST"])
def delete_ticket():
    data = request.json
    id_ve = data.get("id_ve")
    if not id_ve:
        return jsonify({"error": "Missing id_ve, id_ghe"}), 400

    # Lấy thông tin vé để biết id_ghe
    ticket_response = supabase.table("ve").select("id_ghe").eq("id_ve", id_ve).execute()
    if not ticket_response.data:
        return jsonify({"error": "Ticket not found"}), 404
    id_ghe = ticket_response.data[0]["id_ghe"]

    print(id_ve)
    print(ticket_response)
    # Xóa vé từ bảng ve
    supabase.table("ve").delete().eq("id_ve", id_ve).execute()

    # Đặt lại trạng thái ghế thành false trong bảng ghe
    supabase.table("ghe").update({"trang_thai": False}).eq("id_ghe", id_ghe).execute()

    return jsonify({"success": True})


@app.route("/user", methods=["GET"])
def user():
    if "email" not in session:
        return redirect(url_for("signin"))
    return render_template("user.html")


@app.route("/api/get_showtimes/<int:id_phim>")
def get_showtimes(id_phim):
    response = supabase.table("cachieu").select("*").eq("id_phim", id_phim).execute()
    showtimes = response.data
    return jsonify(showtimes)


@app.route("/api/confirm_tickets", methods=["POST"])
def confirm_tickets():
    app.logger.info(session["user"]["email"])
    tickets = request.json
    print(tickets)
    for ticket in tickets:
        supabase.table("ve").insert(ticket).execute()
        supabase.table("ghe").update({"trang_thai": True}).eq(
            "id_ghe", ticket["id_ghe"]
        ).execute()

    return jsonify({"success": True})


@app.route("/logout", methods=["GET", "POST"])
def logout():
    supabase.auth.sign_out()
    session.clear()
    return redirect(url_for("signin"))


def get_movies():
    response = supabase.table("phim").select("id, ten_phim").execute()
    return [(movie["id"], movie["ten_phim"]) for movie in response.data]


@app.route("/admin", methods=["GET", "POST"])
def admin():
    user = session.get("user")
    app.logger.info(user)
    if not user:
        return redirect(url_for("signin"))
    if user.get("role") != "admin":
        return "Bạn không có quyền truy cập trang này", 403
    form = ShowtimeForm()
    # Lấy phim từ supabase
    form.movie_id.choices = get_movies()

    if form.validate_on_submit():
        movie_id = form.movie_id.data
        room_id = form.room_id.data
        start_time = form.start_time.data.strftime(
            "%H:%M:%S"
        )  # Chuyển đổi thời gian thành chuỗi HH:MM:SS
        ngay_chieu = form.ngay_chieu.data.strftime(
            "%Y-%m-%d"
        )  # Chuyển đổi ngày thành chuỗi YYYY-MM-DD
        try:
            result = (
                supabase.table("cachieu")
                .insert(
                    {
                        "id_phim": movie_id,
                        "id_phong": room_id,
                        "gio_bat_dau": start_time,
                        "ngay_chieu": ngay_chieu,
                    },
                )
                .execute()
            )
            id_cachieu = result.data[0]["id_cachieu"]

            # Thêm sẵn các ghế cho ca chiếu được tạo
            # Giả sử mỗi phòng chiếu có 50 ghế, 5 hàng, mỗi hàng 10 ghế
            rows = ["A", "B", "C", "D", "E"]
            cols = range(1, 11)
            seats = []
            for row in rows:
                for col in cols:
                    seat = {
                        "id_cachieu": id_cachieu,
                        "hang": row,
                        "cot": col,
                        "trang_thai": False,
                        "id_loaighe": 1,  # Giả sử loại ghế thường là 1
                    }
                    if row == "E":  # Giả sử hàng E là ghế đôi
                        seat["id_loaighe"] = 2  # Giả sử loại ghế đôi là 2
                    seats.append(seat)

            # Thêm tất cả các ghế vào bảng seats
            supabase.table("ghe").insert(seats).execute()
            flash("Ca chiếu và các ghế đã được thêm thành công!", "success")

        except Exception as e:
            print(f"Error inserting showtime: {e}")
            flash("Có lỗi xảy ra trong quá trình thêm ca chiếu", "error")
            return "Có lỗi xảy ra trong quá trình thêm ca chiếu", 500
        return redirect(url_for("admin"))

    return render_template("admin.html", form=form)

@app.route("/chonrap")
def chonrap():
    return render_template("chonrap.html")

@app.route("/khuyenmai")
def khuyenmai():
    return render_template("khuyenmai.html")

@app.route("/thuesukien")
def thuesukien():
    return render_template("thuesukien.html")

@app.route('/movetocontact', methods=['GET', 'POST'])
def movetocontact():
    return render_template("thuesukienlienhengayform.html")

if __name__ == "__main__":
    app.run(debug=True)
