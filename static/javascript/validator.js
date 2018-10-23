function validate_usr() {
	var user = document.getElementByName('username');
	if (user.value.length <= 2 || user.value.includes(' ')) {
		alert("Invalid name. Username must be more than 3 characters, no spaces.");
		return false;
	}
}

function validate_psw() {
	var pass = document.getElementByName('password');
	var meter = document.getElementById('strengthbar');

	pass.onfocus = function() {
	  document.getElementById('strengthbar').style.display = "block";
	}

	pass.onblur = function() {
	  document.getElementById('strengthbar').style.display = "none";
	}

	pass.onkeyup = function() {
		var strength = 0;

	  	if(pass.value.match('[a-z]')) {
	  		strength++; 
	    }

		if(pass.value.match('[A-Z]')) {
			strength++;
		}

		if(pass.value.match('[0-9]')) {
			strength++;
		}

		if(pass.value.length >= 6) {
			strength++;
		}

		var result = zxcvbn(pass.value);

		meter.value = result.score;
	}
	
	if (!pass.value.match("(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}")) {
		alert("Invalid password. Must contain at least 6 characters.");
		return false;
	}
}

function validate_email() {
	var email = document.getElementByName('email');
	if (!email.value.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$")) {
		alert("Invalid email. Must be of the form 'youexample@email.com'.");
		return false;
	}
}

function validate_name() {
	var name = document.getElementByName('name');
	if (name.value.length <= 1) {
		alert("Invalid name.");
		return false;
	}
}

function validate_creditcard() {

}

function mantain_search() {

}
