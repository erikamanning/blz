
// async function getPolicyAreas(){

//     let req = await axios.get('/get-policy-areas')

//     let policy_areas = []

//     for(let policy_area of req.data){

//         let new_pa = new PolicyArea(policy_area['id'], policy_area['name'])
//         policy_areas.push(new_pa)
//         console.log(new_pa)
//         console.log(policy_areas)
//     }

//     return policy_areas
// }

// async function start(){

//     let policy_areas = await getPolicyAreas();

//     const $ul = $('<ul>')
    
//     for(let pa of policy_areas){
    
//         console.log('pa: ', pa['name'])
//         const new_li = $(`<li>${pa['name']}</li>`);
//         $ul.append(new_li);
//     }
    
//     $('body').append($ul)
// }

// start();

// async function start(){

//     let policy_areas = await getPolicyAreas();

//     const $ul = $('<ul>')
    
//     for(let pa of policy_areas){
    
//         console.log('pa: ', pa['name'])
//         const new_li = $(`<li>${pa['name']}</li>`);
//         $ul.append(new_li);
//     }
    
//     $('body').append($ul)
// }

// start();

// src="{{legislators['r'][j].image}}"

function handleImageError(image){

    console.log('THISSSSSSSSS: ', this)

}

$(document).ready(function(){



    // images = document.getElementsByTagName('img')

    // setTimeout(function(){

    //     for( img of images){

    //         if(!img.complete){
    //             console.log('HELLOOOo!')
    //             img.src='https://www.startpage.com/av/proxy-image?piurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F4%2F4b%2FSeal_of_the_United_States_Congress.svg%2F1200px-Seal_of_the_United_States_Congress.svg.png&sp=1610138024T619f5c322555cb24e633f46780b99fe389b1000dbb6ac1c9e5181bf85415ac79'
    //         }
    //     }

    // },500)

    $billSearchForm = $('#bill-search-form');


    // change to updated javascript
    $billSearchForm.change(function(evt){

        $billSearchForm.submit()
        console.log( "form change" );

    })


    $paginationLinks = $('#pagination-links');


    // change to updated javascript
    $paginationLinks.change(function(evt){

        

        $paginationLinks.submit()
        console.log( "pagination clicked" );

    })

    
    $("#show-details").click(function(evt){

        $('.summary-container').toggleClass('d-none');
        $('.last-major-action').toggleClass('d-none');
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
