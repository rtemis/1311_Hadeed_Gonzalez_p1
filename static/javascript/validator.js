function validate_usr(username) {
	
	return (username.length >= 2 && username == username.trim());
		
}

function validate_psw() {
	var meter = document.getElementById('strengthbar');
	var pass = document.getElementsByName('password');

	var strength = 0;

  	if(pass.value.match('[a-z]+')) {
  		strength++; 
    }
	if(pass.value.match('[A-Z]+')) {
		strength++;
	}
	if(pass.value.match('[0-9]+')) {
		strength++;
	}
	if(pass.value.length >= 12) {
		strength++;
	}
	meter.value = strength;
	
	pass.onblur = function(){
		if (!pass.value.match("(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}")) {
			alert("Invalid password. Must contain at least 6 characters.");
			return false;
		}
	}
}

function validate_email(email) {
	
	return (email.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$"));
}

function validate_name(name) {
	return (name.length >= 2 && name == name.trim() && name.match("[a-zA-Z]+"));
}

function validate_creditcard(card) {
	return(card.match([0-9]+{16}));
	
}

function mantain_search(select) {
	document.getElementsByName(select).selected = true;

}

function validate_register(formulario){
	var retorno = true;
	var msj = "";
	
	if(!validate_usr(formulario['username'].value)) 
	{
		formulario["username"].focus();
		retorno = false;
		msj += "Invalid username. Username must be more than 2 characters.";
	}
	
	if(! validate_email(formulario['email'].value)) 
	{
		if(retorno) 
		{
			formulario["email"].focus();
			retorno = false;
		}
		else msj += "\n";
		msj += "Invalid email. Must be of the form 'youexample@email.com'.";
	}
	
	if(! validate_name(formulario["name"].value)) 
	{
		if(retorno) 
		{
			formulario["name"].focus();
			retorno = false;
		}
		else msj += "\n";
		msj += "Invalid name. Name must be more than 2 characters, not numbers.";
	}

	if(! validate_creditcard(formulario["creditcard"].value)) 
	{
		if(retorno) 
		{
			formulario["creditcard"].focus();
			retorno = false;
		}
		else msj += "\n";
		msj += "Invalid credit card. Card must be 16 numbers.";
	}

		
	if(! retorno) alert(msj);
	
	return(retorno);

}

function add_to_cart(path, m){

}

function remove_from_cart(){

}

function buy_now(){

}
