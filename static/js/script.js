// define contants for various variables
const logPasswordField = document.querySelector("#id_password");
const signPasswordField = document.querySelector("#id_password1");
const confirmSignPasswordField = document.querySelector("#id_password2");
const signupForm = document.querySelector('signupForm'); // replace 'form' with the ID or class of your form element

// // Function to toggle password visibility
function togglePasswordVisibility(formType, checkBox) {
    if (formType == "login") {
        if (checkBox.checked) {
            logPasswordField.type = "text";
        } else {
            logPasswordField.type = "password";
        }
    } else if (formType == "signup") {
        if (checkBox.checked) {
            signPasswordField.type = "text";
            confirmSignPasswordField.type = "text";
        }
        else {
            signPasswordField.type = "password";
            confirmSignPasswordField.type = "password";
        }

    }
}
