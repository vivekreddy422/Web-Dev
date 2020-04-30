 ​document​.​addEventListener​(​'​DOMContentLoaded​'​, () => {
    document.querySelector("#username").onkeyup = () => {
        if(validateEmail(document.querySelector("#username").value)) {
            document.querySelector("#validation-message").innerHTML = "email can not be a username"
            document.querySelector("#register").disabled = true;
            document.querySelector("#login").disabled = true;
            return false
        } else {
            // document.querySelector("#validation-message").innerHTML = ""
            document.querySelector("#register").disabled = false;
            document.querySelector("#login").disabled = false;
            return true
        }
    }

    document.querySelector("#password").onkeyup = () => {
        var password = document.querySelector("#password").value
        if (validatePassword(password)) {
            // document.querySelector("#validation-message").innerHTML = ""
            document.querySelector("#register").disabled = false;
            document.querySelector("#login").disabled = false;
            return true
        } else {
            document.querySelector("#validation-message").innerHTML = "The password should contain at least 6 characters, with at least one uppercase letter, one lowercase letter, one number and a symbol."
            document.querySelector("#register").disabled = true;
            document.querySelector("#login").disabled = true;
            return false
        }
    }
})

function validateEmail(word) {
    var email =  ​/​^​\w​+​(​[​\.​-]​?​\w​+​)@​\w​+​(​[​\.​-]​?​\w​+​)(​\.​\w​{2,3}​)​+​$​/​;​
    if (word.match(email)) {
        return true;
    } else {
        return false;
    }
}

function validatePassword(word) {
    if (word.length < 6 || word.search(/[a-z]/) < 0 || password​.​search​(​/​[​A-Z​]​/​) ​<​ ​0 || password​.​search​(​/​[​0-9]​/​) ​<​ ​0​​
                        || password​.​search​(​/​[​!@#$%^&*]​/​) ​<​ ​0) {
                            return false
                        }​ else {
                            return true
                        }
}