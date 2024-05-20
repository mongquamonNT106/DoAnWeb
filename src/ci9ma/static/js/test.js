const buyTicket = () => {
    // get select seat in div id 'seat'
    const selected = []
    const rows = ['A', 'B', 'C', 'D', 'E']
    rows.forEach((row) => {
        for (let i = 1; i <= 10; i++) {
            const seat = document.getElementById(row + i)
            if (seat.style.backgroundColor === 'green') {
                selected.push(row + i)
            }
        }
    
    })
    alert(selected.join(', ') + ' đã được chọn')

}

const handleSelect = (seat) => {
    const seatElement = document.getElementById(seat)
    if (seatElement.style.backgroundColor === 'white') {
        seatElement.style.backgroundColor = 'green'
        selected.push(row + i)
    } else {
        seatElement.style.backgroundColor = 'white'
        selected.splice(seatSelected.indexOf(row + i), 1)
    }
}

const handleSeatSelect = () => {
    //get set select form server
    const selectedSeats = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
    selectedSeats.forEach((seat) => {
        document.getElementById(seat).style.backgroundColor = 'red'
        document.getElementById(seat).onclick = () => {
            alert('Ghế đã được chọn')
        }
    })
}


const setUp = () => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id = urlParams.get('id')

    if (!id) return;

    // get data from server
    const movie = {
        name: id,
        image: 'https://cdn.galaxycine.vn/media/2024/4/26/roundup-500_1714102279125.jpg',
        date: ['01/04', '02/04', '03/04'],
        price: 75000,
    }

    document.getElementById('movie_content_name').innerText = movie.name
    document.getElementById('movie_content_image').src = movie.image

    const movieDate = document.getElementById('movie_date')
    movie.date.forEach((date) => {
        const str = `
        <div class="box" style="width: 80px; margin: 0px 5px;">
            <p style="font-weight: bold; width: 100px; text-align: center;">${date}</p>
            <p style="font-weight: lighter; width: 100px; text-align: center;">Thu ${new Date().getDay()}</p>
        </div>
        `
        movieDate.insertAdjacentHTML('beforeend', str)
    })
    

}

setUp()


handleSeatSelect()