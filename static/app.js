

$(document).ready(function(){


    async function getFollowedBills(){

        console.log('gUser: ', gUserId);

        let req = await axios.get(`/user/${gUserId}/followed-bills`);
        console.log('req data: ', req);

        fBills = req.data;
        console.log('F BILLS: ', fBills);

        return fBills

        
    }
    async function UIFollowButtons(){

        followed_bills = await getFollowedBills()
    
        for(let bill of followed_bills){
    
            $(`#${bill}`).find('#follow-button').toggleClass('btn-outline-dark')
            $(`#${bill}`).find('#follow-button').toggleClass('btn-dark')
        }
    
    }

    if( gUserId != ''){

        UIFollowButtons();

    }

    // visuals for dashboard buttons and show hide content functionality
    $('#dash-buttons').on('click', function(event){

        if( !$(event.target).hasClass('active') ){

            $(event.target).toggleClass('active')
            $('#dash-state-info').toggleClass('d-none');
            $('#dash-saved-bills').toggleClass('d-none');  
        }

        if( $(event.target).siblings().hasClass('active') ){

            $(event.target).siblings().toggleClass('active')
        }
    });

    // show/hide sponsored bills functionality
    $('#sponsored-bills-button').on('click', function(event){

        $('#sponsored-bills').toggleClass('d-none');
        $('#sponsored-bills-button-icon').toggleClass('fa-caret-square-up');

    });

    $billSearchForm = $('#bill-search-form');

    // change to updated javascript
    $billSearchForm.change(function(evt){

        $billSearchForm.submit();
        console.log( "form change" );

    });


    $paginationLinks = $('#pagination-links');


    // change to updated javascript
    $paginationLinks.change(function(evt){

        

        $paginationLinks.submit();
        console.log( "pagination clicked" );

    });

    
    $("#show-details").click(function(evt){

        $('.summary-container').toggleClass('d-none');
        $('.last-major-action').toggleClass('d-none');
    });


    $('.follow-button').on('click', async function(evt){

        console.log(`Bill ID: ${$(this).parent().parent().parent().parent().attr('id')}`);

        let billId = $(this).parent().parent().parent().parent().attr('id');

        let req = await axios.post(`/bill/${billId}/follow`);

        console.log('Request data: ', req.data);

        $(this).toggleClass('btn-outline-dark')
        $(this).toggleClass('btn-dark')

        // UIFollowAction(req.data.resp_code, evt.target);

    });


    function UIFollowAction(status, button){

        if(status == 'foll_success'){

            $(button).removeClass('btn-outline-dark');
            $(button).addClass('btn-dark');

        }
        else if(status == 'unfoll_success'){

            $(button).removeClass('btn-dark');
            $(button).addClass('btn-outline-dark');
        }
        else{

            $('body').append($("<p>You can't do that at this time</p>"));
        }

    }
});


// currently this hides/shows all summaries, which is a feature I want to keep, but not attached to this button

// clicking follow should be an ajax requestin in this file so that the page doesn't refresh or leave and the button is changed to unfollow when clicked



// next steps, make a user model
