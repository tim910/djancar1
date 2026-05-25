# 🚀 Деплой DjanCar на Render.com

Пошаговая инструкция, чтобы выложить сайт в интернет за **15–20 минут**.

---

## 📋 Что понадобится

1. Аккаунт **GitHub** — https://github.com/signup (бесплатно)
2. Аккаунт **Render** — https://dashboard.render.com/register (можно войти через GitHub)
3. Установленный **Git** — https://git-scm.com/download/win

---

## ШАГ 1 — Залить проект на GitHub

Открой PowerShell в папке `c:\Users\User\Desktop\jankar` и выполни:

```powershell
git init
git add .
git commit -m "Initial commit — DjanCar diploma project"
git branch -M main
```

Затем:
1. Зайди на https://github.com/new
2. Назови репозиторий `djancar` (или как хочешь)
3. **НЕ** ставь галочки "Add README" — оно у тебя уже есть
4. Нажми **Create repository**
5. Скопируй команды, которые покажет GitHub. Они будут такие:

```powershell
git remote add origin https://github.com/ТВОЙ_ЛОГИН/djancar.git
git push -u origin main
```

При первом `git push` он попросит логин/пароль GitHub
(пароль — это **Personal Access Token**, не обычный пароль:
создать тут → https://github.com/settings/tokens/new, права: `repo`).

---

## ШАГ 2 — Деплой на Render (одной кнопкой через Blueprint)

В проекте уже есть файл [render.yaml](render.yaml) — он описывает всю инфраструктуру.

1. Заходи на https://dashboard.render.com/
2. Сверху справа: **New +** → **Blueprint**
3. Подключи свой GitHub (если не подключён) → выбери репозиторий `djancar`
4. Render прочтёт `render.yaml` и покажет:
   - 1 база данных PostgreSQL (бесплатная)
   - 1 веб-сервис (бесплатный)
5. Нажми **Apply** (или **Create New Resources**)
6. Ждёшь ~5 минут — Render:
   - создаёт БД
   - клонирует репозиторий
   - выполняет `build.sh` (установка, миграции, seed-данные)
   - запускает `gunicorn`

Когда статус веб-сервиса станет **Live** (зелёная точка),
у тебя будет ссылка вида:

```
https://djancar.onrender.com
```

🎉 Готово! Сайт в интернете.

---

## ШАГ 3 — Проверь, что работает

| Адрес | Что должно открыться |
|-------|----------------------|
| `https://djancar.onrender.com/` | Главная страница с hero |
| `https://djancar.onrender.com/cars/` | Каталог из 24 авто |
| `https://djancar.onrender.com/map/` | Интерактивная карта Ульяновска |
| `https://djancar.onrender.com/admin/` | Админка (admin / admin12345) |

**Логины**:
- `admin` / `admin12345` — суперюзер
- `demo` / `demo12345` — обычный юзер

---

## ⚠️ Особенности бесплатного тарифа Render

| Фактор | Free план |
|--------|-----------|
| Веб-сервис | Засыпает после **15 мин** простоя |
| Холодный старт | После сна сайт грузится **~30 секунд** |
| PostgreSQL | Срок жизни **90 дней**, потом нужно создать заново |
| Хранилище | 1 ГБ (хватит с запасом) |
| Трафик | 100 ГБ/месяц |

**Важно про медиа-файлы**: загруженные через админку фотографии **не сохраняются** при перезапуске сервиса (Render использует ephemeral диск).
Для дипломной защиты этого хватит — фото авто грузятся с Unsplash CDN, а не из локального `media/`.

Для постоянного хранилища потом можно подключить **Cloudinary** или **AWS S3**.

---

## 🗺 Яндекс.Карты на проде

Ключ `b5e72e64-eaed-42a4-ae58-307175123276` уже прописан в `render.yaml`.

Если карта не отрисуется на проде, нужно в кабинете Яндекс Облако
**добавить домен** `djancar.onrender.com` в список разрешённых для этого ключа:
https://developer.tech.yandex.ru/services/

---

## 🔄 Как обновлять сайт после изменений

Любой `git push` → Render автоматически:
1. Скачает свежий код
2. Запустит `build.sh`
3. Перезапустит сервер

```powershell
git add .
git commit -m "что я изменил"
git push
```

---

## 🐛 Если что-то пошло не так

В дашборде Render → твой сервис → вкладка **Logs**.
Там видны все ошибки сборки и runtime.

Частые проблемы:
- **`Build failed at collectstatic`** — забыл закоммитить файлы в `static/`. Проверь `git status`.
- **`Database not ready`** — Render иногда создаёт сервис раньше БД. Просто нажми **Manual Deploy** ещё раз.
- **`DisallowedHost`** — добавь домен в env `ALLOWED_HOSTS` через дашборд.

---

## 📝 Альтернатива: деплой вручную (без render.yaml)

Если Blueprint по какой-то причине не подходит:

### А. Создать PostgreSQL
1. Dashboard → **New +** → **PostgreSQL**
2. Name: `djancar-db`, Plan: **Free**
3. Скопируй **Internal Database URL** (понадобится через минуту)

### Б. Создать веб-сервис
1. Dashboard → **New +** → **Web Service**
2. Подключи репозиторий
3. Параметры:
   - **Name**: `djancar`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn djancar.wsgi:application`
   - **Plan**: Free
4. **Environment Variables**:
   ```
   DATABASE_URL = <Internal Database URL из БД>
   SECRET_KEY = <любая длинная случайная строка>
   DEBUG = False
   ALLOWED_HOSTS = .onrender.com
   YANDEX_MAPS_API_KEY = b5e72e64-eaed-42a4-ae58-307175123276
   PYTHON_VERSION = 3.12.7
   ```
5. **Create Web Service**

---

## ✅ Готово!

Сохрани ссылку `https://djancar.onrender.com` — её можно вставлять в **диплом**, **резюме** и **портфолио**.

Удачи на защите! 🎓🚗
