const adjListBtn = document.querySelector('#adj-list-btn')
const adjList = document.querySelector('#adj-list')

adjListBtn.addEventListener('click', () => {
  adjList.classList.toggle('hidden')
  adjList.classList.toggle('grid')
})