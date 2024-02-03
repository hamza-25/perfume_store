$(document).ready(function (){
    const price  = parseFloat($('.price').text());
    $('.qty').on('click', function(){
        const qty = parseFloat($(this).val());
        if (!isNaN(qty) && qty != 0){
            $('.price').text((qty * price).toFixed(2));
        }
        
    })
});

