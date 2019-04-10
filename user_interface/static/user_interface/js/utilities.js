function base64ToImage(base64DataString){
	var image = new Image();
	image.setAttribute('src', 'data:image/png;base64,' + base64DataString);
	return image;
}
