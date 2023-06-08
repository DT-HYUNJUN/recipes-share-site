const API_KEY = "0cddd93fad8af4f81a2beab2d3a4041e"
const gotoRecipe = document.getElementById('goto-recipe')
function onGeoOk(position) {
  const lat = position.coords.latitude
  const lon = position.coords.longitude
  const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&lang=kr`
  fetch(url).then(respose => respose.json()).then(data => {
    const userWeather = document.getElementById('user-weather')
    const weatherIcon = document.getElementById('weather-icon')
    const weatherInfoText = document.getElementById('weather-info-text')
    
    const name = data.name
    let weather = data.weather[0].main

    if (weather == 'Clear') {
      weatherIcon.classList.add('bi-brightness-high')
      weatherInfoText.textContent = '오늘 같이 맑은 날에는 '
      gotoRecipe.textContent = '김치찌개'
    } else if(weather == 'Clouds' || weather == 'Haze') {
      weatherIcon.classList.add('bi-cloudy')
      weatherInfoText.textContent = '오늘 같이 흐린 날에는 '
      gotoRecipe.textContent = '하이볼'
    } else if(weather == 'Snow') {
      weatherIcon.classList.add('bi-cloud-snow')
      weatherInfoText.textContent = '오늘 같이 눈 오는 날에는 '
      gotoRecipe.textContent = '크림 파스타'
    } else if(weather == 'Rain' || weather == 'Drizzle' || weather == 'Mist') {
      weatherInfoText.textContent = '오늘 같이 비 오는 날에는 '
      gotoRecipe.textContent = '파전'
      weatherIcon.classList.add('bi-cloud-rain')
    }
    gotoRecipe.addEventListener('click', () => {
      link = gotoRecipe.dataset.link
      console.log(link)
      window.location.href = link + `?keyword=${gotoRecipe.textContent}`
    })
    userWeather.textContent = `${name}의 현재 날씨: `
  })
}

function onGeoError() {
  console.log('Geo Error')
}



navigator.geolocation.getCurrentPosition(onGeoOk,onGeoError)