function showPassword() {
    let password = document.getElementById("password");

    if (password.getAttribute("type") === "password") {
        password.setAttribute('type', "text");
    } else {
        password.setAttribute('type', "password");;
    }
}

function showPassword1() {
    let password1 = document.getElementById("password1");
    let password2 = document.getElementById("password2");

    if (password1.getAttribute("type") === "password") {
        password1.setAttribute('type', "text");
    } else {
        password1.setAttribute('type', "password");;
    }

    if (password2.getAttribute("type") === "password") {
        password2.setAttribute('type', "text");
    } else {
        password2.setAttribute('type', "password");;
    }
}

function showTrackerForm() {
    document.getElementById('edittrackerform').classList.toggle('d-none');
}

function alertGuest() {
    alert("Need to Log In to edit/save data")
}