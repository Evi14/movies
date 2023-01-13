// $.validator.addMethod("pwcheck", function(value) {
//     return /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/.test(value)
//     }); nese do vendosim requirements per permbajtjen e pass
$("#formValidation").validate({
    rules: {
        name: {
            required:true,
            minlength: 3 },
        email: {
            required: true,
            email: true
        },
        password: {
            required: true,
            minlength: 8,
            // pwcheck:true
        },
        confirm_password: {
            required: true,
            equalTo: "#password"
        }
    },
    messages: {
        name:{
            required: "Please enter your name!*",
            minlength: "Name should be at least 3 characters!*"
        },
        email:{
            required: "Please enter your email!*",
            email: "Invalid email address!*"
        },
        password: {
            required: "Please enter your password!*",
            minlength:"Password should be at least 8 characters!*"
            // pwcheck: "Password doesn't meet requirements!*"
        },
        confirm_password: {
            required: "Please confirm your password!*",
            equalTo: "Passwords don't match!*"
        }
        
    },
    submitHandler: function (form) {
        form.submit();
    }
});
