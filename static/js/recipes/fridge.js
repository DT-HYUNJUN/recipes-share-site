const input = document.getElementById('input')

input.onfocus = function () {
  browsers.style.display = 'block';
  input.style.borderRadius = "5px 5px 0 0";  
};
for (let option of browsers.options) {
  option.onclick = function () {
    input.value = option.value;
    browsers.style.display = 'none';
    input.style.borderRadius = "5px";
    input.focus()
  }
};

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
const emptyButton = []

buttonList.forEach(button => {
  if (button.textContent === '+') {
    emptyButton.push(button)
  }
});

console.log(emptyButton)

const ingredientNames = []
const myIngredients = []

ingredients.forEach(ingredient => {
  ingredientNames.push(ingredient.value)
})

const fridgeForm = document.getElementById('fridge-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

i = 1
input.addEventListener('keyup', function(e) {
  if (e.keyCode == 13) {
    const value = e.target.value
    if (buttonList[i].textContent === '+') {
      if (ingredientNames.includes(value) && myIngredients.includes(value) != true ) {
        let param = {
          // target에 ingredient pk가 들어가야 함
          target: input.value,
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
            const toolTip = document.getElementById(`ingredient-${i}`)
            toolTip.textContent = value
            buttonList[i].textContent = value
            myIngredients.push(value)
            // datalist.removeChild(buttonList[i])
            input.value = ""
            i += 1
          },
          error: function () {
            alert("오류!");
          },
        });
      } else {
        console.log('에러 발생~')
      }      
    }
  }
})