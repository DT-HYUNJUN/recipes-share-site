const kakaoBtn = document.getElementById('btnKakao')
const title = kakaoBtn.dataset.title
const content = kakaoBtn.dataset.content
const baseLink = 'http://127.0.0.1:8000'
// const baseLink = kakaoBtn.dataset.baseLink
console.log(baseLink)
const link = kakaoBtn.dataset.link
const image = kakaoBtn.dataset.image
const toastSimple = document.getElementById('toast-simple')


function shareKakao() {
  // 사용할 앱의 JavaScript 키 설정
  Kakao.init('46fed7723052d8712b267e8a83ab2fa4');
  // 카카오링크 버튼 생성
  Kakao.Link.createDefaultButton({
    container: '#btnKakao', // 카카오공유버튼ID
    objectType: 'feed',
    content: {
      title: title, // 보여질 제목
      description: content, // 보여질 설명
      imageUrl: baseLink + image, // 콘텐츠 URL
      link: {
         mobileWebUrl: baseLink + link,
         webUrl: baseLink + link
      }
    }
  });
}


function showToast() {
  toastSimple.classList.remove('hidden');
  toastSimple.classList.add('flex');

  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  const toastTop = scrollTop - 200; // 토스트 메시지의 상단 위치 조정
  const viewportWidth = window.innerWidth;
  const toastWidth = toastSimple.offsetWidth;
  const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
  const currentLeft = scrollLeft + (viewportWidth / 2) - (toastWidth / 2);

  toastSimple.style.top = toastTop + 'px';
  toastSimple.style.left = currentLeft + 'px';
  

  setTimeout(() => {
    toastSimple.classList.remove('flex');
    toastSimple.classList.add('hidden');
  }, 3000);
}

function copyLink() {
  var linkElement = document.createElement('textarea');
  linkElement.value = window.location.href;
  document.body.appendChild(linkElement);
  linkElement.select();
  document.execCommand('copy');
  document.body.removeChild(linkElement);
  
  showToast()
}