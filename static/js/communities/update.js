const updateFormNumber = document.getElementById('id_images-INITIAL_FORMS').value

for (let i = 0; i < updateFormNumber; i++) {
  let targetDiv = document.getElementById(`div_id_images-${i}-image`)
  targetDiv.classList.add('truncate', 'w-5/6')
  targetDiv.children[2].classList.add('w-5/6')
  let targetDeleteDiv = document.getElementById(`div_id_images-${i}-DELETE`)
  targetDeleteDiv.classList.add('flex', 'flex-col')
  targetDeleteDiv.children[1].classList.add('self-center')
}