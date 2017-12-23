$(document).ready(function() {
	
	var baseURL = "http://127.0.0.1:8000/";
	renderTopbar();
	renderBottombar();
	refreshWall();
	setInterval(refreshWall, 15*1000); //refreash wall every 15 seconds
	
	
	function renderMessage(item, index){
		div = $('<div>');
		timeSpan = $('<span>');
		if (index % 2 == 0){
			div.addClass("container message");
			timeSpan.addClass("time-right");
		}else{
			div.addClass("container message darker");
			timeSpan.addClass("time-left");
		}
		div.append($('<p>').html(item.content));
		var ts = new Date(item.create_date);
		div.append(timeSpan.html(item.username + " " + ts.toLocaleString()));
		$("#message_div").append(div);
	}
	
	function refreshWall(){
		$.ajax({
		  url: baseURL + "api/messages/",
		  type: "GET",
		  dataType:'json',
		  success: function(data){
			if($("#message_div").length){
				$("#message_div").empty();
			}else{
				$("body").append($("<div>").attr("id", "message_div"));
			}
			data.forEach(renderMessage);
		  },
		  complete: function(data){
			  //location.reload();
		  }
		});
	}
	
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
			//alert("Please fill all fields");
			showErrorMessage("Please fill all fields");
		} else if (!validateEmail(email)){
			//alert("email format incorrect");
			showErrorMessage("email format incorrect");
		} else if ((password.length) < 8) {
			//alert("Password should atleast 8 character in length");
			showErrorMessage("Password should atleast 8 character in length");
		} else if (!(password).match(cpassword)) {
			//alert("Your passwords don't match. Try again?");
			showErrorMessage("Your passwords don't match. Try again?");
		} else {
			$.ajax({
				url: baseURL + "/register",
				type: "POST",
				dataType: "json",
				data: {username: name,
					   email: email,
					   password: password,
					
					},
				success: function(data){
					if(data.status == 200){
						//alert('User created and you can know log in!')
						showSuccessMessage('User created and you can know log in!');
						document.getElementById('id02').style.display='none';
					}else{
						//alert('username:' +  name + ' already taken please pick another one')
						showErrorMessage('username:' +  name + ' already taken please pick another one');
					}
				}
				
			});	
		}
	});

	$("#login").click(function() {
		var name = $("#username_login").val();
		var password = $("#password_login").val();
		if (name == '' ||password == '') {
			//alert("Please fill all fields");
			showErrorMessage("Please fill all fields");
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
						//alert("Password or Username is incorrect!");
						showErrorMessage("Password or Username is incorrect!");
					}else{
						var cookievalue = data.username + ":" + data.user_id;
						setCookie('session', cookievalue, 1);
						document.getElementById('id01').style.display='none';
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
				//alert(name + " logged out!")
				showSuccessMessage(name + " logged out!");
				renderTopbar();
				renderBottombar();
				//location.reload();
		  },
		  complete: function(data){
			  //location.reload();
		  }
		});
	});
	
	$("#send").click(function() {
		var session = getCookie("session");
		var session_value = session.split(":");
		var name = session_value[0];
		var user_id = session_value[1];
		var content = $("#message_input").val();
		if(session_value != null && session_value != "" &&
			content.trim() != ""){ // user logged in and input not empty
			$.ajax({
			  url: baseURL + "api/messages/",
			  crossDomain: true,
			  type: "POST",
			  dataType:'json',
			  data: {content: content,
					 username: name,
					 user_id: user_id},
			  success: function(data){
					refreshWall();
					$("#message_input").val("");
			  },
			  complete: function(data){
				  //location.reload();
			  }
			});
		}
	});
	
	
	function showErrorMessage(message){
			BootstrapDialog.show({
                type: BootstrapDialog.TYPE_DANGER,
                title: 'Error',
                message: message,
                buttons: [{
					label: 'Close',
					action: function(dialogItself){
						dialogItself.close();
					}
                }]
            });
	}
	
	function showSuccessMessage(message){
		BootstrapDialog.show({
			type: BootstrapDialog.TYPE_SUCCESS,
			title: 'Success',
			message: message,
			buttons: [{
				label: 'Close',
				action: function(dialogItself){
					dialogItself.close();
				}
			}]
		});
	}
	
	function genCSRFTOKEN(){
		var buf = new Uint8Array(1);
		window.crypto.getRandomValues(buf); 
		return buf[0];
	}
	
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	
    $(function () {
        $.ajaxSetup({
			headers:{"X-CSRFToken": getCookie('csrftoken')}
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
			li.append($("<input>").prop('disabled', false).addClass("bottombar").attr({"placeholder": "Type message here", "id":"message_input"}));

		}else{ // not logged in yet
			li.append($("<input>").prop('disabled', true).addClass("bottombar").attr({"placeholder": "Log in to send message", "id":"message_input"}));

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
    	return null;
	}
	
	function deleteCookie(cname) {
		sessionStorage.removeItem("session");
	}
	function isChrome(){
		return navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
	}
});
