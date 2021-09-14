$("form[name=change_pass]").submit(function(e){
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
//    if ($('input[name="new_password"]').val() == $('input[name="new_password_"]').val()){
        $.ajax({
          url: "/user/change_pass",
          type: "POST",
          data: data,
          dataType: "json",
          success: function(resp){
            window.location.href = "/";
          },
          error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
          }
        });

        e.preventDefault();
//    }
//    else{
//        $error.text("Passwords are not the same").removeClass("error--hidden");
//    }

  });