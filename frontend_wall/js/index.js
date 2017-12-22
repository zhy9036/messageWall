$(document).ready(function() {
	
	var baseURL = "http://127.0.0.1:8000/";
	renderTopbar();
	renderBottombar();
	
	function validateEmail(email){  
		if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)){  
			return true;  
		}   
		return false;  
	} 
	$("#register").click(function() {
		var name = $("#username").val();
		var email = $("#email").val();
		var password = $("#password").val();
		var cpassword = $("#cpassword").val();
		if (name == '' || email == '' || password == '' || cpassword == '') {
			alert("Please fill all fields");
		} else if (!validateEmail(email)){
			alert("email format incorrect");
		} else if ((password.length) < 8) {
			alert("Password should atleast 8 character in length");
		} else if (!(password).match(cpassword)) {
			alert("Your passwords don't match. Try again?");
		} else {
			$.ajax({
				url: baseURL + "register",
				type: "POST",
				dataType: "json",
				data: {username: name,
					   email: email,
					   password: password,
					
					},
				success: function(data){
					if(data.status == 200){
						alert('User created and you can know log in!')
						location.reload();
					}else{
						alert('username:' +  name + ' already taken please pick another one')
					}
				}
				
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
			  url: baseURL + "login",
			  crossDomain: true,
			  type: "POST",
			  dataType:'json',
			  data: {username: name,
					 password: password},
			  success: function(data){

					if(data.status == 401){
						alert("Password or Username is incorrect!");
					}else{
						var cookievalue = data.username + ":" + data.user_id;
						setCookie('session', cookievalue, 1);
						location.reload();
					}
			  },
			  complete: function(data){
				  //location.reload();
			  }
			});
		}
	});
	
	$("#logout").click(function() {
		var value = getCookie("session").split(":");
		var name = value[0];
		var user_id = value[1];
		$.ajax({
		  url: baseURL + "logout",
		  crossDomain: true,
		  type: "POST",
		  dataType:'json',
		  data: {username: name,
				 user_id: user_id},
		  success: function(data){
				deleteCookie("session");
				alert(name + " logged out!")
				location.reload();
		  },
		  complete: function(data){
			  //location.reload();
		  }
		});
	});
	
	
    $(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        });
    });
    
    
    function renderTopbar(){
		var session_value = getCookie("session");
		div = $("<div>").addClass("top");
		ul = $("<ul>").addClass("topbar");
		li = $("<li>").addClass("right");
		li2 = $("<li>").addClass("topbar");
		
		if(session_value != null && session_value != ""){ // user logged in
			var username = session_value.split(':')[0];
			li.append($("<a>").attr("id", "logout").html("Log out"));
			li2.append($("<a>").html("Hello " + username));
			ul.append(li);
			ul.append(li2);
		}else{ // not logged in yet
			li.append($("<a>").attr("onclick", "document.getElementById('id02').style.display='block'").html("Register"));
			li1 = $("<li>").addClass("right").append($("<a>").
				attr("onclick", "document.getElementById('id01').style.display='block'").html("Login"));
			li2.append($("<a>").html("Hello Guest"));
			ul.append(li);
			ul.append(li1)
			ul.append(li2);
		}
		$("body").append(div.append(ul));
		
	}


	function renderBottombar(){
		var session_value = getCookie("session");
		ul = $("<ul>").addClass("bottombar");
		li = $("<li>").addClass("bottombar");
		li2 = $("<li>").addClass("right");
		li2.append($("<a>").addClass("active").attr("id", "send").html("Send"));
		if(session_value != null && session_value != ""){ // user logged in
			li.append($("<input>").prop('disabled', false).addClass("bottombar").attr({"placeholder": "Type message here", "id":"message"}));

		}else{ // not logged in yet
			li.append($("<input>").prop('disabled', true).addClass("bottombar").attr({"placeholder": "Log in to send message", "id":"message"}));

		}
		ul.append(li);
		ul.append(li2);
		$("body").append(ul);
		
	}

	//need to check browser first
	//chrome won't accept local cookie with path
	//if chrome use sessionStorage instead
	function setCookie(cname,cvalue,exdays) {
		var d = new Date();
		d.setTime(d.getTime() + (exdays*24*60*60*1000));
		var expires = "expires=" + d.toGMTString();
		
		if(isChrome()){
			sessionStorage.setItem(cname, cvalue);
		}else{
			document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
		}
	}

	function getCookie(cname) {
		if(isChrome()){
			return sessionStorage.getItem(cname);
		}
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
	
	function deleteCookie(cname) {
		sessionStorage.removeItem("session");
	}
	function isChrome(){
		return navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
	}
});
