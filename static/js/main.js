// DjanCar — общий JS
document.addEventListener('DOMContentLoaded', function () {


    // ===== БУРГЕР-МЕНЮ =====
    const burger = document.getElementById('burgerBtn');
    const backdrop = document.getElementById('mobileBackdrop');
    const menu = document.getElementById('mobileMenu');
    const body = document.body;

    function closeMenu() { body.classList.remove('menu-open'); }
    function toggleMenu() { body.classList.toggle('menu-open'); }

    if (burger) {
        burger.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            toggleMenu();
        });
    }
    if (backdrop) {
        backdrop.addEventListener('click', closeMenu);
    }
    // Закрытие меню при тапе на пункт
    if (menu) {
        menu.querySelectorAll('a').forEach(function (a) {
            a.addEventListener('click', closeMenu);
        });
    }
    // Закрытие по Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeMenu();
    });
    // Закрытие при изменении размера окна (поворот, ресайз)
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) closeMenu();
    });


    // ===== Авто-закрытие алертов =====
    setTimeout(function () {
        document.querySelectorAll('.alert').forEach(function (a) {
            a.style.transition = 'opacity 0.4s';
            a.style.opacity = '0';
            setTimeout(function () { a.remove(); }, 500);
        });
    }, 6000);


    // ===== Подсветка активного пункта меню =====
    const path = window.location.pathname;
    document.querySelectorAll('.desktop-nav a, .mobile-menu a').forEach(function (a) {
        const href = a.getAttribute('href');
        if (!href) return;
        if (href === path || (href !== '/' && path.startsWith(href))) {
            a.style.background = 'var(--bg-grey)';
            a.style.color = 'var(--primary)';
        }
    });


    // ===== Плавное появление при скролле =====
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.style.opacity = '1';
                    e.target.style.transform = 'translateY(0)';
                    observer.unobserve(e.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.section-head, .how-card, .feature, .review, .team-card').forEach(function (el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s, transform 0.6s';
            observer.observe(el);
        });
    }
});
