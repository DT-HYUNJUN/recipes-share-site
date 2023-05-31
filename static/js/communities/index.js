const forms = document.querySelectorAll('.like-form')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  forms.forEach( (form) => {
    form.addEventListener('submit', function(event) {
      event.preventDefault()

      const postId = event.target.dataset.postId
      axios({
        method : 'post',
        url: `http://127.0.0.1:8000/communities/${postId}/like/`,
        headers : {'X-CSRFToken': csrftoken},
      })

      .then((response) => {
        const like = response.data.like
        const likeBtn = document.querySelector(`#like-${postId}`)
        const likeBtni = form.querySelector('#like-heart')
        // const postLikeCount = form.querySelector('#post-like-count')
        if (like === true) {
          const postLikeCount = form.querySelector('#post-like-count')
          console.log(postLikeCount)
          likeBtni.classList.remove('bi-heart')
          likeBtni.classList.add('bi-heart-fill')
          postLikeCount.textContent = String(parserInt(postLikeCount) + 1)
          
        } else {
          const postLikeCount = form.querySelector('#post-like-count')
          console.log(postLikeCount)
          likeBtni.classList.remove('bi-heart-fill')
          likeBtni.classList.add('bi-heart')
          postLikeCount.textContent = String(parserInt(postLikeCount) - 1)
        }
      })

      .catch((error) => {
        console.log(error.response)
      })
    })
  })