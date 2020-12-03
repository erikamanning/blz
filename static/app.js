$(document).ready(function(){

    $(".summary-button").click(function(evt){

        // if($('.summary-container').is(":visible")){

            // $('.summary-container').hide();
        //   }
        //   else if($('.summary-container').is(":hidden")){
            $('.summary-container').toggleClass('d-none');
        //   }
        console.log('Clicked')
    });





});


// currently this hides/shows all summaries, which is a feature I want to keep, but not attached to this button

// clicking follow should be an ajax requestin in this file so that the page doesn't refresh or leave and the button is changed to unfollow when clicked



// next steps, make a user model
