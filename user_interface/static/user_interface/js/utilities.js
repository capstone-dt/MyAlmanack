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
