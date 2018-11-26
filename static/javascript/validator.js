function validate_registration() {
	var Fname = document.forms["registration"]["FnameField"].value;
	if (!Fname.match("^[a-zA-z ]{2,50}$")){
		alert("Name cannot start or end with spaces, at least two letters.");
		return false;
	}

	var Lname = document.forms["registration"]["LnameField"].value;
	if (!Lname.match("^[a-zA-z ]{2,50}$")){
		alert("Last name cannot start or end with spaces, at least two letters.");
		return false;
	}
	var age = document.forms["registration"]["ageField"].value;
	if (!age.match("[0-9]{0,2}")){
		alert("Age are only numbers.");
		return false;
	}

	var address1 = document.forms["registration"]["address1Field"].value;
	if (!address1.match("^[a-zA-Z0-9 ]{2,50}$")){
		alert("Address (1) cannot contain special characters.");
		return false;
	};

	var address2 = document.forms["registration"]["address2Field"].value;
	if (!address2.match("^[a-zA-Z0-9 ]{0,50}$")){
		alert("Address (2) cannot contain special characters.");
		return false;
	};

	var city = document.forms["registration"]["cityField"].value;
	if (!city.match("^[a-zA-z ]{2,50}$")){
		alert("City cannot start or end with spaces, at least two letters.");
		return false;
	}
	var state = document.forms["registration"]["stateField"].value;
	if (!state.match("^[a-zA-z ]{0,50}$")){
		alert("State cannot start or end with spaces.");
		return false;
	}

	var country = document.forms["registration"]["countryField"].value;
	if (!country.match("^[a-zA-z ]{2,50}$")){
		alert("Country cannot start or end with spaces, at least two letters.");
		return false;
	}

	var region = document.forms["registration"]["regionField"].value;
	if (!region.match("^[a-zA-z ]{0,50}$")){
		alert("Region cannot start or end with spaces, at least two letters, maximum six.");
		return false;
	}

	var zip = document.forms["registration"]["zipField"].value;
	if (!zip.match("[0-9]+{5,9}")){
		alert("Zip are only numbers, at least five, maximum nine.");
		return false;
	}


	var username = document.forms["registration"]["usernameField"].value;
	if (!username.match("^[a-zA-Z0-9_]{3,20}$")){
		alert("Username must be at least 3 characters long with no special characters(except _ ).");
		return false;
	};

	var email = document.forms["registration"]["emailField"].value;
	if (!email.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$")){
		alert("Email must match pattern 'you@example.com'");
		return false;
	}

	var password = document.forms["registration"]["passwordField"].value;
	if (!password.match("[a-zA-Z0-9@!#$%&*]{8,}")){
		alert("Password must be at least 8 characters.");
		return false;
	}

	var card = document.forms["registration"]["creditcardField"].value;
	if (!card.match("[0-9]{16}")){
		alert("Credit Card must contain 16 digits.");
		return false;
	}
	var cardtype = document.forms["registration"]["creditcardtypeField"].value;
	if (!cardtype.match("^[a-zA-z ]{2,6}$")){
		alert("Card type cannot start or end with spaces, at least two letters.");
		return false;
	}
	var exMonth=document.getElementById("exMonth");
	var exYear=document.getElementById("exYear");
	var today = new Date();
	var someday = new Date();
	someday.setFullYear(exYear, exMonth, 1);
	if (someday < today) {
   alert("The expiry date is before today's date. Please select a valid expiry date");
   return false;
	}


	var phone = document.forms["registration"]["phoneField"].value;
	if (!phone.match("[0-9]{0,12}")){
		alert("Number is only digits, at leats nine, maximun twelve.");
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

$(document).ready(function () {
	path = window.location.href;
	base = path.split("wsgi");
	path = base[0] + 'wsgi/hits'
  	setInterval (function() {
  		$.ajax({
		  	type: "POST",
		  	url: path
		}).done(function( text ) {
       		$('#hits').html(text);
		});
  	}, 3000);
});

$(document).ready(function(){
	$('.principal').on('click', function() {
		$('.details').toggle();
	});
});

var seq=0;
function namebuy(){

	seq=seq+1;
    document.write("Buy " + seq);
}


function error_login(){

	alert("Username or password incorrect, try again.\n\tMaybe are you not registered?");
}

function error_buy(){

	alert("Sorry, you can't buy all this movies because you don't have enough money.\n\tTo change your money, go to Purchase History page");
}

function ok_buy(){

	alert("Your buy is done, check your purchase history.");
}

function must_login(){
	alert("You must be logged in to buy movies.");
}
