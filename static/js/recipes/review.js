const reviewSection = document.querySelector('#reviews')
const reviews = document.querySelectorAll('#review')

reviews.forEach(review => {
  const commentTextarea = review.querySelector('#comment-textarea')
  const input = review.querySelector('textarea')
  const aTags = review.querySelectorAll('a')
  const editBtn = aTags[0]
  const deleteBtn = aTags[1]
  const submitBtn = review.querySelector('#submit-btn')
  const cancelBtn = review.querySelector('#cancel-btn')
  const reviewContent = review.querySelector('#review-content')

  if (editBtn && deleteBtn) {
    editBtn.addEventListener('click', () => {
      reviewContent.classList.add('hidden')
      commentTextarea.classList.remove('hidden')

    })
  
    cancelBtn.addEventListener('click', () => {
      reviewContent.classList.remove('hidden')
      commentTextarea.classList.add('hidden')

    })
  
    submitBtn.addEventListener('click', () => {
      let param = {
        'pk': review.dataset.reviewPk,
        'content': input.value
      }
      
      $.ajax({
        url: review.dataset.updateUrl,
        type: 'POST',
        headers: {
          'X-CSRFTOKEN': review.dataset.csrftoken
        },
        data: JSON.stringify(param),
        success:function(data) {
          reviewContent.textContent = data.content
          commentTextarea.classList.add('hidden')
          reviewContent.classList.remove('hidden')
        },
        error: function() {
          alert('오류!')
        }
      })
    })
  }
  

  // deleteBtn.addEventListener('click', () => {
  //   let param = {
  //     'reviewPk': review.dataset.reviewPk,
  //     'recipePk': review.dataset.recipePk,
  //   }

  //   $.ajax({
  //     url: review.dataset.deleteUrl,
  //     type: 'POST',
  //     headers: {
  //       'X-CSRFTOKEN': review.dataset.csrftoken
  //     },
  //     data: JSON.stringify(param),
  //     success:function(data) {
  //       reviewSection.removeChild(review)
  //     },
  //     error: function() {
  //       alert('오류!')
  //     }
  //   })
  // })
});