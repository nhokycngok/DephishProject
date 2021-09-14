
    function send_verify(dm,list){

        if (list == 'black'){
            var type = document.getElementById("type"+dm).value;
            var level = document.getElementById("level"+dm).value;
            link = "/add_to_list?domain=" + String(dm) + "&list=" + String(list) + "&type=" + String(type) + "&level" + String(level);
        }
        else if (list == 'white'){
            link = "/add_to_list?domain=" + String(dm) + "&list=" + String(list);
        }
        window.location.href = link;
    }
    function send_del(domain, type){
        window.location.href = "/del_from_list_verify?domain="+ String(domain)+ "&type=" + String(type);
    }
