document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#propertyCarousel').addEventListener('slid.bs.carousel', propertyCarouselSlide);
  document.querySelectorAll('.area-carousel').forEach(el => el.addEventListener('slid.bs.carousel', areaCarouselSlide));
});


const propertyCarouselSlide = (event) => {
  let propertyId = document.querySelector('#propertyCarousel .carousel-item.active').getAttribute('data-property-id');
  document.querySelectorAll('.property-areas').forEach(section => {
    if (section.getAttribute('data-property-id') === propertyId) {
      section.style.display = 'block';
    } else {
      section.style.display = 'none';
    }
  });

  document.querySelectorAll('.area-images').forEach(section => section.style.display = 'none');
}

const areaCarouselSlide = (event) => {
  let areaId = event.target.querySelector('.carousel-item.active').getAttribute('data-area-id');
  document.querySelectorAll('.area-images').forEach(section => {
    if (section.getAttribute('data-area-id') === areaId) {
      section.style.display = 'block';
    } else {
      section.style.display = 'none';
    }
  });
}