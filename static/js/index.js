console.log("testing testing")

function getPasswordStrength(password){
    let s = 0;

    if (password.length > 4){
        s++;
    }

    if (password.length > 6){
        s++;
    }

    if (/[A-Z]/.test(password)){ //testing for capital letters
        s++;
    }
    if(/[0-9]/.test(password)){ //testing for numbers 0-9
        s++;
    }

    if (/[^A-Za-z0-9]/.test(password)){
        s++;
    }

    return s;
}

//code for displaying strength meter
var password_box = document.querySelector(".form-group #password")
if(password_box){
    password_box.addEventListener("focus", function(){ //focus concentrates on whether or not 
        console.log("are you even working // FOCUSING ON PASSWORD BOX")
        document.querySelector(".form-group .password_strength").style.display = "block";
    });
}
else{
    console.log(".form_group #password2 NOT FOUND")
}


var toggle_button = document.querySelector(".form-group .password_toggler")

if(toggle_button){
    toggle_button.addEventListener("click", function(){
       
        let el = toggle_button;
        if(el.classList.contains("active")){
            console.log("Hide password clicked")
            document.querySelector(".form-group #password_sign_in").setAttribute("type", "password")
            el.classList.remove("active") //remove a class list from the element (.form-group .password_toggler)
        }

        else{
            console.log("Show password clicked")
            document.querySelector(".form-group #password_sign_in").setAttribute("type", "text")
            el.classList.add("active") //creating a class list for the element (.form-group .password_toggler)
        }
    });
}


password_box.addEventListener("keyup", function(e){ //keyup = keys being pressed 
    let password = e.target.value;
    let strength = getPasswordStrength(password)
    let passwordStrengthSpan = document.querySelectorAll(".form-group .password_strength span")
    strength = Math.max(strength, 1)
    passwordStrengthSpan[1].style.width = strength*20 + "%";

    if(strength < 2){
        passwordStrengthSpan[0].innerText = "Strength: Weak";
        passwordStrengthSpan[1].style.color = "#111";
        passwordStrengthSpan[1].style.background = "#d13636";
    }

    else if(strength >= 2 && strength <= 4){
        passwordStrengthSpan[0].innerText = "Strength: Medium";
        passwordStrengthSpan[1].style.color = "#111"
        passwordStrengthSpan[1].style.background = "#ffff00";

    }
    
   else{
        passwordStrengthSpan[0].innerText = "Strength: Strong";
        passwordStrengthSpan[1].style.color = "#111"
        passwordStrengthSpan[1].style.background = "#008000"
   } 
})



