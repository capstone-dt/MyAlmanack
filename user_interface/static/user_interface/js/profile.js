
// @Author: Michael Resnik

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 						FRIEND BUTTON LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

function addFriendClicked(){
	console.log("addFriendClicked");
	console.log(_name_selected);
	var addFormElem = document.getElementById("id_FIreqalias");
	addFormElem.value = _name_selected;
	console.log(addFormElem);
	var submitAddFriend = document.getElementById("submitAddFriend");
	submitAddFriend.click();
}
function remFriendClicked(){
	console.log("remFriendClicked");
	console.log(_name_selected);
	var remFormElem = document.getElementById("id_FIremalias");
	remFormElem.value = _name_selected;
	console.log(remFormElem);
	var submitRemFriend = document.getElementById("submitRemFriend");
	submitRemFriend.click();
}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 						PROFILE DISPLAY LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

var database_user_json = {};
var database_selected_json = {};
function loadSelectedData(){
	var name_div = document.getElementById("name_display");
	name_div.innerText = database_selected_json.first_name + " " + database_selected_json.last_name;
	var alias_div = document.getElementById("alias_display");
	alias_div.innerText = "@" + database_selected_json.alias;
	var desc_div = document.getElementById("description_display");
	desc_div.innerText = database_selected_json.user_desc;
	if(database_selected_json.user_desc == ""){
		desc_div.innerText = "No description has been provided."
		desc_div.style.color = "grey";
	}
	var prof_pic_div = document.getElementById("imageDisplay");
	var img_div = base64ToImagePassed(database_selected_json.profile_picture, prof_pic_div);
	img_div.style.width = "175px";
	img_div.style.height = "175px";
	updateFriendsCards();
	updateGroupsCards();
}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 							CARD LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

var card_picture_dim = 75;
function updateFriendsCards(){
	var friends_cont_div = document.getElementById("friends_cont_div");
	for(var i = 0; i < database_selected_json.friends_info.length; i++){
		var curr_friend = database_selected_json.friends_info[i];
		var col_div = document.createElement("div");
		col_div.className = "col card-col";
		var card_div = document.createElement("div");
		card_div.className = "cust-card card pr-0";

		var row_div = document.createElement("div");
		row_div.className = "row";
		row_div.style = "width:300px; padding-left:20px; padding-top:5px;"

		var image_div = document.createElement("div");
		var def_image = base64ToImage(curr_friend.profile_picture);
		def_image.setAttribute("width", card_picture_dim + "px");
		def_image.setAttribute("height", card_picture_dim + "px");
		image_div.className = "float-left";
		image_div.appendChild(def_image);


		var user_text_div = document.createElement("div");
		user_text_div.innerHTML = curr_friend.first_name + " " + curr_friend.last_name + "<br>";
		var alias_div = document.createElement('a');
		alias_div.href = "javascript:redir('redirfb/" + curr_friend.firebase_id + "');";
		alias_div.innerText = "@" + curr_friend.alias;
		user_text_div.style ="display:inline; font-size:20px; padding-left:10px;";
		user_text_div.className = "float-left";
		user_text_div.appendChild(alias_div);


		row_div.appendChild(image_div);
		row_div.appendChild(user_text_div);
		card_div.appendChild(row_div);
		col_div.appendChild(card_div);
		friends_cont_div.appendChild(col_div);
		card_div.setAttribute("width", (user_text_div.getBoundingClientRect().width + card_picture_dim + 20) + "px");
		card_div.setAttribute("height", "120px");
		col_div.setAttribute("height", "120px");
	}
}
// Updates group cards with needed information
function updateGroupsCards(){
	var groups_cont_div = document.getElementById("groups_cont_div");
	for(var i = 0; i < database_selected_json.groups_info.length; i++){
		var curr_group = database_selected_json.groups_info[i];
		var col_div = document.createElement("div");
		col_div.className = "col card-col";
		var card_div = document.createElement("div");
		card_div.className = "cust-card card pr-0";

		var row_div = document.createElement("div");
		row_div.className = "row";
		row_div.style = "width:300px; padding-left:20px; padding-top:5px;"

		var group_text_div = document.createElement("div");
		var inner_group_div = document.createElement("a");
		inner_group_div.href = "javascript:redir('redirgn/" + curr_group.group_name + "');";
		inner_group_div.innerText = curr_group.group_name;
		group_text_div.style ="display:inline; font-size:20px; padding-left:10px;";
		group_text_div.className = "float-left";
		group_text_div.appendChild(inner_group_div);

		row_div.appendChild(group_text_div);
		card_div.appendChild(row_div);
		col_div.appendChild(card_div);
		groups_cont_div.appendChild(col_div);
		card_div.setAttribute("width", (groups_cont_div.getBoundingClientRect().width + card_picture_dim + 20) + "px");
		card_div.setAttribute("height", "120px");
		col_div.setAttribute("height", "120px");
	}
}