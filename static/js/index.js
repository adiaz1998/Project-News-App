console.log("testing connection between server and client")


var toggle_button = document.querySelector(".form-group .password_toggler")
var toggle_button_2 = document.querySelector(".form-group .password_toggler_reg")
var toggle_button_3 = document.querySelector(".form-group .password_toggler_2")

//code for toggling password being shown on/off
if (toggle_button) {

    toggle_button.addEventListener("click", toggle_on_off)
        //toggle_button2.addEventListener("click", toggle_on_off(".form-group", ".password_toggler_reg"))
    function toggle_on_off() {
        let el = toggle_button;
        if (el.classList.contains("active")) {
            console.log("Hide password clicked")
            document.getElementById('password_sign_in').setAttribute("type", "password")
            el.classList.remove("active") //remove a class list from the element (.form-group .password_toggler)
        } else {
            console.log("Show password clicked")
            document.getElementById('password_sign_in').setAttribute("type", "text")

            // document.querySelector(".form-group #password_sign_in").setAttribute("type", "text")
            el.classList.add("active") //creating a class list for the element (.form-group .password_toggler)
        }
    }
}

toggle_button_2.addEventListener("click", function() {

    let el = toggle_button_2;
    if (el.classList.contains("active1")) {
        console.log("Hide password clicked")
        document.querySelector(".form-group #password").setAttribute("type", "password")
        el.classList.remove("active1") //remove a class list from the element (.form-group .password_toggler)
    } else {
        console.log("Show password clicked")
        document.querySelector(".form-group #password").setAttribute("type", "text")
        el.classList.add("active1") //creating a class list for the element (.form-group .password_toggler)
    }
});


toggle_button_3.addEventListener("click", toggle_on_off)
    //toggle_button2.addEventListener("click", toggle_on_off(".form-group", ".password_toggler_reg"))
function toggle_on_off() {
    let el = toggle_button_3;
    if (el.classList.contains("active")) {
        console.log("Hide password clicked")
        document.getElementById('password2').setAttribute("type", "password")
        el.classList.remove("active") //remove a class list from the element (.form-group .password_toggler)
    } else {
        console.log("Show password clicked")
        document.getElementById('password2').setAttribute("type", "text")

        // document.querySelector(".form-group #password_sign_in").setAttribute("type", "text")
        el.classList.add("active") //creating a class list for the element (.form-group .password_toggler)
    }

}

//function for getting passwordStrength
function getPasswordStrength(password) {
    let s = 0;

    if (password.length == 0) {
        s = 0;
    }
    if (password.length > 4) {
        s++;
    }

    if (password.length > 6) {
        s++;
    }

    if (/[A-Z]/.test(password)) { //testing for capital letters
        s++;
    }
    if (/[0-9]/.test(password)) { //testing for numbers 0-9
        s++;
    }

    if (/[^A-Za-z0-9]/.test(password)) {
        s++;
    }

    return s;
}

//code for displaying strength meter
var sign_up_password_box = document.querySelector(".form-group #password")
var sign_up_password_box_2 = document.querySelector(".form-group #password2")

if (sign_up_password_box) {
    sign_up_password_box.addEventListener("click", function() { //focus concentrates on whether or not
        console.log("are you even working // FOCUSING ON PASSWORD BOX")
        document.querySelector(".form-group .password_strength").style.display = "block";
        //document.querySelector(".form-group .password_strength").height = "0px";
    });
} else {
    console.log(".form_group #password NOT FOUND")
}


if (sign_up_password_box) {

    sign_up_password_box.addEventListener("keyup", function(e) { //keyup = keys being pressed
        let password = e.target.value;
        let strength = getPasswordStrength(password)
        let passwordStrengthSpan = document.querySelectorAll(".form-group .password_strength span")
        strength = Math.max(strength, 1)
        passwordStrengthSpan[1].style.width = strength * 20 + "%";

        if (strength < 2) {
            passwordStrengthSpan[0].innerText = "Strength: Weak";
            passwordStrengthSpan[1].style.color = "#111";
            passwordStrengthSpan[1].style.background = "#d13636";

        } else if (strength >= 2 && strength <= 4) {

            passwordStrengthSpan[0].innerText = "Strength: Medium";
            passwordStrengthSpan[1].style.color = "#111"
            passwordStrengthSpan[1].style.background = "#ffff00";

        } else if (strength == 0) {
            passwordStrengthSpan[0].innerText = "Strength: Neutral";
            passwordStrengthSpan[1].style.color = "#111"
            passwordStrengthSpan[1].style.background = "#f2f2f2";

        } else {
            passwordStrengthSpan[0].innerText = "Strength: Strong";
            passwordStrengthSpan[1].style.color = "#111"
            passwordStrengthSpan[1].style.background = "#008000"
        }
    });
}

//checking for password length (MADE CHANGES TO THIS ON 10/9/2021)
if (sign_up_password_box) {

    sign_up_password_box.addEventListener("keyup", check_for_password_length)

    function check_for_password_length() {
        const pass_length = document.getElementById("password").value.length;
        console.log("Password length: " + pass_length + " characters");
        if (pass_length != null && pass_length == 0) {

            console.log("entered second block ")
            let passwordStrengthSpan = document.querySelectorAll(".form-group .password_strength span");
            passwordStrengthSpan[0].innerText = "Strength: Neutral";
            passwordStrengthSpan[1].style.background = "none";

        }
    }

}
//JS NOTES: var declarations are globally scoped or function scoped while let and const are block scoped. 
//var variables can be updated and re-declared within its scope; let variables can be updated but not re-declared; 
//const variables can neither be updated nor re-declared. They are all hoisted to the top of their scope

//What is a block? A block is a chunk of code bounded by {}. A block lives in curly braces. Anything within curly braces is a block.


//code for showing password strength tip
if (sign_up_password_box) {

    sign_up_password_box.addEventListener("mouseenter", function() {
        console.log("mouse hovered over password_box")
        document.querySelector(".strong_password_tip").style.display = "block"; //get the class for to display the password tip content

    });

    sign_up_password_box.addEventListener("mouseleave", function() {
        console.log("mouse moved away from password_box")
        document.querySelector(".strong_password_tip").style.display = "none"; //get the class for to display the password tip content

    });

}
//document.querySelector(".form-group #password").addEventListener("mouseout", get_password);

//code for confirming two passwords are equal to each other
//(MADE CHANGES TO THIS ON 10/9/2021)
sign_up_password_box.addEventListener("keyup", check_for_similar_passwords)
sign_up_password_box_2.addEventListener("keyup", check_for_similar_passwords)

function check_for_similar_passwords() {

    const password1 = document.getElementById('password').value
    const password2 = document.getElementById('password2').value
    console.log("password1:", password1, "password2:", password2)

    if (password1 == password2) {
        console.log("passwords are equal to each other")
            //disable the warning: ..... element
        document.querySelector('.confirm_password').style.display = "none";
        //document.querySelector(".form-group .password_strength").style.display = "none";
        document.querySelector('.btn').disabled = false;
        document.querySelector('.btn').style.display = "block";
        document.querySelector(".form-group .password_strength").style.display = "block";

    } else {
        console.log("Please make sure your passwords equal each other")
            //enable the warning: ..element
        document.querySelector('.confirm_password').style.display = "block";
        document.querySelector('.confirm_password').style.color = "red";
        document.querySelector('.btn').disabled = true;

        if (document.querySelector('.btn').disabled == true) {
            document.querySelector('.btn').style.display = "none";

            //console.log(";p;")
            //document.querySelector('.btn').addEventListener("mouseover", displayError)

            //function displayError() {
            //  console.log("lol bro")
            //}
        }
    }
}