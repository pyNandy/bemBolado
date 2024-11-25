let show = true;
const menuContent = document.querySelector('.content');
const menuToggle = menuContent.querySelector('.menu-toggle');

menuToggle.addEventListener('click', () => {
    document.body.style.overflow = show ? 'hidden' : 'initial';
    document.body.classList.toggle('menu-open', show);
    menuContent.classList.toggle('on', show);
    show = !show;
});

window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && menuContent.classList.contains('on')) {
        document.body.style.overflow = 'initial';
        document.body.classList.remove('menu-open');
        menuContent.classList.remove('on');
        show = true;
    }
});

// Preload and animate images
document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll(".image-to-load");
    images.forEach(img => {
        img.onload = () => {
            img.classList.add("loaded");
        };
        if (img.complete) {
            img.classList.add("loaded");
        }
    });
});

// Fade-slide animation for elements on scroll
document.addEventListener("DOMContentLoaded", function() {
    const elements = document.querySelectorAll(".fade-slide");

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("loaded");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(element => {
        observer.observe(element);
    });
});

// Text animation for specific elements
document.addEventListener("DOMContentLoaded", function() {
    const textElements = document.querySelectorAll(".text-animation");
    
    textElements.forEach(text => {
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("loaded");
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });

        observer.observe(text);
    });
});
