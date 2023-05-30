const pw1 = document.querySelector('#id_new_password1')
const pw2 = document.querySelector('#id_new_password2')

pw1.addEventListener('change', (e) => {
  if (pw1.value !== pw2.value) {
    pw2.setCustomValidity(" ")
  } else {
    pw2.setCustomValidity("")
  }
  pw2.reportValidity()
})

pw2.addEventListener('change', (e) => {
  if (pw1.value !== pw2.value) {
    pw2.setCustomValidity(" ")
  } else {
    pw2.setCustomValidity("")
  }
  pw2.reportValidity()
})