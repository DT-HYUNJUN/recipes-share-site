// ingredient existed
let updateForms = document.querySelectorAll('.ingredient-update-form')

updateForms.forEach(form => {
  $(function() {
    $(form.querySelector('select')).select2({
      width: '60%'
    })
  })
  let quantity = form.querySelector('.textinput')
  quantity.classList.add('py-0.5')
  quantity.parentNode.classList.add('grow')
})

// step existed
let stepForms = document.querySelectorAll('.step-update-form')

stepForms.forEach(form => {
  form.classList.add('flex', 'gap-2')
  form.querySelector('label').textContent = 'X'
  form.querySelector('label').classList.remove('mb-2')
  form.querySelector('label').classList.add('mb-1', 'text-red-500')
  form.childNodes[1].classList.add('grow')
  form.childNodes[5].classList.add('flex', 'flex-col', 'items-center')
})

// variables
let title = document.querySelector('#div_id_title')
let image = document.querySelector('#div_id_image')
let ingredientForm = document.querySelectorAll('.ingredient-form')
let addIngredient = document.querySelector('#add-ingredient')
let totalForms = document.querySelector('#id_recipeingredient_set-TOTAL_FORMS')
let ingredientLabel = document.querySelector('#ingredient_label')
let formNum = ingredientForm.length - 1
let line = document.querySelector('#bottom-line')
let formContainer = document.querySelector('#form-container')
let stepForm = document.querySelectorAll('.step-form')
let addStep = document.querySelector('#add-step')
let totalSteps = document.querySelector('#id_recipestep_set-TOTAL_FORMS')
const ingredientSection = document.getElementById('ingredients-section')
const stepSection = document.getElementById('steps-section')
const category = document.getElementById('id_category')
const time = document.getElementById('id_time')
let stepNum = stepForm.length - 1

// base form
title.classList.add('grow')
image.querySelector('input').classList.add('w-full')
time.classList.add('py-0.5')

$(function() {
  $(category).select2({
    containerCssClass: 'error'
  })
})

// step
addStep.addEventListener('click', addDetail)

function addDetail(e) {
  e.preventDefault()

  let newForm = stepForm[0].cloneNode(true)
  let formRegex = RegExp(`recipestep_set-(\\d){1}-`, 'g')

  stepNum++
  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `recipestep_set-${stepNum}-`)
  newForm.innerHTML = newForm.innerHTML.replace()
  // formContainer.insertBefore(newForm, ingredientLabel)
  newForm.classList.remove('hidden')
  stepSection.insertBefore(newForm, line)
  totalSteps.setAttribute('value', `${stepNum + 1}`)
}

// ingredient
addIngredient.addEventListener('click', addForm)

function addForm(e) {
  e.preventDefault()

  let newForm = ingredientForm[0].cloneNode(true)
  let formRegex = RegExp(`recipeingredient_set-(\\d){1}-`,'g')

  formNum++
  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `recipeingredient_set-${formNum}-`)
  newForm.innerHTML = newForm.innerHTML.replace()
  quantityInput = newForm.querySelector('input')
  quantityInput.setAttribute('placeholder', '수량을 입력해주세요')
  ingredientSection.insertBefore(newForm, line)
  totalForms.setAttribute('value', `${formNum + 1}`)

  $(function() {
    $(newForm.querySelector('select')).select2({
      tags: true,
      width: '60%'
    })
  })

  newForm.classList.remove('hidden')
  let quantity = newForm.querySelector('.textinput')
  quantity.classList.add('py-0.5')
  quantity.parentNode.classList.add('grow')
}

const equipForm = document.getElementById('equip-form')
const labels = equipForm.querySelectorAll('div > label')
labels.forEach(label => {
  label.classList.remove('mb-2')
})

const microwave = document.getElementById('div_id_microwave')
microwave.classList.add('flex', 'justify-between', 'w-32')
microwave.classList.remove('mb-3')

const stove = document.getElementById('div_id_stove')
stove.classList.add('flex', 'justify-between', 'w-32')
stove.classList.remove('mb-3')

const oven = document.getElementById('div_id_oven')
oven.classList.add('flex', 'justify-between', 'w-32')
oven.classList.remove('mb-3')

const airFryer = document.getElementById('div_id_air_fryer')
airFryer.classList.add('flex', 'justify-between', 'w-32')
airFryer.classList.remove('mb-3')