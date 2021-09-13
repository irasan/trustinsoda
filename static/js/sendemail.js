function sendMail(contactForm){
    emailjs.send("outlook", "enable", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "subject": contactForm.subject.value,
        "message": contactForm.message.value
    })
    .then(
        function(response) {
            console.log("SUCCESS", response);
        },
        function(error) {
            console.log("FAILED", error);
        }
    );
    return false;
}

function newAlert() {
    alert("If you have completed the form correctly you will receive a confirmation email shortly!")
}