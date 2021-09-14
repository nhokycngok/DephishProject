var url_base = window.location.href;
if (url_base.includes("/home")){
    document.getElementById("home_taskbar").style.fontWeight = "bold";
}
if (url_base.includes("/black")){
    document.getElementById("home_blacklist").style.fontWeight = "bold";
}
if (url_base.includes("/white")){
    document.getElementById("home_whitelist").style.fontWeight = "bold";
}
if (url_base.includes("/vdomain_white") ){
    document.getElementById("home_report").style.fontWeight = "bold";
    document.getElementById("home_report_white").style.fontWeight = "bold";
}
if (url_base.includes("/vdomain_black") ){
    document.getElementById("home_report").style.fontWeight = "bold";
    document.getElementById("home_report_black").style.fontWeight = "bold";
}
if (url_base.includes("/all_member")){
    document.getElementById("home_all_member").style.fontWeight = "bold";
}

