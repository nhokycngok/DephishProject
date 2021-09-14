const setDOMInfo = info => {
    document.getElementById('domain').textContent = info.domain
    +" nằm trong danh sách các website NGUY HIỂM theo báo cáo của cộng động và nguồn tin cậy.";
    document.getElementById('btn-domain').textContent ="Tôi muốn truy cập "+ info.domain;
};

window.addEventListener('DOMContentLoaded', () => {
  chrome.tabs.query({
    active: true,
    currentWindow: true
  }, tabs => {
    chrome.tabs.sendMessage(
        tabs[0].id,
        {from: 'block', subject: 'DOMInfo'},
        setDOMInfo);
  });
});

window.addEventListener('DOMContentLoaded', () => {
  var link = document.getElementById('hideFrame');
  link.addEventListener('click', function() {
    hideFrame();
  });
});
function hideFrame() {
  parent.window.postMessage("removetheiframe", "*");
}