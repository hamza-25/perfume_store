function viewProfile() {
    // Implement logic to view profile
    console.log("View Profile");
  }
  
  function logout() {
    // Implement logout logic
    console.log("Logout");
  }
$(function(){
  $('.add-category').on('click', function(){
    $('.category-form').toggle()
  })
  $('.add-product').on('click', function(){
    $('.product-form').toggle()
  })
  $('.add-address').on('click', function(){
    $('.address-form').toggle()
  })
})