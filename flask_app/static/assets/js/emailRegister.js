let formValidation = document.getElementById("formValidation");
let formValidationLogin = document.getElementById("formValidationLogin");
let is_valid = false;
let login_validation = true;
let pass_valid = true;

// REGISTER CHECKINGS
function check_email() {
    let email = document.forms["formValidation"]["email"].value;
    let regex = new RegExp("[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]");
    if (getUser(email)) {
        document.getElementById("emailError").innerHTML = "";
        is_valid = true
    }
}

async function getUser(email) {
    fetch("http://127.0.0.1:5000/getUser")
        .then((response) => response.json())
        .then((data) => {
            for (i = 0; i < data.length; i++) {
                if (email == data[i]["email"]) {
                    document.getElementById("emailError").innerHTML = "This email already exists!*";
                    is_valid = false;
                } else {
                    is_valid = true;
                }
            }
        });
    return is_valid;
}

// LOGIN CHECKINGS
function check_email_login() {
    let emailLogin = document.forms["formValidationLogin"]["email"].value;
    let regex = new RegExp("[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]");
    if (emailLogin.length == 0) {
                document.getElementById("emailErrorLogin").innerHTML = "Email is required!*";
                login_validation = true;
            } else {
                if (!regex.test(emailLogin) && emailLogin.length != 0) {
                    document.getElementById("emailErrorLogin").innerHTML = "Invalid email address!*";
                    login_validation = true;
                }
                else if (getUserLogin(emailLogin)) {
                    if (document.getElementById("emailErrorLogin").innerHTML == ""){
                        login_validation = false
                    } else{
                        document.getElementById("emailErrorLogin").innerHTML = "";
                        login_validation = true;
                    }
                    
                }
            }
    return login_validation;
}

async function getUserLogin(email) {
    fetch("http://127.0.0.1:5000/getUserLogin")
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            for (i = 0; i < data.length; i++) {
                console.log(i);
                if (email == data[i]["email"]) {
                    document.getElementById("emailErrorLogin").innerHTML = "";
                    login_validation = false;
                    break;
                }
                else if (email.length != 0 && email != data[i]["email"]) {
                    document.getElementById("emailErrorLogin").innerHTML = "This email doesn't exist! Register!*";
                    login_validation = true;
                } else {
                    document.getElementById("emailErrorLogin").innerHTML = "Please enter your email!*";
                    login_validation = true;
                }
            }
        });
    return login_validation;
}

function check_pass_login() {
    check_email_login();
    let loginPass = document.forms["formValidationLogin"]["password"].value;

    if (loginPass.length == 0) {
        document.getElementById("loginPassError").innerHTML = "Password is required!*";
        pass_valid = true;
    }
    else { 
            document.getElementById("loginPassError").innerHTML = "";
            pass_valid = false; 
        }
    return pass_valid;
}

// nuk lejon berjen submit te login nese fushat nuk jane plotesuar sipas kushteve
$(document).ready(function () {
    $('#formValidationLogin').submit(function (e) {
        if ((login_validation == true && pass_valid == true) || (login_validation == true && pass_valid == false) || (login_validation == false && pass_valid == true)) {
            e.preventDefault();

        }
        // or return false;
    });
});