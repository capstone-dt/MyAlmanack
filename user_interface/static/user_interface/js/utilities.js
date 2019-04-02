function base64ToImage(base64DataString){
	var image = new Image();
	image.setAttribute('src', 'data:image/png;base64,' + base64DataString);
	image.setAttribute('width', "200px");
	image.setAttribute('height', "200px");
	return image;
}
