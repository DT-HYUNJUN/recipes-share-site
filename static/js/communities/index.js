const forms = document.querySelectorAll('.like-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

forms.forEach( (form) => {
  form.addEventListener('submit', function(event) {
  //   event.preventDefault()

  //   const postId = event.target.dataset.postId
  //   axios({
  //     method : 'post',
  //     url: `http://127.0.0.1:8000/communities/${postId}/like/`,
  //     headers : {'X-CSRFToken': csrftoken},
  //   })

  //   .then((response) => {
  //     const like = response.data.like
  //     // const likeBtn = document.querySelector(`#like-${postId}`)
  //     const likeBtni = form.querySelector('#like-heart')
  //     const postLikeCount = form.querySelector('#post-like-count')
  //     if (like === true) {
  //       postLikeCount.textContent = parseInt(postLikeCount.textContent) + 1
  //       likeBtni.classList.remove('bi-heart')
  //       likeBtni.classList.add('bi-heart-fill')
  //     } else {
  //       postLikeCount.textContent = parseInt(postLikeCount.textContent) - 1
  //       likeBtni.classList.remove('bi-heart-fill')
  //       likeBtni.classList.add('bi-heart')
  //     }
  //   })

  //   .catch((error) => {
  //     console.log(error.response)
  //   })
  event.preventDefault()
  const postId = event.target.dataset.postId
  let likePostCount = form.querySelector('#post-like-count')

  axios({
    method : 'post',
    url: `/communities/${postId}/like/`,
    headers: {'X-CSRFToken': csrftoken},
  })
  .then((response) => {
    const isLiked = response.data.is_liked
    const likeIcon = form.querySelector('i')
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
})