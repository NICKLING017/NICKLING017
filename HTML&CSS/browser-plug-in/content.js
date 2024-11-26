let notificationElement = null;

function showNotification(message) {
  if (notificationElement) {
    document.body.removeChild(notificationElement);
  }

  notificationElement = document.createElement('div');
  notificationElement.textContent = message;
  notificationElement.id = 'moyu-notification';
  document.body.appendChild(notificationElement);

  console.log('Notification shown:', message);

  setTimeout(() => {
    if (notificationElement && notificationElement.parentNode) {
      notificationElement.parentNode.removeChild(notificationElement);
      notificationElement = null;
      console.log('Notification removed');
    }
  }, 5000);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Message received:', request);
  if (request.action === 'showNotification') {
    showNotification(request.message);
  }
});

console.log('Content script loaded');