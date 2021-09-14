const url = window.location.href;
const domain = window.location.hostname;
const result = {};

// shortening_service
try {
  const patt3 = /bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|ity\.im|q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net/gi
  if (patt3.test(domain)) {
    result['Short service']= "1";
  } else {
    result['Short service'] = "-1";
  }
} catch  {
  result['Short service'] = "0";
}

// domain contain "-"
try {
  const patt = /-/;
  if (patt.test(domain)) {
    result['(-) Prefix/Suffix in domain'] = '1';
  } else {
    result['(-) Prefix/Suffix in domain'] = '-1';
  }
} catch  {
  result['(-) Prefix/Suffix in domain'] = '0';
}

// domain contain suspicious keyword
wordlist = ["weebly", "chuyentien", "chuyen-tien", "vay", "quatang", "qua-tang", "vay-tin-dung", "vaytindung",
 "giaithuong", "giai-thuong", "tang", "guiqua", "gui-qua", "trao-qua", "traoqua", "trao-thuong", "traothuong", 
 "mo-tai-khoan", "motaikhoan", "mo-the", "mothe", "tinchap", "tin-chap", "thechap", "the-chap", "trung-thuong", 
 "trungthuong","nhanthuong"];

function handlerContain(text) {
  check = false;
  for ( var i in text) {
    let re = RegExp(text[i])
    if (re.test(domain)) {
      check = true;
    }
  }
  return check;
}

try {
  check = handlerContain(wordlist)
  if (check == true) result['D contain keyword'] = '1';
  else result['D contain keyword'] = '-1';

} catch {
  result['D contain keyword'] = '0';
}

// domain contain digit character
try {
  var onlyNum = /^\d+$/;
  countNum = 0;
  for (let i = 0; i < domain.length; i++) {
    if (onlyNum.test(domain[i]) == true) {
      countNum++;
    }
  }
  percentage = (countNum/domain.length) * 100
  if (percentage < 10) result['D contain digit'] = '-1';
  else if (percentage > 10 && percentage < 30) result['D contain digit'] = '0';
  else result['D contain digit'] = '1';

} catch {
  result['D contain digit'] = '0';
}

// score for tld
trustTLD = ['.com','.co','.org','.us','.net','.blog','.io','.biz','.gov'];

function handlerEndText(text) {
  check = false;
  for ( var i in text) {
    let gov = RegExp('.gov.');
    let edu = RegExp('.edu.');
    if (domain.endsWith(text[i])||gov.test(domain)||edu.test(domain)) {
      check = true;
    }
  }
  return check;
}

try {
  check = handlerEndText(trustTLD)
  if (check == true) result['trustTLD'] = '-1';
  else result['trustTLD'] = '1';

} catch {
  result['trustTLD'] = '0';
}

// redirect using "//"
try {
  if (url.lastIndexOf('//') > 7) result['Redirecting using //'] = '1';
  else result['Redirecting using //'] = '-1';

} catch {
  result['Redirecting using //'] = '0';
}

// HTTPS
try {
  const patt = /https:\/\//;
  if (patt.test(url)) result['HTTPS'] = '-1';
  else result['HTTPS'] = '1';

} catch {
  result['HTTPS'] = '0';
}

// favicon
try {
  let favicon = undefined;
  const nodeList = document.getElementsByTagName('link');
  for (let i = 0; i < nodeList.length; i++) {
    if ((nodeList[i].getAttribute('rel') == 'icon') || (nodeList[i].getAttribute('rel') == 'shortcut icon')) {
      favicon = nodeList[i].getAttribute('href');
    }
  }
  if (!favicon) result['Favicon'] = '1';
  else {
    const patt = RegExp("favicon");
    if (patt.test(favicon)) result['Favicon'] = '-1';
    else result['Favicon'] = '1';
  }

} catch {
  result['Favicon'] = '0';
}

//missing title
try {
  const titletags = document.title;
  if(titletags == "") result['missing title']= "1";
  else result['missing title']= "-1";

} catch {
  result['missing title']= "0";
}

// server form handler
try {
  const forms = document.getElementsByTagName('form');
  result['SFH'] = '-1';
  const patt = RegExp(domain);
  for (let i = 0; i < forms.length; i++) {
    const action = forms[i].getAttribute('action');
    if (!action || action == '') {
      result['SFH'] = '1';
      break;
    }
    else if (action.startsWith("https://") && patt.test(action) || (action.charAt(0) == '/')) {
      result['SFH'] = '-1'
    }
  }

} catch {
  result['SFH'] = '0';
}

// using iframe
try {
  const iframes = document.getElementsByTagName('iframe');
  if (iframes.length == 0) result['iFrames'] = '1';
  else result['iFrames'] = '-1';

} catch {
  result['iFrames'] = '0';
}

// popup window
try {
  var scripts = document.getElementsByTagName("script");
  if(scripts.length==0) result["Popup"] = '0';
  for (var i = 0; i < scripts.length; ++i) {
    if (scripts[i].textContent.match("window.open")) {
        result["Popup"] = '1';
        break;
    } else {
        result["Popup"] = '-1';
        break;
    }
  }
} catch {
  result["Popup"] = '0';
}

// url of tag a
try {
  const aTags = document.getElementsByTagName('a');
  const patt = RegExp(domain);
  var phishCount = 0;
  var legitCount = 0;
  
  for (let i = 0; i < aTags.length; i++) {
    const hrefs = aTags[i].getAttribute('href');
    if (!hrefs) continue;
    if (patt.test(hrefs)) legitCount++;
    else if (hrefs.charAt(0) == '#' || (hrefs.charAt(0) == '/' && hrefs.charAt(1) != '/')) legitCount++;
    else phishCount++;
  }
  var totalCount = phishCount + legitCount;
  var outRequest = (phishCount / totalCount) * 100;

  if (outRequest < 31) result['Anchor'] = '-1';
  else if (outRequest >= 31 && outRequest <= 67) result['Anchor'] = '0';
  else result['Anchor'] = '1';

} catch {
  result['Anchor'] = '0';
}

// url of image
try {
  const imgTags = document.getElementsByTagName('img');
  var phishCount = 0;
  var legitCount = 0;
  
  for (let i = 0; i < imgTags.length; i++) {
    const src = imgTags[i].getAttribute('src');
    if (!src) continue;
    if (src.startsWith('https://')) legitCount++;
    else if (src.charAt(0) == '/' && src.charAt(1) != '/') legitCount++;
    else phishCount++;
  }

  var totalCount = phishCount + legitCount;
  var outRequest = (phishCount / totalCount) * 100;
  
  if (outRequest < 22) result['Request URL'] = '-1';
  else if (outRequest >= 22 && outRequest < 61) result['Request URL'] = '0';
  else result['Request URL'] = '1';

} catch {
  result['Request URL'] = '0';
}

// Links in script and link
try {
  const sTags = document.getElementsByTagName('script');
  const lTags = document.getElementsByTagName('link');

  var phishCount = 0;
  var legitCount = 0;

  for (let i = 0; i < sTags.length; i++) {
    const sTag = sTags[i].getAttribute('src');
    if (sTag != null) {
      if (sTag.startsWith('https://')) legitCount++;
      else if (sTag.charAt(0) == '/' && sTag.charAt(1) != '/') legitCount++;
      else phishCount++;
    }
  }
  
  for (let i = 0; i < lTags.length; i++) {
    const lTag = lTags[i].getAttribute('href');
    if (!lTag) continue;
    if (lTag.startsWith('https://')) legitCount++;
    else if (lTag.charAt(0) == '/' && lTag.charAt(1) != '/') legitCount++;
    else phishCount++;
  }

  var totalCount = phishCount + legitCount;
  var outRequest = (phishCount / totalCount) * 100;
  
  if (outRequest < 17) result['Script & Link'] = '-1';
  else if (outRequest >= 17 && outRequest <= 81) result['Script & Link'] = '0';
  else result['Script & Link'] = '1';

} catch {
  result['Script & Link'] = '0';
}

// frequent Domain Name Mismatch
try {
  var list_links_in_web = document.links;
  var dict = {};
  if (list_links_in_web.length > 0 ){  
    for(let i = 0 ;i < list_links_in_web.length ; i ++){    
      one_url = list_links_in_web[i].hostname;
      if (typeof dict[one_url] === "undefined" ) dict[one_url]= 1;
      else dict[one_url]= dict[one_url] +1;                
    }

    var items = Object.keys(dict).map(function(key) {
      return [key, dict[key]];
    });

    items.sort(function(first, second) {
      return second[1] - first[1];
    });

    var url_name = window.location.href; 
    var arr_domain_name = url_name.split("/");
    var domain_name = arr_domain_name[0] + "//" + arr_domain_name[2]

    if (domain_name.includes(items[0][0])) result['FDNM'] = '-1';
    else result['FDNM'] = '1';   
  }
  else result['FDNM'] = '-1';

} catch {
  result['FDNM'] = '0';
}

// contact mail
try{
  var search_in = document.body.innerHTML;
  string_context = search_in.toString();
  array_mails = string_context.match(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/gi);
  if (array_mails[array_mails.length - 1].split("@")[1] != domain.replace('www.', '')){
    result['checkmail'] = "1";
  } else {
    result['checkmail'] = '-1';
  }
} catch {
  result['checkmail'] = "0"  
}

// verify by bo cong thuong
try {
  result['bocongthuong'] = '0';
  var bct = document.querySelectorAll("a[href^='http://online.gov.vn/']");
  for (var i = 0, l = bct.length; i < l; i++) {
    if (!bct[i]) continue
    if(bct[i]) result['bocongthuong'] = "-1"
  }
} catch {
  result['bocongthuong'] = '0'
}

// verify by tin nhiem mang
try {
  result['tinnhiemmang'] = '0';
  var tnm = document.querySelectorAll("a[href^='https://tinnhiemmang.vn/']");
  for (var i = 0, l = tnm.length; i < l; i++) {
    if (!tnm[i]) continue;
    else result['tinnhiemmang'] = "-1"
  }
} catch{
  result['tinnhiemmang'] = '0';
}

chrome.runtime.onMessage.addListener((msg, sender, response) => {
  if ((msg.from === 'white') && (msg.subject === 'DOMInfo')) {
    var domInfo = {
      domain: domain,
    };
    response(domInfo);
  }
});

let data_request = {
  DomainName: domain,
  ShorteningService: parseInt(result['Short service']),
  DashCharacter: parseInt(result['(-) Prefix/Suffix in domain']),
  SensitiveWords: parseInt(result['D contain keyword']),
  PercentNumericChars: parseInt(result['D contain digit']),
  TrustTLD:  parseInt(result['trustTLD']),
  RedirectInURL:  parseInt(result['Redirecting using //']),
  HTTPS:  parseInt(result['HTTPS']),
  favicon:  parseInt(result['Favicon']),
  MissingTitle:  parseInt(result['missing title']),
  ServerFormHandler:  parseInt(result['SFH']),
  Iframe:  parseInt(result['iFrames']),
  PopupWindow:  parseInt(result["Popup"]),
  AnchorHref:  parseInt(result['Anchor']),
  ImageSrc:  parseInt(result['Request URL']),
  ScriptAndLink:  parseInt(result['Script & Link']),
  FrequentDomainNameMismatch:  parseInt(result['FDNM']),
  ContactMail:  parseInt(result['checkmail']),
  VerifyByMoitVn:  parseInt(result['bocongthuong']),
  VerifyByTnm:  parseInt(result['tinnhiemmang'])
}

async function send() {
  $.ajax({
    url: "https://api.dephish.tech/v1/predict",
    type:"POST",
    data:JSON.stringify(data_request),
    contentType:"application/json; charset=utf-8",
    dataType:"json",
    success: function(data){
      console.log("success");
      console.log(data)
      percen = parseInt(data["percent"]*100)
      chrome.runtime.onMessage.addListener((msg, sender, response) => {
        if ((msg.from === 'popup') && (msg.subject === 'DOMInfo')) {
          var domInfo = {
            domain: domain,
            percen: percen,
            check: String(data["result: "])
          };
          response(domInfo);
        }
      });
    }
  });
}

function blocking() {
  var ifm=document.createElement('iframe');
  var listTag = document.body.getElementsByTagName("*")
  for (let index = 0; index < listTag.length; index++) {
    const element = listTag[index];
    element.style.display = "none"
  }
  ifm.innerHTML=document.body.innerHTML+='<iframe id="finject"></iframe>'
  var iframe = document.getElementById("finject");
  iframe.src = chrome.extension.getURL("block.html");
  iframe.style.display = "block";
  iframe.style.border = "none";
  iframe.style.height = "100vh";
  iframe.style.width = "100vw"
  chrome.runtime.onMessage.addListener((msg, sender, response) => {
    if ((msg.from === 'block') && (msg.subject === 'DOMInfo')) {
      var domInfo = {
        domain: domain,
      };
      response(domInfo);
    }
  });
}

function receiveMessage(event){
  if (event.data=="removetheiframe"){
    var element = document.getElementById('finject');
    var listTag = document.body.getElementsByTagName("*")
    for (let index = 0; index < listTag.length; index++) {
      const element = listTag[index];
      element.style.display = "block";
    }
    element.parentNode.removeChild(element);
  }
}
window.addEventListener("message", receiveMessage, false);

//com black
var parts = location.hostname.split('.');
if (parts.length>3) {
  var subdomain = parts.shift();
  var upperleveldomain = parts.join('.');
  check_domain = upperleveldomain;
}
else if (domain.startsWith("www.")) check_domain = domain.split("www.")[1];
else check_domain = domain;

var port = chrome.extension.connect({
    name: "Com about black"
});
port.postMessage("black");
port.onMessage.addListener(function(msg) {
  var port = chrome.extension.connect({
    name: "black popup"
  });
  checkpoint = false;
  let alphabet = 'abcdefghijklmnopqrstuvwxyz'.split('');
  for (let char = 0; char < alphabet.length; char++) {
    var element = alphabet[char];
    if (check_domain.startsWith(element)) {
      if (msg[element].includes(check_domain)) {
        port.postMessage("true-black");
        blocking();
        checkpoint = true;
      }
    }
  }
  if (check_domain.match(/^\d/)){
    if (msg["num"].includes(check_domain)) {
      port.postMessage("true-black");
      blocking();
      checkpoint = true;
    }
  }
  if (checkpoint == false) {
    //com white
    var port = chrome.extension.connect({
      name: "Com about white"
    });
    port.postMessage("white");
    port.onMessage.addListener(function(msg) {
      var port = chrome.extension.connect({
        name: "white popup"
      });
      let alphabet = 'abcdefghijklmnopqrstuvwxyz'.split('');
      for (let char = 0; char < alphabet.length; char++) {
        var element = alphabet[char];
        if (check_domain.startsWith(element)) {
          if (msg[element].includes(check_domain)) {port.postMessage("true-white");}
          else {port.postMessage("predict");send();}
        }
      }
      if (check_domain.match(/^\d/)){
        if (msg["num"].includes(check_domain)) {port.postMessage("true-white");}
        else {port.postMessage("predict");send();}
      }
    });
  }
});


chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.report != undefined)
      sendReport(request.report)
  }
);

async function sendReport(datas) {
  $.ajax({
    url: "https://api.dephish.tech/v1/addVerify",
    type:"POST",
    data:JSON.stringify(datas),
    contentType:"application/json; charset=utf-8",
    dataType:"json",
    success: function(data){
      console.log("success");
      console.log(data);
    }
  });
}