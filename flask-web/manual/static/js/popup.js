function openForm(list){
        check_ = list;
        if (check_ == "black") {
            document.getElementById("myForm2").style.display = "none";
            document.getElementById("update_white").style.display = "none";
            document.getElementById("update_black").style.display = "none";
            document.getElementById("search_black").style.display = "block";
            if (document.getElementById("myForm1").style.display === "block"){
                document.getElementById("myForm1").style.display = "none";
            }
            else{
                document.getElementById("myForm1").style.display = "block";
            }
        }
        else if (check_ == "white"){
            document.getElementById("search_white").style.display = "block";
            document.getElementById("myForm1").style.display ="none";
            document.getElementById("update_white").style.display = "none";
            document.getElementById("update_black").style.display = "none";
            if (document.getElementById("myForm2").style.display === "block"){
                document.getElementById("myForm2").style.display = "none";
            }
            else{
                document.getElementById("myForm2").style.display = "block";
            }
        }
    }
function update(old_domain, old_type, old_level, list){
    if (list== 'black'){
        document.getElementById("update_white").style.display = "none";
        document.getElementById("myForm2").style.display = "none";
        document.getElementById("myForm1").style.display ="none";
        document.getElementById("search_black").style.display = "block";
        if (document.getElementById("update_black").style.display === "none"){
            document.getElementById("old_domain").value = old_domain;
            document.getElementById("up_domain").value = old_domain;
            document.getElementById("up_type").value = old_type;
            document.getElementById("up_level").value = old_level;
            document.getElementById("up_domain").focus();
            document.getElementById("update_black").style.display = "block";
        }
        else{
            if (document.getElementById("up_domain").value == old_domain){
                document.getElementById("update_black").style.display = "none";    
            }
            else{
                document.getElementById("old_domain").value = old_domain;
                document.getElementById("up_domain").value = old_domain;
                document.getElementById("up_type").value = old_type;
                document.getElementById("up_level").value = old_level;
                document.getElementById("up_domain").focus();
                document.getElementById("update_black").style.display = "block";
            }
            
        }
    }
    else if (list== 'white'){
        document.getElementById("search_white").style.display = "block";
        document.getElementById("update_black").style.display = "none";
        document.getElementById("myForm2").style.display = "none";
        document.getElementById("myForm1").style.display ="none";
        if (document.getElementById("update_white").style.display == "none"){
            document.getElementById("old_domain_").value = old_domain;
            document.getElementById("up_domain_").value = old_domain;
            document.getElementById("up_domain_").focus();
            document.getElementById("update_white").style.display = "block"
        }
        else{
            if (document.getElementById("up_domain").value == old_domain ){
                document.getElementById("update_white").style.display = "none";    
            }
            else{
                document.getElementById("old_domain_").value = old_domain;
                document.getElementById("up_domain_").value = old_domain;
                document.getElementById("up_domain_").focus();
                document.getElementById("update_white").style.display = "block"
            }
            
        }
    }
}
