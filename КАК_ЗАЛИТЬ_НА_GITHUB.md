# 📤 Как залить DjanCar на GitHub — подробная инструкция

Эта инструкция для тех, кто **никогда не работал с Git/GitHub**.
Всё на Windows. Каждый шаг разжёван.

---

## ⏱ Общее время: 15–20 минут

| Шаг | Что делаем | Время |
|-----|-----------|-------|
| 1   | Устанавливаем Git | 3 мин |
| 2   | Создаём аккаунт GitHub | 2 мин |
| 3   | Настраиваем Git локально | 1 мин |
| 4   | Создаём токен доступа (PAT) | 3 мин |
| 5   | Создаём репозиторий на GitHub | 1 мин |
| 6   | Заливаем код через команды | 5 мин |

---

## 🔧 ШАГ 1 — Установить Git

### Проверь, может уже стоит
Открой **PowerShell** (Win+R → набираешь `powershell` → Enter) и набери:

```powershell
git --version
```

Если видишь что-то типа `git version 2.43.0` — **переходи к шагу 2**.
Если ошибка "не является командой" — ставим:

### Установка
1. Скачай: https://git-scm.com/download/win
2. Запусти установщик
3. **На все вопросы жми Next** — настройки по умолчанию подходят
4. После установки **закрой и заново открой PowerShell**
5. Проверь снова: `git --version`

---

## 👤 ШАГ 2 — Создать аккаунт GitHub

1. Заходи на https://github.com/signup
2. Введи **email** (рабочий, на него придёт код)
3. Придумай **пароль** (минимум 8 символов, должен содержать цифры)
4. Придумай **username** — это будет твой ник, появится в URL
   - Например: `surfakep`, `ivan-ulyanovsk`, `djancar-dev`
   - Только латиница, цифры и дефис
   - **Запомни его** — он будет в адресе репозитория
5. Подтверди email — открой письмо от GitHub, скопируй код, вставь
6. На вопросы про "How do you plan to use GitHub?" — выбирай любое
7. Тариф — **Free**

✅ Готово, у тебя есть аккаунт.

---

## ⚙️ ШАГ 3 — Настроить Git на компьютере (один раз навсегда)

Открой PowerShell и выполни две команды (подставь СВОИ имя и email):

```powershell
git config --global user.name "Ivan Ivanov"
git config --global user.email "tvoi-email@example.com"
```

Email должен быть **тот же, что в GitHub-аккаунте**.

Проверь:
```powershell
git config --global user.name
git config --global user.email
```

Должны вывести то, что ввёл.

---

## 🔑 ШАГ 4 — Создать Personal Access Token (PAT)

**ВАЖНО**: GitHub с 2021 года не принимает обычный пароль при `git push`.
Нужен специальный токен. Это просто.

1. Зайди на https://github.com/settings/tokens/new
   (если попросит залогиниться — войди)

2. Заполни:
   - **Note**: `DjanCar Deploy` (или что хочешь — для себя)
   - **Expiration**: `90 days` (или `No expiration` для удобства)
   - **Select scopes**: поставь галку напротив **`repo`** (все галочки внутри отметятся автоматически)

3. Внизу страницы — кнопка **Generate token**

4. ⚠️ **СРАЗУ скопируй токен** (выглядит как `ghp_xxxxxxxxxxxxxxx`)
   После закрытия страницы ты его больше **никогда не увидишь!**
   Сохрани его в Блокнот на всякий случай.

---

## 📁 ШАГ 5 — Создать репозиторий на GitHub

1. Зайди на https://github.com/new
2. Заполни:
   - **Repository name**: `djancar`
   - **Description** (опционально): `Diploma project — carsharing in Ulyanovsk`
   - **Public** (если хочешь, чтобы все видели) или **Private** (только ты)
   - **НЕ ставь** галочки:
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license

   Почему? Потому что у тебя в проекте они уже есть.

3. Нажми **Create repository**

4. После создания GitHub покажет страницу с командами. Скопируй URL вверху:
   ```
   https://github.com/ТВОЙ_USERNAME/djancar.git
   ```
   Он понадобится в шаге 6.

---

## 🚀 ШАГ 6 — Залить код

Открой PowerShell **в папке проекта**:

**Вариант А (простой)**: Открой проводник Windows, зайди в `C:\Users\User\Desktop\jankar`,
в адресной строке вверху сотри путь и напечатай `powershell` → Enter.
PowerShell откроется сразу в этой папке.

**Вариант Б**: В уже открытом PowerShell:
```powershell
cd C:\Users\User\Desktop\jankar
```

Теперь по очереди вводи команды и жми Enter после каждой:

### 6.1 — Инициализация
```powershell
git init
```
Выведет: `Initialized empty Git repository...`

### 6.2 — Создать главную ветку
```powershell
git branch -M main
```
Ничего не выведет — это нормально.

### 6.3 — Добавить все файлы
```powershell
git add .
```
Точка в конце — обязательна! Может вывести предупреждения про `LF/CRLF` — игнорируй.

### 6.4 — Проверить что добавилось
```powershell
git status
```
Увидишь длинный список зелёных файлов — это значит, всё готово к коммиту.

### 6.5 — Первый коммит
```powershell
git commit -m "DjanCar diploma project - initial commit"
```
Выведет: `[main (root-commit) abc1234] DjanCar...` и список файлов.

### 6.6 — Привязать GitHub-репозиторий

**Подставь свой username** вместо `TVOI_USERNAME`:
```powershell
git remote add origin https://github.com/TVOI_USERNAME/djancar.git
```
Ничего не выведет — это нормально.

### 6.7 — Залить (самый волнующий момент!)
```powershell
git push -u origin main
```

GitHub попросит логин/пароль:
- **Username**: твой username с GitHub
- **Password**: вставь **PAT-токен** из Шага 4 (НЕ обычный пароль!)
  - Правый клик мыши в PowerShell — это и есть Paste
  - Токен НЕ показывается при вводе — это нормально, просто жми Enter

Если всё ок — побежит прогресс-бар:
```
Enumerating objects: 67, done.
Counting objects: 100% (67/67), done.
...
To https://github.com/TVOI_USERNAME/djancar.git
 * [new branch]      main -> main
```

🎉 **Готово! Код на GitHub!**

Открой https://github.com/TVOI_USERNAME/djancar — увидишь все свои файлы.

---

## 🐛 Если что-то пошло не так

### Ошибка: `'git' is not recognized`
Не установлен Git или PowerShell открыт ещё до установки.
→ Закрой и заново открой PowerShell. Если не помогло — переустанови Git.

### Ошибка: `Permission denied (publickey)` или `authentication failed`
Ввёл не тот пароль. Должен быть **PAT-токен**, а не пароль от GitHub.
→ Создай новый токен (Шаг 4) и попробуй снова:
```powershell
git push -u origin main
```

### Ошибка: `remote origin already exists`
Ты уже делал `git remote add origin` ранее.
→ Удали и пересоздай:
```powershell
git remote remove origin
git remote add origin https://github.com/TVOI_USERNAME/djancar.git
```

### Ошибка: `Updates were rejected because the remote contains work`
GitHub-репозиторий уже не пустой (ты случайно поставил галочку Add README при создании).
→ Самый простой способ:
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Ошибка: `failed to push some refs` или `rejected (fetch first)`
Та же причина. То же решение, что выше.

### Окно с просьбой логина не появилось, а сразу ошибка
Возможно, у тебя сохранены старые креды.
→ Удали их:
```powershell
git config --global --unset credential.helper
```
И попробуй снова — должно появиться окошко.

### Push висит очень долго
Проект ~3 МБ, должен залиться за 10–30 секунд.
Если висит больше минуты — Ctrl+C, проверь интернет, попробуй снова.

---

## 📝 Как обновлять код потом

После каждого изменения файлов:

```powershell
git add .
git commit -m "что я изменил"
git push
```

Три команды. Этого достаточно.

Render автоматически подхватит изменения и перезапустит сайт.

---

## ✅ Что дальше

Когда код залит — переходи к **деплою на Render**.
Инструкция в файле [DEPLOY_RENDER.md](DEPLOY_RENDER.md), начиная с **Шага 2**.

---

## 🆘 Совсем не получается?

Скинь мне точный текст ошибки из PowerShell — помогу разобраться.
