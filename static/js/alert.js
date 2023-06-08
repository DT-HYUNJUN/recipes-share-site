console.log('alert 작동중')

const closeAlert = document.getElementById('close-alert')

if (!sessionStorage.getItem('weather-info-dismissed')) {
  console.log('세션 없음')
  // Show the alert
  const alertElement = document.getElementById('weather-info');
  alertElement.classList.remove('hidden')
  alertElement.classList.add('flex', 'justify-center')
}

if (sessionStorage.getItem('weather-info-dismissed')) {
  // Show the alert
  console.log('세션 있음')
  const alertElement = document.getElementById('weather-info');
  alertElement.classList.remove('flex', 'justify-center')
  alertElement.classList.add('hidden')
}

closeAlert.addEventListener('click', () => {
  console.log('dismiss')
  const alertElement = document.getElementById('weather-info');
  alertElement.style.display = 'none';

  // Set the session storage to prevent showing the alert again
  sessionStorage.setItem('weather-info-dismissed', 'true');
})

///////////////////////////////////////////////////////////////////////////

const closeBirthday = document.getElementById('close-birthday')

// if (!sessionStorage.getItem('birthday-info-dismissed')) {
//   console.log('세션 없음')
//   // Show the alert
//   const alertElement = document.getElementById('birthday-alert');
//   alertElement.classList.remove('hidden')
//   alertElement.classList.add('fixed')
// }

// if (sessionStorage.getItem('birthday-info-dismissed')) {
//   // Show the alert
//   console.log('세션 있음')
//   const alertElement = document.getElementById('birthday-alert');
//   alertElement.classList.remove('fixed')
//   alertElement.classList.add('hidden')
// }

closeBirthday.addEventListener('click', () => {
  console.log('dismiss')
  const alertElement = document.getElementById('birthday-alert');
  alertElement.style.display = 'none';

  // Set the session storage to prevent showing the alert again
  sessionStorage.setItem('birthday-info-dismissed', 'true');
})