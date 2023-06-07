const likesForm = document.querySelector('#like-form')
let likePostCount = document.querySelector('#like-post-count')
const likeFormCsrfToken = likesForm.querySelector('[name=csrfmiddlewaretoken]').value;

likesForm.addEventListener('submit', function (event) {
  event.preventDefault()
  const postId = event.target.dataset.postId

  axios({
    method : 'post',
    url: `/communities/${postId}/like/`,
    headers: {'X-CSRFToken': likeFormCsrfToken},
  })
  .then((response) => {
    const isLiked = response.data.is_liked
    const likeIcon = document.querySelector('#likes_btn > i')
    if (isLiked === true) {
      likeIcon.classList.remove('bi-heart')
      likeIcon.classList.add('bi-heart-fill')
      likePostCount.textContent = parseInt(likePostCount.textContent) + 1
    } else {
      likeIcon.classList.add('bi-heart')
      likeIcon.classList.remove('bi-heart-fill')
      likePostCount.textContent = parseInt(likePostCount.textContent) - 1
    }
  })
})