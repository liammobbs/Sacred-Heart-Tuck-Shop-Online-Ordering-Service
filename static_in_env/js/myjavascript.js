//window resize to fix ios address bar issue

// First we get the viewport height and we multiply it by 1% to get a value for a vh unit


window.onresize = function() {
    document.body.height = window.innerHeight;
    let vh = window.innerHeight * 0.01;
    // Then we set the value in the --vh custom property to the root of the document
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}
window.onresize();

// We listen to the resize event
window.addEventListener('resize', () => {
    // We execute the same script as before
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
});



$(document).on('click','.open-OptionModal',function(){
    var slug = $(this).data('slug');
    var object = $(this).data('object');
    update_variations(slug);


    $(".modal-body #object").text(object);
    $(".modal-body #slug").text(slug);
    $('#OptionModal').modal('show');

});

function update_variations(slug){
    $('.option-content').html('').load(
    "{% url 'core:update-variations' %}?slug=" +slug
    );
};


function AjaxUpdateQuantity(djangourl){
    let url = djangourl
    console.log("hello world");
    console.log(url);
    var token =  $('input[name="csrfmiddlewaretoken"]').attr('value')

    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('Csrf-Token', token);
        }
    });
    
    $.ajax({
        type: "POST",
        url: url,
        data: {isAjax: "true"},
        success: function(response) {alert(response);},
        error: function() {alert("Couldn't remove item");}
    }) 
};