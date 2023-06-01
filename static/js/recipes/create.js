// step
let formContainer = document.querySelector('#form-container')
let stepForm = document.querySelectorAll('.step-form')
let addStep = document.querySelector('#add-step')
let totalSteps = document.querySelector('#id_recipestep_set-TOTAL_FORMS')
let stepNum = stepForm.length - 1

addStep.addEventListener('click', addDetail)

function addDetail(e) {
  e.preventDefault()

  let newForm = stepForm[0].cloneNode(true)
  let formRegex = RegExp(`recipestep_set-(\\d){1}-`, 'g')

  stepNum++
  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `recipestep_set-${stepNum}-`)
  newForm.innerHTML = newForm.innerHTML.replace()
  formContainer.insertBefore(newForm, addStep)
  totalSteps.setAttribute('value', `${stepNum + 1}`)
}

// ingredient
let ingredientForm = document.querySelectorAll('.ingredient-form')
let addIngredient = document.querySelector('#add-ingredient')
let totalForms = document.querySelector('#id_recipeingredient_set-TOTAL_FORMS')
let formNum = ingredientForm.length - 1

addIngredient.addEventListener('click', addForm)

function addForm(e) {
  e.preventDefault()

  let newForm = ingredientForm[0].cloneNode(true)
  let formRegex = RegExp(`recipeingredient_set-(\\d){1}-`,'g')

  formNum++
  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `recipeingredient_set-${formNum}-`)
  newForm.innerHTML = newForm.innerHTML.replace()
  formContainer.insertBefore(newForm, addIngredient)
  totalForms.setAttribute('value', `${formNum + 1}`)

  $(function() {
    $(newForm.querySelector('select')).select2()
  })

  newForm.classList.remove('hidden')
  let options = newForm.querySelector('.select2-container')
  let quantity = newForm.querySelector('.textinput')
  console.log(options)
  options.style.width = '60%'
  quantity.classList.add('ms-4')
  quantity.classList.add('py-0.5')
}