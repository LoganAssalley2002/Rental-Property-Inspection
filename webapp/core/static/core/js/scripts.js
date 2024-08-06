
// document.addEventListener('DOMContentLoaded', function() {
//     const owl = document.getElementById('walkingOwl'); // Get the owl element
//     if (!owl) return; // If the owl element does not exist, stop execution

//     let left = 45; // Starting position
//     let direction = 1; // 1 for moving right, -1 for moving left

//     function moveOwl() {
//         left += direction; // Increment or decrement left position based on direction
//         if (left > window.innerWidth - 45) {
//             direction = -1; // Change direction to left if it goes offscreen to the right
//         } else if (left < 45) {
//             direction = 1; // Change direction to right if it goes offscreen to the left
//         }
//         owl.style.left = left + 'px'; // Update position
//     }

//     setInterval(moveOwl, 2);
// });

// window.addEventListener('DOMContentLoaded', event => {

//     // Navbar shrink function
//     var navbarShrink = function () {
//         const navbarCollapsible = document.body.querySelector('#mainNav');
//         if (!navbarCollapsible) {
//             return;
//         }
//         if (window.scrollY === 0) {
//             navbarCollapsible.classList.remove('navbar-shrink')
//         } else {
//             navbarCollapsible.classList.add('navbar-shrink')
//         }

//     };

//     // Shrink the navbar 
//     navbarShrink();

//     // Shrink the navbar when page is scrolled
//     document.addEventListener('scroll', navbarShrink);

//     // Activate Bootstrap scrollspy on the main nav element
//     const mainNav = document.body.querySelector('#mainNav');
//     if (mainNav) {
//         new bootstrap.ScrollSpy(document.body, {
//             target: '#mainNav',
//             rootMargin: '0px 0px -40%',
//         });
//     };

//     // Collapse responsive navbar when toggler is visible
//     const navbarToggler = document.body.querySelector('.navbar-toggler');
//     const responsiveNavItems = [].slice.call(
//         document.querySelectorAll('#navbarResponsive .nav-link')
//     );
//     responsiveNavItems.map(function (responsiveNavItem) {
//         responsiveNavItem.addEventListener('click', () => {
//             if (window.getComputedStyle(navbarToggler).display !== 'none') {
//                 navbarToggler.click();
//             }
//         });
//     });

// });


// $(document).ready(function(){
//     console.log("Document is ready");
//     var areaIndex = 1;
//     $("#add_area").off('click').on('click', function(){
//         console.log("Add Area button clicked");
//         var area_form = $(".area_form:first").clone(true); // Clone the form, including event handlers
//         console.log("Form cloned", area_form);
//         area_form.find('input, select, textarea').each(function() {
//             var newName = $(this).attr('name').replace('0', areaIndex);
//             $(this).attr('name', newName);
//             $(this).val(''); // Clear the input value
//         });
//         area_form.show(); // Show the form
//         $("#areas").append(area_form);
//         console.log("Form appended", area_form);
//         areaIndex++;
//     });
// });


// $(document).ready(function(){
//     var areaIndex = 0;
//     $("#add_area").off('click').on('click', function(){
//         var area_form = $(".area_form:first").clone(true);
//         areaIndex++;

//         // Update all input field names including file uploads
//         area_form.find('input, select, textarea').each(function() {
//             if ($(this).attr('name')) {
//                 // Find the existing area index in the name
//                 var existingIndex = $(this).attr('name').match(/\d+/);
//                 console.log(existingIndex);
//                 console.log(areaIndex);
//                 if (existingIndex) {
//                     var newName = $(this).attr('name').replace(existingIndex[0], areaIndex); 
//                     $(this).attr('name', newName);
//                 }
//             }
//             $(this).val(''); 
//         });

//         $("#areas").append(area_form); 
//     });
// });


















































