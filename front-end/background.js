function getData(url) {
    return fetch(url).then((response) => response.json());
}

//read white from server
var dict_whiteDomains = {
    'a': [],'b': [],'c': [],'d': [],'e': [],'f': [],'g': [],'h': [],'i': [],'j': [],'k': [],'l': [],'m': [],
    'n': [],'o': [],'p': [],'q': [],'r': [],'s': [],'t': [],'u': [],'v': [],'w': [],'x': [],'y': [],'z': [],
    'num': []
};
getData("https://api.dephish.tech/v1/whitelist").then((res) =>
    {
        for(let i=0;i<res['whitelist'].length;i++){
            let domain = res['whitelist'][i]["domain"]
            let alphabet = 'abcdefghijklmnopqrstuvwxyz'.split('');
            for (let char = 0; char < alphabet.length; char++) {
                const element = alphabet[char];
                if (domain.startsWith(element)) dict_whiteDomains[element].push(domain);
                else if(domain.match(/^\d/)) dict_whiteDomains["num"].push(domain);
            }
        }
    }
);

// read black from server
var dict_blackDomains = {
    'a': [],'b': [],'c': [],'d': [],'e': [],'f': [],'g': [],'h': [],'i': [],'j': [],'k': [],'l': [],'m': [],
    'n': [],'o': [],'p': [],'q': [],'r': [],'s': [],'t': [],'u': [],'v': [],'w': [],'x': [],'y': [],'z': [],
    'num': []
};
getData("https://api.dephish.tech/v1/blacklist").then((res) =>
    {   
        for(let i=0;i<res['blacklist'].length;i++){
            let domain = res['blacklist'][i]["domain"]
            let alphabet = 'abcdefghijklmnopqrstuvwxyz'.split('');
            for (let char = 0; char < alphabet.length; char++) {
                const element = alphabet[char];
                if (domain.startsWith(element)) dict_blackDomains[element].push(domain);
                else if(domain.match(/^\d/)) dict_blackDomains["num"].push(domain);
            }
        }
    }
);

chrome.extension.onConnect.addListener(function(port) {
    port.onMessage.addListener(function(msg) {
        console.log(msg)
        if (msg === "white") port.postMessage(dict_whiteDomains);
        else if (msg === "black") port.postMessage(dict_blackDomains);
        else if (msg === "true-white") chrome.browserAction.setPopup({ popup: "white.html"});
        else if (msg === "true-black") chrome.browserAction.setPopup({ popup: "black.html"});
        else chrome.browserAction.setPopup({ popup: "popup.html"});
    });
})