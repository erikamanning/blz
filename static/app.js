

$(document).ready(function(){

    $('.sm-leg-card').on('click', function(){

        let leg_id = $(this).attr('id') 
        window.location = `/legislator/${leg_id}`
    })

    async function getFollowedBills(){

        let req = await axios.get(`/user/${gUserId}/followed-bills`);
        fBills = req.data;

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

    $(".details-button").click(function(evt){

        lma = $(this).parent().parent().find('.last-major-action')
        $(lma).toggleClass('d-none')

    });

    $('.follow-button').on('click', async function(evt){

        let billId = $(this).parent().parent().parent().parent().attr('id');

        let req = await axios.post(`/bill/${billId}/follow`);

        console.log('Request data: ', req.data);

        $(this).toggleClass('btn-outline-dark')
        $(this).toggleClass('btn-dark')

        // if this is the follow section, remove bill from list
        if ($(this).parent().parent().parent().parent().parent().parent().parent().attr('id') == 'followed-bills'){

            $(this).parent().parent().parent().parent().parent().parent().fadeOut("slow")
        }
    });

});