
var _days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
var _days_of_week_abv = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"];
var _days_of_week_abv_abv = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
var _months_of_year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var _times_of_day_12 = ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"];
var _redirecting = false;

function base64ToImage(base64DataString){
	var image = new Image();
	image.setAttribute('src', 'data:image/png;base64,' + base64DataString);
	return image;
}
function base64ToImagePassed(base64DataString, image_passed){
	image_passed.setAttribute('src', 'data:image/png;base64,' + base64DataString);
	return image_passed;
}
function parseQuotesJson(json_string){
	return JSON.parse(json_string.replace(/&quot;/g,'\"').replace(/&#39;/g,"\'"));
}
function redirHome(){
	_redirecting = true;
	var curr_loc = window.location.href;
	var curr_array = [...curr_loc];
	var new_loc = "";
	var slash_count = 0;
	for(var c_i = 0; c_i < curr_array.length && slash_count != 3; c_i++){
		var curr_char = curr_array[c_i];
		if(curr_char == "/"){
			slash_count++;
		}
		new_loc+=curr_char;
	}
	window.location.replace(new_loc);
}
function redir(passed){
	_redirecting = true;
	var curr_loc = window.location.href;
	var curr_array = [...curr_loc];
	var slash_count = 0;
	var new_loc = "";
	for(var c_i = 0; c_i < curr_array.length && slash_count != 3; c_i++){
		var curr_char = curr_array[c_i];
		if(curr_char == "/"){
			slash_count++;
		}
		new_loc+=curr_char;
	}
	window.location.replace(new_loc + passed);
}
function loadCalendarIfNonNull(){
	var calendar_frame_button = document.getElementById("loadCalendarFrameID");
	if(calendar_frame_button != null){
		calendar_frame_button.click();
	}
}

function customDateString(date){
	var date_string = _months_of_year[date.getMonth()] + " ";
	date_string += date.getDate() + ", ";
	date_string += date.getFullYear();
	return date_string;
}

function customTimeString(date){
	var hr = date.getHours();
	var min = date.getMinutes();
	if (min < 10) {
	    min = "0" + min;
	}
	var ampm = "am";
	if( hr > 12 ) {
	    hr -= 12;
	    ampm = "pm";
	}
	if(hr == 12){
		ampm = "pm";
	}
	if(hr == 0){
		hr = 12;
		ampm = "am";
	}
	var time_string = hr + ":" + min + ampm;
	return time_string;
}

function closeAllModals(){
	var all_close_buttons = document.getElementsByClassName("close");
	for(var i = 0; i < all_close_buttons.length; i++){
		var curr_close = all_close_buttons[i];
		curr_close.click();
	}
}
