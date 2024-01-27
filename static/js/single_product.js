$(document).ready(function (){
    const price  = parseInt($('.price').text());
    $('.qty').on('click', function(){
        const qty = parseInt($(this).val());
        if (qty != 0){
            $('.price').text(qty * price);
        }
        
    })
});

