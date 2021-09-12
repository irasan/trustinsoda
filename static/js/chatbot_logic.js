$(document).ready(function () {

  $("h5").css('color', 'red');

  let x = 0
  let keyslist = ['full_name', 'email', 'phone', 'city', 'country', 'password1', 'password2', 'disc', 'area', 'type', 'exp', 'exp2', 'contact', 'accom']
  $('.chatbox').keypress(function (e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $(".current-input").click();
      let label = $(".current-input").attr("id");

      x ++
/*       console.log(labelList[x])
      var next = function (dict, key) {
        var keyss = Object.keys(dict);
          console.log(keyss);
          i = keyss.indexOf(key);
          console.log(i);
        return i !== -1 && keyss[i + 1];
      };

      nextLabel = next(labelList, label)
      nextanswer = (Object.keys(labelList)).indexOf(label)
      console.log(nextanswer + 1) */

      $(".current-input").removeClass("current-input").addClass("previous-input");

      $(".chatbox").append($(labelList[keyslist[x]]).hide().fadeIn("fast"));

      $(".chatbox").append($(inputList[keyslist[x]]).hide().fadeIn("fast"));

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