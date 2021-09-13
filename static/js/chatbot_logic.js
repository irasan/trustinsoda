$(document).ready(function () {

  let x = 0
  let keyslist = ['full_name', 'email', 'phone', 'city', 'country', 'password1', 'password2', 'disc', 'area', 'type', 'exp', 'exp2', 'contact', 'accom']
  $('.chatbox').keypress(function (e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $(".current-input").click();

      x ++

      if (keyslist[x] == 'accom') {
      $(".chatbox").append($(submit).hide().fadeIn("fast"));
      } else {
        $(".current-input").removeClass("current-input").addClass("previous-input");
        
        $(".chatbox").append($(labelList[keyslist[x]]).hide().fadeIn("fast"));
        
        $(".chatbox").append($(inputList[keyslist[x]]).hide().fadeIn("fast"));

        $(".current-input").focus();
      }
        
      $("html, body").animate(
        {
          scrollTop: $("html, body").get(0).scrollHeight,
        },
        2000
      );

      return true;
    }
  });

});