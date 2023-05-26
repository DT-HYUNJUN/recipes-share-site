const reviews = document.querySelectorAll('#reviews')

reviews.forEach(review => {
  const input = review.querySelector('input')
  const aTags = review.querySelectorAll('a')
  const editBtn = aTags[0]
  const deleteBtn = aTags[1]

  editBtn.addEventListener('click', () => {
    
  })
});