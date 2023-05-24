$(document).ready(function(){
  $('.recipe-slide').slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 4,
    prevArrow : "<button type='button' class='slick-prev slick-index-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next slick-index-next'>Next</button>",
  });
})