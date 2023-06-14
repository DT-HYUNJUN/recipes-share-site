var carousel = document.getElementById('default-carousel');
var carouselItems = carousel.querySelectorAll('[data-carousel-item]');
var currentIndex = 0;

var delay = 3000; // 3초 지연 시간 (단위: 밀리초)

function showNextItem() {
  // 현재 아이템을 숨김
  carouselItems[currentIndex].classList.add('hidden');
  
  // 다음 아이템으로 인덱스를 업데이트
  currentIndex = (currentIndex + 1) % carouselItems.length;
  
  // 다음 아이템을 보여줌
  carouselItems[currentIndex].classList.remove('hidden');
  
  // delay 밀리초 후에 다음 아이템을 보여주기 위해 재귀 호출
  setTimeout(showNextItem, delay);
}

// 첫 번째 아이템을 보여줌
carouselItems[currentIndex].classList.remove('hidden');

// delay 밀리초 후에 다음 아이템을 보여주기 위해 호출
setTimeout(showNextItem, delay);
