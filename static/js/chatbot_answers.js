// this is a dictionary of all the labels for the input fields
const labelList = {
  "full_name": '<p class="label">What is your full name?</p>',
  "email": '<p class="label">Nice name!<br>Now, what is your email address?</p>',
  "phone": '<p class="label">Great!<br>Next, we need your phone number</p>',
  "city": '<p class="label">Where do you live? Enter the city name</p>',
  "country": '<p class="label">And that city is in which country?</p>',
  "password1": '<p class="label">Now, you need to type in a password for when you log in</p>',
  "password2": '<p class="label">Can you repeat that password please, just to make sure that we got it right</p>',
  "disc": '<p class="label">Thank you, we are half way through the registration process.<br>Now, can you tell us a bit about yourself?</p>',
  "area": '<p class="label">That looks good!<br>Next, what area are you looking for work in:<br>Retail, Admin, Hospitality, IT or Other?<br>If you want to choose more than one, seperate the words with a comma just like the above.</p>',
  "type": '<p class="label">So, what type of work do you want to do?</p>',
  "exp": '<p class="label">Have you work experience in this area?<br>Put everything you think is relevent.</p>',
  "exp2": '<p class="label">Have you other training or experiences relevant to this job?</p>',
  "contact": '<p class="label">Almost done ...<br>How do you want employers to contact you, by mail or by phone?</p>',
  "accom": '<p class="label">And finally<br>Are there any accommodations you need for the interview or workplace?</p>',
};

// this is a dictionary of all the input fields that the user has to fill
const inputList = {
  "full_name": '<input type="text" class="form-control current-input" id="full_name" name="full_name" required>',
  "email": '<input type="email" class="form-control current-input" id="email" name="email" required>',
  "phone": '<input type="text" class="form-control current-input" id="phone" name="phone" required>',
  "city": '<input type="text" class="form-control current-input" id="city" name="city" required>',
  "country": '<input type="text" class="form-control current-input" id="country" name="country" required>',
  "password1": '<input type="password" class="form-control current-input" id="password1" name="password1" required>',
  "password2": '<input type="password" class="form-control current-input" id="password2" name="password2" required>',
  "disc": '<textarea class="form-control current-input" id="description" name="description" rows="3"></textarea>',
  "area": '<input type="text" class="form-control current-input" id="sector" name="sector" required>',
  "type": '<input type="text" class="form-control current-input" id="sector_other" name="sector_other" required>',
  "exp": '<input type="text" class="form-control current-input" id="experience1" name="experience1" required>',
  "exp2": '<input type="text" class="form-control current-input" id="education" name="education" required>',
  "contact": '<input type="text" class="form-control current-input" id="contact_preference" name="contact_preference" required>',
  "accom": '<textarea class="form-control current-input" id="accommodations" name="accommodations" rows="3"></textarea>', 
  "avatar": '<input type="text" class="form-control current-input" id="avatar" name="avatar">',
};

const submit = '<button type="submit" class="btn btn-primary next-page mt-3 mb-5">Submit Registration!</button>'

function getUserInput() {

  var full_name = document.getElementById("full_name").value;
  var email = document.getElementById("email").value;
  var phone = document.getElementById("phone").value;
  var city = document.getElementById("city").value;
  var country = document.getElementById("country").value;
  var password1 = document.getElementById("password1").value;
  var password2 = document.getElementById("password2").value;
  var discription = document.getElementById("disc").value;
  var sector = document.getElementById("area").value;
  var sector_other = document.getElementById("type").value;
  var experience = document.getElementById("exp").value;
  var education = document.getElementById("exp2").value;
  var contact_preference = document.getElementById("contact").value;
  var accommodations = document.getElementById("accom").value;
  var avatar = 0;

}
