// DjanCar — общий JS
(function () {
    'use strict';

    // Закрытие алертов через 6 секунд
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(a => {
            a.style.transition = 'opacity 0.4s';
            a.style.opacity = '0';
            setTimeout(() => a.remove(), 500);
        });
    }, 6000);

    // Закрытие мобильного меню при клике на ссылку
    document.querySelectorAll('.main-nav a').forEach(a => {
        a.addEventListener('click', () => document.body.classList.remove('menu-open'));
    });

    // Подсветка активного пункта меню
    const path = window.location.pathname;
    document.querySelectorAll('.main-nav a').forEach(a => {
        if (a.getAttribute('href') === path) {
            a.style.background = 'var(--bg-grey)';
            a.style.color = 'var(--primary)';
        }
    });

    // Плавное появление при скролле
    const observer = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.style.opacity = '1';
                e.target.style.transform = 'translateY(0)';
                observer.unobserve(e.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.section-head, .how-card, .feature, .review, .team-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s, transform 0.6s';
        observer.observe(el);
    });
})();
