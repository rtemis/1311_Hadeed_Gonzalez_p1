function validate_registration() {
	var name = document.forms["registration"]["nameField"].value;
	if (!name.match("^[a-zA-z ]{2,}$")){
		alert("Name cannot start or end with spaces.");
		return false;
	}

	var address = document.forms["registration"]["addressField"].value;
	if (!address.match("^[a-zA-Z0-9 ]{2,}$")){
		alert("Address cannot contain special characters.");
		return false;
	};

	var username = document.forms["registration"]["usernameField"].value;
	if (!username.match("^[a-zA-Z0-9_]{3,20}$")){
		alert("Username must be at least 3 characters long with no special characters.");
		return false;
	};

	var email = document.forms["registration"]["emailField"].value;
	if (!email.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$")){
		alert("Email must match pattern 'you@example.com'");
		return false;
	}

	var password = document.forms["registration"]["passwordField"].value;
	if (!password.match("[a-zA-Z0-9@!#$%&*]{6,}")){
		alert("Password must be at least 6 characters.");
		return false;
	}

	var card = document.forms["registration"]["creditcardField"].value;
	if (!card.match("[0-9]{16}")){
		alert("Credit Card must contain 16 digits.");
		return false;
	}

}

function validate_psw() {
	var meter = document.getElementById("strengthbar");
	var pass = document.getElementById("passwordField");

	pass.onkeydown = function (){
		var strength = 0;
	  	
	  	if(pass.value.match("[a-z]")) {
	  		strength++; 
	    }
		if(pass.value.match("[A-Z]")) {
			strength++;
		}
		if(pass.value.match("[0-9]")) {
			strength++;
		}
		if(pass.value.match("[!@#$%&*]")) {
			strength++;
		}

		meter.value = strength;
	}
}


/*function validate_login(){
	var user = document.forms["login"]["username"].value;
	var password = document.forms["login"]["password"].value;
	var path_string = document.forms["login"]["path"].value;

	if (fs.lstatSync(path_string+'/'+username).isDirectory()) {
		alert("User not found.");
		return false;
	}

	var client = new XMLHttpRequest();
	client.open('GET', path_string+'/'+username+'/'+'datos.dat');
	client.onload = (function(){

	var txt = client.responseText;

	var arr = [];
	var lines = txt.split('\n');
	client.send(null);
}
*/
/*
function remove_from_cart(){

	for(j=0; j < lines.length; j++) {
	  	arr[j] = lines[j].split(" : ");
	  	
	  	if (password == arr[2]) {}
	}
}
*/

$(document).ready(function () {
  	setInterval (function() {
	  	var text = Math.floor((Math.random() * 1000) + 1);
       	$('#hits').html(text);  	
  	}, 3000);
});

function remove_from_cart(){

}

