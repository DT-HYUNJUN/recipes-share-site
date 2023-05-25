const moreBtn = document.getElementById('more-btn')
let i = 1
moreBtn.addEventListener('click', () => {
  const recipe = document.getElementById(`recipe-hidden-${i}`)
  recipe.classList.remove('hidden')
  recipe.classList.add('grid')
  if (i == 2) {
    moreBtn.classList.add('hidden')
  }
  i += 1
})