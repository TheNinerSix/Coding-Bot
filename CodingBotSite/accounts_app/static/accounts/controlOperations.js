//INPUT VALIDATION ISN'T IMPLEMENTED CURRENTLY
//COMMENTS CANNOT BE PROPERLY ADDED TO TEMPLATE LITERALS (` `) SO ALL COMMENTS WILL BE ABOVE THE FUNCTIONS
//ALL FORM SUBMISSION ARE SENT TO SELF AND NOT USED AT ALL

window.onload = function() {
	
	//Gives functionality to the popovers on Input fields
	$(function(){
		$('[data-toggle="popover"]').popover()
	  });

	$("#menuAction").submit(function() {
		var input = $("#commandLine").val(); //GET INPUT FIELD
		$("#commandLine").val(""); //CLEAR TEXT FIELD
		switch(input) {
			case "Pack Select": //URL REDIRECT
				window.location.assign("http://127.0.0.1:8000/game");
				console.log("Valid");
				break;
			case "Class Select":
				
				console.log("Valid");
				break;
			case "Progress Report":
				
				console.log("Valid");
				break;		
			case "Help":
				$("#contentLine").append( //DISPLAY TEXT
				`<p>'Pack Select' - Choose a question pack to work on<br/>
				'Class Select' - Choose the class you want to progress in<br/>
				'Progress Report' - View a report of how you're doing<br/>
				'Help' - Display all the available commands<br/>
				'Log Out' - Quit playing with this account</p>`);
				console.log("Valid");
				break;		
			case "Log Out": //URL REDIRECT
				window.location.assign("http://127.0.0.1:8000/");
				console.log("Valid");
				break;		
			default: //DISPLAY TEXT
				$("#contentLine").append(
				`<p>Invalid Input: Please type 'Help' if you 
				have forgotten the required command.</p>`);
				console.log("Invalid");
				break;	
		}
		$("#contentLine").scrollTop($("#contentLine")[0].scrollHeight); //FORCE SCROLL TO BOTTOM
		return false; //DON'T REFRESH PAGE
	});
}