let myModal = new bootstrap.Modal(document.getElementById('modal'));

// Reset localStorage
localStorage.setItem('first_time_user', 'true');

const check_first_time_user = () => {

    if (localStorage.getItem('first_time_user') == undefined || localStorage.getItem('first_time_user') == "true") {
        myModal.toggle();
        localStorage.setItem('first_time_user', 'false');
    }

}

check_first_time_user();