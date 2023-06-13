function handleScroll() {
  const controller = document.querySelector('#controller');
  const isFixedTop = window.scrollY === 0; // 상단에 고정된 상태 여부 확인

  if (controller) {
    if (isFixedTop) {
      controller.classList.remove('lg:block'); // 상단에 고정된 상태일 때 숨김 클래스 추가
      controller.classList.add('lg:hidden'); 
    } else {
      controller.classList.remove('lg:hidden'); // 상단에 고정된 상태가 아닐 때 숨김 클래스 제거
      controller.classList.add('lg:block');
    }
  }
}

function handleScrollNavbar() {
  const controller = document.querySelector('#mobile-navbar');
  const isFixedTop = window.scrollY === 0; // 상단에 고정된 상태 여부 확인

  if (controller) {
    if (isFixedTop) {
      controller.classList.remove('block'); // 상단에 고정된 상태일 때 숨김 클래스 추가
      controller.classList.add('hidden'); 
    } else {
      controller.classList.remove('hidden'); // 상단에 고정된 상태가 아닐 때 숨김 클래스 제거
      controller.classList.add('block'); 
    }
  }
}

window.addEventListener('scroll', handleScroll);

window.addEventListener('scroll', handleScrollNavbar);

