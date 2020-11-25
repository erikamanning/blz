$(document).ready(function(){

    $(".summary-button").click(function(evt){

        // console.log($(".summary-button").parent().prop('tagName'))

        // let parent = $(".summary-button").parent()
        ($(evt).parent()).prev().toggle("slow", function(){

        });
    });
});