// RANSOM SYNTAX - Student help chatbot widget
(function () {
  function getCookie(name) {
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var toggleBtn = document.getElementById('smc-chat-toggle');
    var closeBtn = document.getElementById('smc-chat-close');
    var chatWindow = document.getElementById('smc-chat-window');
    var chatBody = document.getElementById('smc-chat-body');
    var chatForm = document.getElementById('smc-chat-form');
    var chatInput = document.getElementById('smc-chat-input');
    var quickBtns = document.querySelectorAll('.smc-quick-btn');

    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', function () {
      chatWindow.classList.toggle('d-none');
      if (!chatWindow.classList.contains('d-none')) {
        chatInput.focus();
      }
    });
    closeBtn.addEventListener('click', function () {
      chatWindow.classList.add('d-none');
    });

    function addMessage(text, sender, link) {
      var div = document.createElement('div');
      div.className = 'smc-msg ' + (sender === 'user' ? 'smc-msg-user' : 'smc-msg-bot');
      div.textContent = text;
      if (link) {
        div.appendChild(document.createElement('br'));
        var a = document.createElement('a');
        a.href = link;
        a.textContent = 'Click here →';
        div.appendChild(a);
      }
      chatBody.appendChild(div);
      chatBody.scrollTop = chatBody.scrollHeight;
    }

    function sendMessage(message) {
      addMessage(message, 'user');
      fetch('/chatbot/ask/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ message: message })
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          addMessage(data.reply, 'bot', data.link);
        })
        .catch(function () {
          addMessage("Sorry, something went wrong. Please try the Enquiry form instead.", 'bot');
        });
    }

    chatForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var message = chatInput.value.trim();
      if (!message) return;
      sendMessage(message);
      chatInput.value = '';
    });

    quickBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        sendMessage(btn.getAttribute('data-q'));
      });
    });
  });
})();
