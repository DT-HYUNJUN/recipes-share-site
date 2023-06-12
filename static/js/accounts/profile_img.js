const profileImg = document.getElementById('id_profile_image')

profileImg.addEventListener('change', (ev) => {
  let input = ev.target
  if (input.files && input.files[0]) {
    let reader = new FileReader()
    reader.onload = function(e) {
      let imagePreview = document.getElementById('imagePreview')
      imagePreview.src = e.target.result
      imagePreview.style.display = 'block'
    }
    reader.readAsDataURL(input.files[0])
  }
})

function previewImage(event) {
    var input = event.target;
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var imagePreview = document.getElementById("imagePreview");
        imagePreview.src = e.target.result;
        imagePreview.style.display = "block";
      };
      reader.readAsDataURL(input.files[0]);
    }
  }