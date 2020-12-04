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


    $('.follow-button').on('click', async function(evt){

        console.log(`Bill ID: ${$(evt.target).parent().parent().parent().parent().attr('id')}`)

        let billId = $(evt.target).parent().parent().parent().parent().attr('id')

        let req = await axios.post(`/bill/${billId}/follow`)

        console.log('Request data: ', req.data)

        UIFollowAction(req.data.resp_code, evt.target)

    })


    function UIFollowAction(status, button){

        if(status == 'foll_success'){

            $(button).removeClass('btn-success');
            $(button).addClass('btn-outline-danger');
            $(button).text('Unfollow')


        }
        else if(status == 'unfoll_success'){

            $(button).removeClass('btn-outline-danger');
            $(button).addClass('btn-success');
            $(button).text('Follow')
        }
        else{

            $('body').append($("<p>You can't do that at this time</p>"))
        }

    }
});


// currently this hides/shows all summaries, which is a feature I want to keep, but not attached to this button

// clicking follow should be an ajax requestin in this file so that the page doesn't refresh or leave and the button is changed to unfollow when clicked



// next steps, make a user model
