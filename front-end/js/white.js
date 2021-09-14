const setDOMInfo = info => {
    document.getElementById('domain').textContent = info.domain;
};

window.addEventListener('DOMContentLoaded', () => {
    chrome.tabs.query({
      active: true,
      currentWindow: true
    }, tabs => {
      chrome.tabs.sendMessage(
          tabs[0].id,
          {from: 'white', subject: 'DOMInfo'},
          setDOMInfo);
    });
});