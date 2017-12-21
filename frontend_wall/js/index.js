$(document).ready(function() {
	$("#register").click(function() {
		var name = $("#name").val();
		var email = $("#email").val();
		var password = $("#password").val();
		var cpassword = $("#cpassword").val();
		if (name == '' || email == '' || password == '' || cpassword == '') {
			alert("Please fill all fields");
		} else if ((password.length) < 8) {
			alert("Password should atleast 8 character in length");
		} else if (!(password).match(cpassword)) {
			alert("Your passwords don't match. Try again?");
		} else {
			$.post("register.php", {
				usename: name,
				email: email,
				password: password
			}, function(data) {
				alert(data);
			});		
		}
	});

	$("#login").click(function() {
		var name = $("#username_login").val();
		var password = $("#password_login").val();
		if (name == '' ||password == '') {
			alert("Please fill all fields");
		} else {
			$.ajax({
			  url: "http://127.0.0.1:8000/login",
			  crossDomain: true,
			  type: "POST",
			  dataType:'json',
			  data: {username: name,
					 password: password},
			  success: function(data){
				  alert(data.status);
			  }
			});
		}
	});
    $(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        });
    });

	function setCookie(cname, cvalue, exdays) {
		var d = new Date();
		d.setTime(d.getTime() + exdays*(24*60*60*1000));
		var expires = "expires="+d.toUTCString();
		document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
	
	}


	function getCookie(cname) {
		var name = cname + "=";
		var decodedCookie = decodeURIComponent(document.cookie);
		var ca = decodedCookie.split(';');
		for(var i = 0; i <ca.length; i++) {
		    var c = ca[i];
		    while (c.charAt(0) == ' ') {
		        c = c.substring(1);
		    }
		    if (c.indexOf(name) == 0) {
		        return c.substring(name.length, c.length);
		    }
		}
    	return "";
	}
});
