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
