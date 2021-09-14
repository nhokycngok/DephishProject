function open_from_member(){
    if (document.getElementById("myForm").style.display === "block"){
        document.getElementById("myForm").style.display = "none";
        document.getElementById("search_member").style.display = "block";
    }
    else{
        document.getElementById("myForm").style.display = "block";
        document.getElementById("search_member").style.display = "block";
    }

}
