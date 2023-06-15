const kakaoBtn = document.getElementById('btnKakao')
const title = kakaoBtn.dataset.title
const content = kakaoBtn.dataset.content
let link = kakaoBtn.dataset.link
link = link.substring(1)
const likeCount = kakaoBtn.dataset.likeCount
const commentCount = kakaoBtn.dataset.commentCount
const viewCount = kakaoBtn.dataset.viewCount

console.log(commentCount)

const toastSimple = document.getElementById('toast-simple')
Kakao.init('46fed7723052d8712b267e8a83ab2fa4')


function shareKakao() {
  Kakao.Share.createCustomButton({
    container: '#btnKakao',
    templateId: 94650,
    templateArgs: {
      TITLE: title,
      CONTENT: content,
      LIKECOUNT: likeCount,
      COMMENTCOUNT: commentCount,
      VIEWCOUNT: viewCount,
      LINK: link,
    },
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