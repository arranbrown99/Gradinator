//hides a class until the button with the correct name is pressed used in band_calculator_slug.html
$(document).ready(function(){
    $(".to_be_hidden").hide()
    $(".predict_btn").click(function(){


        $(".p"+this.name).show()

    });


});
