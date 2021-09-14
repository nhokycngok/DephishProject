const setDOMInfo = info => {
  document.getElementById('domain').textContent = info.domain;
  document.getElementById('percen').textContent = String(info.percen)+"%";

  if(info.check=="-1") {
    document.getElementById('color').classList.add("green");
    document.getElementById('percen').style.color = "green";
    document.getElementById('confirm').textContent = "Theo dự đoán của học máy,";
    document.getElementById('confirm2').textContent = "website này có thể AN TOÀN";
    document.getElementById('confirm').style.color = "#73B14E";
    document.getElementById('confirm2').style.color = "#73B14E";
  } else {
    document.getElementById('color').classList.add("red");
    document.getElementById('percen').style.color = "red"
    document.getElementById('confirm').textContent = "Theo dự đoán của học máy,";
    document.getElementById('confirm2').textContent = "website này có thể NGUY HIỂM";
    document.getElementById('confirm').style.color = "#E94033";
    document.getElementById('confirm2').style.color = "#E94033";
  }
  var circle = "p"+info.percen;
  document.getElementById('color').classList.add(circle)
};

window.addEventListener('DOMContentLoaded', () => {
  chrome.tabs.query({
    active: true,
    currentWindow: true
  }, tabs => {
    chrome.tabs.sendMessage(tabs[0].id,{from: 'popup', subject: 'DOMInfo'},setDOMInfo);
  });
  var link = document.getElementById('report');
  link.addEventListener('click', function() {
    report();
  });
});

function showFeat() {
  var target = document.getElementById("txtArea");
  if (target.style.display ==="none") {
    target.style.display = "block";
  }
  else target.style.display = "none";
}

function report() {
  var target = document.getElementById("report");
  var target2 = document.getElementById("sendStatus");
  var target3 = document.getElementById("guide");
  if (target.style.display = "block") {
    target2.style.display = "block";
    target.style.display = "none";
    target3.style.display = "none";
    var color = document.getElementById('percen').style.color;
    if (color == "green") typeCheck = "black";
    else typeCheck = "white";
    var info = document.getElementById('domain').textContent;
    datas = {
      "domain": info,
      "type": typeCheck,
    }
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {report:datas});
    });
  }
}