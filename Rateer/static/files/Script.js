$(document).ready(function() {
  $('img').each(function() {
      var currentImage = $(this);
      currentImage.wrap("<a class='image-link' href='" + currentImage.attr("src") + "'</a>");
  });
  $('.image-link').magnificPopup({type:'image'});
});
$(document).ready(function() {
$('[data-toggle="collapse"]').click(function() {
  $(this).toggleClass( "active" );
  if ($(this).hasClass("active")) {
    $(this).text("Hide");
  } else {
    $(this).text("Show");
  }
});



