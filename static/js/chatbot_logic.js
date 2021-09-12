$(document).ready(function () {

  $("h5").css('color', 'red');


  $('.chatbox').keypress(function (e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $(".current-input").click();
      let label = $(".current-input").attr("id");

      var next = function(dict, key) {
        var keys = Object.keys(dict)
          , i = keys.indexOf(key);
        return i !== -1 && keys[i + 1];
      };

      nextLabel = next(inputList, label)

      $(".current-input").removeClass("current-input").addClass("previous-input");

      $(".chatbox").append(inputList[nextLabel]);


      return console.log(nextLabel);
    }
  });

});