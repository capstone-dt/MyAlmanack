
// @Author: Michael Resnik

function windowResized(){
	console.log("window resized");
	updateSearch();
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 						FRIEND BUTTON LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

function addFriendClicked(_name_selected){
	console.log("addFriendClicked");
	console.log(_name_selected);
	var addFormElem = document.getElementById("id_FIreqalias");
	addFormElem.value = _name_selected;
	console.log(addFormElem);
	var submitAddFriend = document.getElementById("submitAddFriend");
	submitAddFriend.click();
}
function remFriendClicked(_name_selected){
	console.log("remFriendClicked");
	console.log(_name_selected);
	var remFormElem = document.getElementById("id_FIremalias");
	remFormElem.value = _name_selected;
	console.log(remFormElem);
	var submitRemFriend = document.getElementById("submitRemFriend");
	submitRemFriend.click();
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 						SEARCH DISPLAY LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //


function clearDivLists(){
	var list_div = document.getElementById("height_list");
	while(list_div.children.length > 0){
		list_div.removeChild(list_div.children[0]);
	}
}
function drawUserElement(struct){
	var a_elem = document.createElement('a');
	a_elem.className = "navbar-text";
	a_elem.style = "width:100%; padding-right:30px;";
	a_elem.style.borderBottom = "1px solid grey";

	var def_image = base64ToImage(struct.profile_picture);
	def_image.setAttribute("width", "80px");
	def_image.setAttribute("height", "80px");
	var list_elem = document.createElement('li');
	list_elem.className = "nav-item";
	list_elem.style = "width:100%; "

	var row_elem = document.createElement('div');
	row_elem.className = "row";

	var image_div = document.createElement('div');
	image_div.style = "display:inline; padding-right:20px; padding-left:20px;";
	image_div.appendChild(def_image);
	image_div.className = "float-left";
	var user_text_div = document.createElement('div');
	user_text_div.innerHTML = struct.first_name + " " + struct.last_name + "<br>";
	var alias_div = document.createElement('a');
	alias_div.href = "javascript:redir('redirfb/" + struct.firebase_id + "');";
	alias_div.innerText = "@" + struct.alias;
	user_text_div.appendChild(alias_div);
	user_text_div.style ="display:inline; font-size:20px;";
	user_text_div.className = "float-left";

	row_elem.appendChild(image_div);
	row_elem.appendChild(user_text_div);
	if(struct.isSelf == false){
		if(struct.isFriend == false){
			if(struct.isRequested == true){
				var button_cont = document.createElement('div');
				button_cont.className = "ml-auto";
				var temp_addButton = document.createElement('div');
				temp_addButton.className="requestedButton";
				temp_addButton.innerText="Friend Requested";
				temp_addButton.style="width:200px;"
				button_cont.appendChild(temp_addButton);
				row_elem.appendChild(button_cont);
			}else{
				// Add friend Button
				var button_cont = document.createElement('div');
				button_cont.className = "ml-auto";
				var temp_addButton = document.createElement('div');
				temp_addButton.className="friendButton";
				temp_addButton.innerText="Add Friend";
				temp_addButton.setAttribute("onclick", "addFriendClicked('" + struct.alias + "');");
				temp_addButton.style="width:200px;"
				button_cont.appendChild(temp_addButton);
				row_elem.appendChild(button_cont);
			}
		}else if(struct.isFriend == true){
			// Remove Friend Button
			var button_cont = document.createElement('div');
			button_cont.className = "ml-auto";
			var temp_remButton = document.createElement('div');
			temp_remButton.className="removeFriendButton ml-auto";
			temp_remButton.innerText="Remove Friend";
			temp_remButton.setAttribute("onclick", "remFriendClicked('" + struct.alias + "');");
			temp_remButton.style="width:200px;"
			button_cont.appendChild(temp_remButton);
			row_elem.appendChild(button_cont);
		}
	}

	a_elem.appendChild(row_elem);

	var list_div = document.getElementById("height_list");
	list_elem.appendChild(a_elem);
	list_div.appendChild(list_elem);
	return list_div;
}
function drawGroupElement(struct){
	var description = struct.description;
	var list_elem = document.createElement('li');
	list_elem.className = "nav-item";
	list_elem.style = "width:100%;"

	var row_elem = document.createElement('div');
	row_elem.className = "row";

	var a_elem = document.createElement('a');
	a_elem.className = "navbar-text";
	a_elem.innerHTML = struct.group_name;
	a_elem.href = "javascript:redir('redirgn/" + struct.group_name + "');";
	a_elem.style = "width:100%; font-size:20px;";
	var desc_elem = document.createElement('a');
	desc_elem.className = "navbar-text";
	desc_elem.style = "width:100%; font-size:20px;";
	var list_div = document.getElementById("height_list");
	row_elem.appendChild(a_elem);
	if(struct.group_desc != ""){
		desc_elem.innerText = struct.group_desc;
		row_elem.appendChild(desc_elem);
	}
	row_elem.style.borderBottom = "1px solid grey";
	list_elem.appendChild(row_elem);
	list_div.appendChild(list_elem);
	return list_div;
}
function drawEventElement(struct){
	var a_elem = document.createElement('a');
	a_elem.className = "navbar-text";
	a_elem.style = "width:100%";
	a_elem.style.borderBottom = "1px solid grey";

	var list_elem = document.createElement('li');
	list_elem.className = "nav-item";
	list_elem.style = "width:100%; "

	var row_elem = document.createElement('div');
	row_elem.className = "row";
	row_elem.style = "padding-left:20px; "

	var event_text_div = document.createElement('div');
	event_text_div.innerHTML = struct.event_title + "<br>";
	var alias_div = document.createElement('a');
	alias_div.innerText = "@" + struct.event_creator_alias;
	alias_div.href = "javascript:redir('redirfb/" + struct.event_creator_firebase_id + "');";
	event_text_div.appendChild(alias_div);
	event_text_div.innerHTML += "<br>" + struct.description;
	event_text_div.style ="display:inline; font-size:20px;";
	event_text_div.className = "float-left";

	row_elem.appendChild(event_text_div);
	a_elem.appendChild(row_elem);

	var list_div = document.getElementById("height_list");
	list_elem.appendChild(a_elem);
	list_div.appendChild(list_elem);
	return list_div;
}

function populateUsers(){
	for(var i = 0; i < _searchElements.users.length; i++){
		var curr_struct = _searchElements.users[i];
		drawUserElement(curr_struct);
	}
}

function populateEvents(){
	for(var i = 0; i < _searchElements.events.length; i++){
		var curr_struct = _searchElements.events[i];
		drawEventElement(curr_struct);
	}
}

function populateGroups(){
	for(var i = 0; i < _searchElements.groups.length; i++){
		var curr_struct = _searchElements.groups[i];
		drawGroupElement(curr_struct);
	}
}

function updateSearch(){
	var trap_cont_id = "trap_cont";
	var trap_cont_div = document.getElementById(trap_cont_id);
	var trap_rect = trap_cont_div.getBoundingClientRect();
	var cont_id = "scroll_div_cont_row";
	var cont_div = document.getElementById(cont_id);
	var rect = cont_div.getBoundingClientRect();
	var users_tab_div = document.getElementById("users_tab");
	var users_rect = users_tab_div.getBoundingClientRect();
	var def_left = users_rect.left + 15;
	var def_width = window.innerWidth - 2*def_left;
	def_width = Math.max(def_width, 370);
	cont_div.style = "position:absolute; border-color: black;"
	+ " top:" 
	+ (users_rect.bottom - 7) + "px;"
	+ "height:" + (50) + "%;"
	+ "width:" + (def_width) + "px;"
	+ "left:" + (def_left) + "px;";
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 						SELECT TABS LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

function selectTab(sel_id){
	if(_tabSelect === sel_id){
		return;
	}
	_tabSelect = sel_id;
	clearDivLists();
	updateSearch();
	var scroll_div_cont = document.getElementById("scroll_div_cont");
	scroll_div_cont.scrollTop = 0;
	scroll_div_cont.style.width ="100%";
	var trap_cont = document.getElementById("trap_cont");
	var children = trap_cont.children;
	console.log("selected:" + sel_id);
	console.log(children);
	for(var i = 0; i < children.length; i++){
		if(children[i].id === sel_id){
			children[i].className = "selected";
			continue;
		}
		children[i].className = "";
	}
	switch(sel_id){
		case "events_tab":
			selectEvents();
			break;
		case "group_tab":
			selectGroups();
			break;
		case "users_tab":
			selectUsers();
			break;
		default:
			return;
	}
}
function selectUsers(){
	console.log("select:users");
	populateUsers();
}
function selectEvents(){
	console.log("select:events");
	populateEvents();
}
function selectGroups(){
	console.log("select:groups");
	populateGroups();
}
function mainSearch(){
	window.addEventListener("resize", windowResized);
	var searchTermDisplay = document.getElementById("searchTermDisplay");
	searchTermDisplay.innerText = _searchElements.search_term;
	selectTab("users_tab");
	windowResized();
}