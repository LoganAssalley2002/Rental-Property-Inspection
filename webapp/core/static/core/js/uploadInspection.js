// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelector('#add_area').addEventListener('click', addArea);
// });

// window.addEventListener('load', () => {
//     document.querySelectorAll('.delete-area').forEach(el => el.addEventListener('click', removeArea));
// });


// const getLastIndex = () => {
//     let indices = [];
//     document.querySelectorAll('.area_form').forEach(el => indices.push(parseInt(el.getAttribute('data-area-index'))));

//     return Math.max(...indices);
// }

// const addArea = (event) => {
//     let newIndex = getLastIndex() + 1;
//     let newNode = document.querySelector('.area_form').cloneNode(true);
//     newNode.setAttribute('data-area-index', newIndex);

//     let imageInput = newNode.querySelector('input[type="file"]');
//     imageInput.setAttribute('id', `images_${newIndex}`);
//     imageInput.setAttribute('name', `images_${newIndex}`);
//     imageInput.value = '';

//     let areaName = newNode.querySelector('input[id*="id_name"]');
//     areaName.setAttribute('id', `id_name_${newIndex}`);
//     areaName.value = '';

//     let notes = newNode.querySelector('textarea[id*="id_notes"]');
//     notes.setAttribute('id', `id_notes_${newIndex}`);
//     notes.value = '';

//     newNode.querySelector('.delete-area').addEventListener('click', removeArea);

//     document.querySelector('#areas').appendChild(newNode);
// }

// const removeArea = (event) => {
//     if (document.querySelectorAll('.area_form').length > 1) {
//         event.target.closest('.area_form').remove();
//     }
// }