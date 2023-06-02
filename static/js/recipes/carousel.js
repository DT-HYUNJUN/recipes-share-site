$(document).ready(function () {
  // 인기순
  $(".recipe-likes-slide").slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 4,
    prevArrow: '<button type="button" class="slick-prev"><</button>',
    nextArrow: '<button type="button" class="slick-next">></button>',
    autoplay: true,
    autoplaySpeed: 3000, // Set the autoplay time for the recipe-like-slide slider
    // speed: 2500,
    pauseOnHover: false,
    pauseOnFocus: false,

    responsive: [
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          rows: 1,
        },
      },
      {
        breakpoint: 1280,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
        },
      },
    ],
  });
  // 날씨순
  $(".recipe-weather-slide").slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 4,
    prevArrow: '<button type="button" class="slick-prev"><</button>',
    nextArrow: '<button type="button" class="slick-next">></button>',
    autoplay: true,
    autoplaySpeed: 5000, // Set the autoplay time for the recipe-slide slider
    // speed: 2000,
    pauseOnHover: false,
    pauseOnFocus: false,

    responsive: [
      {
        breakpoint: 1280,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          rows: 1,
        },
      },
    ],
  });

  //냉장고
  $(".recipe-fridge-slide").slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 4,
    prevArrow: '<button type="button" class="slick-prev"><</button>',
    nextArrow: '<button type="button" class="slick-next">></button>',
    autoplay: true,
    autoplaySpeed: 5000, // Set the autoplay time for the recipe-slide slider
    // speed: 2000,
    pauseOnHover: false,
    pauseOnFocus: false,

    responsive: [
      {
        breakpoint: 1280,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          rows: 1,
        },
      },
    ],
  });

  // 프로필
  $(".recipe-profile-slide").slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 4,
    prevArrow: '<button type="button" class="slick-prev"><</button>',
    nextArrow: '<button type="button" class="slick-next">></button>',
    // autoplay: true,
    // autoplaySpeed: 5000, // Set the autoplay time for the recipe-slide slider
    // // speed: 2000,
    // pauseOnHover: false,
    // pauseOnFocus: false,

    responsive: [
      {
        breakpoint: 1280,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2,
          rows: 1,
        },
      },
    ],
  });
});
