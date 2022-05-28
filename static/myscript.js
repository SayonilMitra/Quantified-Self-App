function showPassword() {
    let password = document.getElementById("password");
    let password1 = document.getElementById("password1");
    let password2 = document.getElementById("password2");

    if (password.getAttribute("type") === "password") {
        password.setAttribute('type', "text");
    } else {
        password.setAttribute('type', "password");;
    }

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

function changeForm() {
    showLoginForm();
    showRegisterForm();
}

function showLoginForm() {
    let login_form_visibility = document.getElementById("login_form_main");
    login_form_visibility.classList.toggle("d-none");

}

function showRegisterForm() {
    let register_form_visibility = document.getElementById("register_form_main");
    register_form_visibility.classList.toggle("d-none");
    
}

function showTrackerForm() {
    document.getElementById('edittrackerform').classList.toggle('d-none');
}