const reviewSection = document.querySelector('#reviews')
const reviews = document.querySelectorAll('#review')

const reviewForm = document.querySelector('#review-form')
const reviewField = document.querySelector('#id_content')
reviewField.setAttribute('rows', '2')
reviewField.setAttribute('placeholder', '여기에 리뷰를 작성해보세요!')
reviewField.classList.add ('border-0')
reviewField.classList.add ('focus:ring-0')
reviewField.classList.add ('resize-none')

// const divIdContent = document.querySelector('#div_id_content')

reviews.forEach(review => {
  const dropdownBtn = review.querySelector('#dropdownDefaultButton')
  const pk = review.dataset.reviewPk
  const dropdown = review.querySelector(`#dropdown-${pk}`)
  const commentTextarea = review.querySelector('#comment-textarea')
  const input = review.querySelector('#review-update-field')
  const aTags = review.querySelectorAll('a')
  const editBtn = review.querySelector('#edit-btn')
  const deleteBtn = review.querySelector('#delete-btn')
  const submitBtn = review.querySelector('#submit-btn')
  const cancelBtn = review.querySelector('#cancel-btn')
  const reviewContent = review.querySelector('#review-content')

  if (editBtn) {
    editBtn.addEventListener('click', () => {
      reviewContent.classList.add('hidden')
      commentTextarea.classList.remove('hidden')
      dropdown.classList.add('hidden')
      dropdownBtn.classList.add('hidden')
    })
  
    cancelBtn.addEventListener('click', () => {
      reviewContent.classList.remove('hidden')
      commentTextarea.classList.add('hidden')
      dropdownBtn.classList.remove('hidden')
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
          dropdownBtn.classList.remove('hidden')
        },
        error: function() {
          alert('오류!')
        }
      })
    })

    deleteBtn.addEventListener('click', () => {
      let param = {
        'review_pk': review.dataset.reviewPk,
        'recipe_pk': review.dataset.recipePk,
      }

      $.ajax({
        url: review.dataset.deleteUrl,
        type: 'POST',
        headers: {
          'X-CSRFTOKEN': review.dataset.csrftoken
        },
        data: JSON.stringify(param),
        success:function(data) {
          reviewSection.removeChild(review)
        },
        error: function() {
          alert('오류!')
        }
      })
    })
  }
});


const reviewSubmit = reviewForm.querySelector('#review_create_submit')
reviewSubmit.addEventListener('click', (e) => {
  e.preventDefault()
  let param = {
    'pk': reviewForm.dataset.pk,
    'content': reviewField.value
  }
  $.ajax({
    url: reviewForm.dataset.url,
    type: 'POST',
    headers: {
      'X-CSRFTOKEN': reviewForm.dataset.csrftoken
    },
    data: JSON.stringify(param),
    success:function(data) {
      
    },
    error: function() {
      alert('오류!')
    }
  })
})
// // 리뷰