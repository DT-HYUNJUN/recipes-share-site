const input = document.getElementById('input')

input.onfocus = function () {
  browsers.style.display = 'block';
  input.style.borderRadius = "5px 5px 0 0";  
};

setInterval(() => {
  for (let option of browsers.options) {
    option.onclick = function () {
      input.value = option.value;
      browsers.style.display = 'none';
      input.style.borderRadius = "5px";
      input.focus()
    }
  }
}, 1)

input.oninput = function() {
  currentFocus = -1;
  var text = input.value.toUpperCase();
  for (let option of browsers.options) {
    if(option.value.toUpperCase().indexOf(text) > -1){
      option.style.display = "block";
  }else{
    option.style.display = "none";
    }
  };
}
var currentFocus = -1;
input.onkeydown = function(e) {
  if(e.keyCode == 40){
    currentFocus++
   addActive(browsers.options);
  }
  else if(e.keyCode == 38){
    currentFocus--
   addActive(browsers.options);
  }
  else if(e.keyCode == 13){
    e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (browsers.options) browsers.options[currentFocus].click();
        }
  }
}

function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("active");
  }
  function removeActive(x) {
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("active");
    }
  }

const fridgeList = document.getElementById('fridge-list')
const buttonList = fridgeList.querySelectorAll('button')
const datalist = document.getElementById('browsers')
const ingredients = datalist.querySelectorAll('option')
const ingrdDeleteBtn = document.getElementById('ingrd-delete')
const ingrdCancelBtn = document.getElementById('ingrd-cancel')
// const ingrdXBtn = document.getElementById('ingrd-x')
const emptyButton = []
let ingrdButton = []
const deletedBtnList = []
const toolTipList = []


// ingredients.forEach(ingredient => {
//   console.log(ingredient)
//   ingredient.addEventListener('click', () => {
//     input.value = ingredient.value
//     input.focus()
//   })
// })

buttonList.forEach(button => {
  const tooltipId = button.dataset.tooltipTarget
  const tooltip = document.getElementById(tooltipId)
  toolTipList.push(tooltip)
});

// buttonList.forEach(button => {
//   if (button.textContent === '+') {
//     emptyButton.push(button)
//   }
// });

// console.log(emptyButton)

const ingredientNames = []
const myIngredients = []

ingredients.forEach(ingredient => {
  ingredientNames.push(ingredient.value)
})

const fridgeForm = document.getElementById('fridge-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


// 재료 추가
input.addEventListener('keyup', function(e) {
  let start = 0
  if (e.keyCode == 13) {
    for (let i = 0; i < buttonList.length; i++) {
      if (buttonList[i].textContent === '+') {
        start = i
        break
      }
    }
    console.log(start)
    const value = input.value
    if (buttonList[start].textContent === '+') {
      if (ingredientNames.includes(value) && myIngredients.includes(value) != true) {
        let param = {
          target: value,
        };
        $.ajax({
          url: fridgeForm.dataset.url,
          type: "POST",
          headers: {
            "X-CSRFTOKEN": csrftoken,
          },
          data: JSON.stringify(param),
          success: function (data) {
            console.log(data)
            const toolTip = document.getElementById(`ingredient-${start+1}`)
            toolTip.textContent = value
            buttonList[start].textContent = value
            myIngredients.push(value)
            const toDeleteBtn = document.getElementById(value)
            deletedBtnList.push(toDeleteBtn.textContent)
            toDeleteBtn.remove()
            input.value = ""
          },
          error: function () {
            alert("오류!");
          },
        });
      } else {
        console.log('에러 발생~')
      }      
    }
    else {
      i += 1
    }
  }
})


// buttonList.forEach(button => {
//   if (button.textContent !== '+') {
//     ingrdButton.push(button)
//   }
// });

// 재료 삭제
ingrdDeleteBtn.addEventListener('click', () => {
  ingrdButton = []
  buttonList.forEach(button => {
    if (button.textContent !== '+') {
      ingrdButton.push(button)
    }
  });
  console.log(ingrdButton)
  ingrdDeleteBtn.classList.add('hidden')
  ingrdCancelBtn.classList.remove('hidden')
  ingrdButton.forEach(button => {
    button.classList.add('brightness-50')
    button.addEventListener('click', () => {
      // console.log(button.textContent)
      // console.log(button.id)
      // rearrange(button.id)
      let param = {
        target: button.textContent,
      };
      $.ajax({
        url: fridgeForm.dataset.url,
        type: "POST",
        headers: {
          "X-CSRFTOKEN": csrftoken,
        },
        data: JSON.stringify(param),
        success: function (data) {
          console.log(data)
          // const toolTip = document.getElementById(`ingredient-${start}`)
          const tooltipId = button.dataset.tooltipTarget
          const tooltip = document.getElementById(tooltipId)
          getDeletedBtnBack(button.textContent)
          tooltip.textContent = ''
          button.textContent = '+'
          rearrange(button.id)
        },
        error: function () {
          alert("오류!");
        },
      });
    })
  })
})

ingrdCancelBtn.addEventListener('click', () => {
  ingrdCancelBtn.classList.add('hidden')
  ingrdDeleteBtn.classList.remove('hidden')
  ingrdButton.forEach(button => {
    button.classList.remove('brightness-50')
  });
})

const rearrange = (id) => {
  const temp = []
  const idStart = parseInt(id)
  for (let i = idStart + 1; i < 10; i++) {
    if (buttonList[i-1].textContent !== '+') {
      temp.push(buttonList[i-1].textContent)
    }
  }
  temp.push('+')
  for (let i = 0; i < temp.length; i++) {
    // console.log(temp[i])
    // console.log(buttonList[i].textContent)
    // console.log(buttonList[idStart + i-1].textContent)
    // console.log(temp[i])
    buttonList[idStart + i - 1].textContent = temp[i]
    toolTipList[idStart + i - 1].textContent = temp[i]
    if (i === temp.length-1) {
      console.log('last')
      console.log(buttonList[i + idStart -1].classList.remove('brightness-50'))
    }
  }
}

const getDeletedBtnBack = (value) => {
  const ingrdBtnBack = document.createElement('option')
  ingrdBtnBack.setAttribute('id', value)
  ingrdBtnBack.setAttribute('value', value)
  ingrdBtnBack.textContent = value
  datalist.appendChild(ingrdBtnBack)
}