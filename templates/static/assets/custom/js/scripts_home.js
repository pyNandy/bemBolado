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
