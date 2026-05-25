// DjanCar — общий JS
(function () {
    'use strict';

    // ===== Бургер-меню =====
    window.toggleMenu = function (e) {
        if (e) e.stopPropagation();
        document.body.classList.toggle('menu-open');
        const isOpen = document.body.classList.contains('menu-open');
        // Иконка ☰ → ✕
        const btn = document.querySelector('.burger');
        if (btn) btn.textContent = isOpen ? '✕' : '☰';
        // Блокируем скролл при открытом меню
        document.body.style.overflow = isOpen ? 'hidden' : '';
    };

    // Закрытие по клику на подложку (псевдоэлемент ::after на body)
    document.addEventListener('click', function (e) {
        if (!document.body.classList.contains('menu-open')) return;
        // если клик не по меню и не по бургеру — закрыть
        const isMenu = e.target.closest('.main-nav');
        const isBurger = e.target.closest('.burger');
        if (!isMenu && !isBurger) {
            window.toggleMenu();
        }
    });

    // Закрытие меню при клике на пункт
    document.querySelectorAll('.main-nav a').forEach(a => {
        a.addEventListener('click', () => {
            if (document.body.classList.contains('menu-open')) {
                window.toggleMenu();
            }
        });
    });

    // Закрытие по Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && document.body.classList.contains('menu-open')) {
            window.toggleMenu();
        }
    });

    // ===== Авто-закрытие алертов =====
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(a => {
            a.style.transition = 'opacity 0.4s';
            a.style.opacity = '0';
            setTimeout(() => a.remove(), 500);
        });
    }, 6000);

    // ===== Подсветка активного пункта меню =====
    const path = window.location.pathname;
    document.querySelectorAll('.main-nav a').forEach(a => {
        const href = a.getAttribute('href');
        if (href === path || (href !== '/' && path.startsWith(href))) {
            a.style.background = 'var(--bg-grey)';
            a.style.color = 'var(--primary)';
        }
    });

    // ===== Плавное появление при скролле =====
    if ('IntersectionObserver' in window) {
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
    }

    // ===== Свайп по краю экрана = открыть меню =====
    let touchStartX = 0;
    document.addEventListener('touchstart', e => {
        touchStartX = e.touches[0].clientX;
    }, { passive: true });
    document.addEventListener('touchend', e => {
        if (window.innerWidth > 768) return;
        const dx = e.changedTouches[0].clientX - touchStartX;
        const startedAtRightEdge = touchStartX > window.innerWidth - 30;
        if (dx < -50 && startedAtRightEdge && !document.body.classList.contains('menu-open')) {
            window.toggleMenu();
        }
        // Свайп вправо при открытом меню → закрыть
        if (dx > 80 && document.body.classList.contains('menu-open')) {
            window.toggleMenu();
        }
    }, { passive: true });
})();
