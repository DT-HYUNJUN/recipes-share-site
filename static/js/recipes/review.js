const reviewSection = document.querySelector('#reviews')
const reviews = document.querySelectorAll('#review')

reviews.forEach(review => {
  const input = review.querySelector('input')
  const aTags = review.querySelectorAll('a')
  const editBtn = aTags[0]
  const deleteBtn = aTags[1]
  const submitSection = review.querySelector('#submit-section')
  const submitBtn = submitSection.querySelectorAll('span')[0]
  const cancelBtn = submitSection.querySelectorAll('span')[1]
  const reviewContent = review.querySelector('#review-content')
  
  editBtn.addEventListener('click', () => {
    reviewContent.classList.add('hidden')
    input.classList.remove('hidden')
    submitSection.classList.remove('invisible')
  })

  cancelBtn.addEventListener('click', () => {
    reviewContent.classList.remove('hidden')
    input.classList.add('hidden')
    submitSection.classList.add('invisible')
  })

  submitBtn.addEventListener('click', () => {
    let param = {
      'reviewPk': review.dataset.reviewPk,
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
        input.value = data.content
        input.readOnly = true
        input.classList.remove('border-1')
        input.classList.add('border-0')
        submitSection.classList.add('invisible')
      },
      error: function() {
        alert('오류!')
      }
    })
  })

  // deleteBtn.addEventListener('click', () => {
  //   // let param = {
  //   //   'reviewPk': review.dataset.reviewPk,
  //   //   'recipePk': review.dataset.recipePk,
  //   // }

  //   // $.ajax({
  //   //   url: review.dataset.deleteUrl,
  //   //   type: 'POST',
  //   //   headers: {
  //   //     'X-CSRFTOKEN': review.dataset.csrftoken
  //   //   },
  //   //   data: JSON.stringify(param),
  //   //   success:function(data) {
  //   //     reviewSection.removeChild(review)
  //   //   },
  //   //   error: function() {
  //   //     alert('오류!')
  //   //   }
  //   // })
  // })
});