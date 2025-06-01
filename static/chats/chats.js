document.addEventListener('DOMContentLoaded', function() {
    // Извлечение и парсинг данных пользователя из localStorage
    var userData = JSON.parse(localStorage.getItem('user_data'));
    var userName = userData ? userData.name : 'Аноним'; // Использовать имя пользователя или 'Аноним', если данных нет

    // Обработка нажатия кнопки отправки сообщения
    document.getElementById("send").addEventListener("click", sendMessage);
    document.getElementById("text_message").addEventListener("keydown", function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        var messageText = document.getElementById("text_message").value;
        if (messageText.length > 0) {
            fetch('/chats/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ message: messageText }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка при отправке сообщения');
                }
                return response.json();
            })
            .then(data => {
                displayMessage(userName, messageText);
                document.getElementById("text_message").value = "";
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        }
    }
});

// Функция для отображения сообщения
function displayMessage(userName, messageText) {
    var messageCont = document.getElementById("message_block");

    var messageDiv = document.createElement("div");
    messageDiv.classList.add("message");

    var messageMeta = document.createElement("div");
    messageMeta.classList.add("meta");

    // Форматирование времени сообщения
    var date = new Date();
    var timeString = date.getHours().toString().padStart(2, '0') + ":" +
                     date.getMinutes().toString().padStart(2, '0') + ":" +
                     date.getSeconds().toString().padStart(2, '0');
                     
    messageMeta.innerText = `${userName} (${timeString})`;

    var messageContent = document.createElement("div");
    messageContent.classList.add("content");
    messageContent.textContent = messageText;

    messageDiv.appendChild(messageMeta);
    messageDiv.appendChild(messageContent);
    messageCont.appendChild(messageDiv);
}

// Функция для получения значения cookie по имени
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break; // Прерываем цикл, если нашли нужное cookie
            }
        }
    }
    return cookieValue;
}
