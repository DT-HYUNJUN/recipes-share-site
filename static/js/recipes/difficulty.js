const difficultyForm = document.querySelector('#id_difficulty')
const difficultyInput = document.querySelector('#difficulty-input')
console.log(difficultyForm)
const stars = difficultyForm.querySelectorAll('svg')

// const starFill = (id) => {
//   return () => {
//     starFillReset()
//     const starId = id.substring(5);
//     for (let i = 1; i <= starId; i++) {
//       const starToFill = difficultyForm.querySelector(`#star-${i}`)
//       starToFill.setAttribute('fill', '#ffdd63')
//     }
//   }
// }

const starFillReset = () => {
  stars.forEach(star => {
    star.setAttribute('fill', '#eee')
  });
}

stars.forEach(star => {
  const starId = star.id.substring(5);
  star.addEventListener('mouseover', () => {  

  })
  star.addEventListener('click', () => {
    starFillReset()
    for (let i = 1; i <= starId; i++) {
      const starToFill = difficultyForm.querySelector(`#star-${i}`)
      starToFill.setAttribute('fill', '#ffdd63')
    }
    difficultyInput.value = starId
  })
});