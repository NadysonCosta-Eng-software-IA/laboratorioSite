// Script básico para interações futuras
// Por enquanto, vazio - podemos adicionar animações de rolagem ou validação de formulário depois

document.addEventListener('DOMContentLoaded', function() {
    console.log('Página carregada com sucesso!');
});

// Carrossel de imagens no hero
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    slides[index].classList.add('active');
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}

// Inicia o carrossel automático a cada 3 segundos
setInterval(nextSlide, 3000);

// Mostra a primeira slide
showSlide(currentSlide);