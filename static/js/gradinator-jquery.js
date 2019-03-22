//hides a class until the button with the correct name is pressed used in band_calculator_slug.html
$(document).ready(function () {
    $(".to_be_hidden").hide()
    var hidden = true
    $(".predict_btn").click(function () {

        if (hidden == true) {
            $(".p" + this.name).show()
            hidden = false
        } else {
            $(".p" + this.name).hide()
            hidden = true
        }
    });


       $(".hover").hover(function() {
          $(this).animate({paddingLeft: '+=10px'}, 400);
        }, function() {
          $(this).animate({paddingLeft: '-=10px'}, 400);
        });


});
