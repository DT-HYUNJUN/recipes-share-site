const API_KEY = "0cddd93fad8af4f81a2beab2d3a4041e"
console.log('test')
function onGeoOk(position) {
  console.log('geo ok')
  const lat = position.coords.latitude
  const lon = position.coords.longitude
  const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&lang=kr`
  fetch(url).then(respose => respose.json()).then(data => {
    const userWeather = document.getElementById('user-weather')
    const weatherIcon = document.getElementById('weather-icon')
    const name = data.name
    let weather = data.weather[0].main
    console.log(name, weather)

    if (weather == 'Clear') {
      weatherIcon.classList.add('bi-brightness-high')
    } else if(weather == 'Clouds' || weather == 'Haze') {
      weatherIcon.classList.add('bi-cloudy')
    } else if(weather == 'Snow') {
      weatherIcon.classList.add('bi-cloud-snow')
    } else if(weather == 'Rain' || weather == 'Drizzle' || weather == 'Mist') {
      weatherIcon.classList.add('bi-cloud-rain')
    }
    
    userWeather.textContent = `${name}의 현재 날씨: `
  })
}

function onGeoError() {
  console.log('Geo Error')
}

navigator.geolocation.getCurrentPosition(onGeoOk)