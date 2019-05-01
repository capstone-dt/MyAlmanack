
// @Author: Michael Resnik

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 						GROUP BUTTON LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

function joinGroupClicked(){
	var join_group_input = document.getElementById("id_GIreqname");
	join_group_input.value = group_dict.group_name;
	var join_submit = document.getElementById("submitJoinGroup");
	join_submit.click();
}
function leaveGroupClicked(){
	var leave_group_input = document.getElementById("id_GIremname");
	leave_group_input.value = group_dict.group_name;
	var leave_submit = document.getElementById("submitLeaveGroup");
	leave_submit.click();
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 						GROUP DISPLAY LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

function updateGroupDataVisual(){
	var group_name_div = document.getElementById("groupNameDisplay");
	group_name_div.innerHTML = "Group : " + group_dict.group_name;
	var group_desc_div = document.getElementById("groupDescDisplay");
	group_desc_div.innerText = group_dict.group_desc;
	if(group_dict.group_desc == ""){
		group_desc_div.innerText = "No description has been provided."
		group_desc_div.style.color = "grey";
	}
	if(group_dict.status == "MEMBER"){
		var leaveGroupButton = document.getElementById("leaveGroupButton");
		leaveGroupButton.style.display = "block";
		var joinGroupButton = document.getElementById("joinGroupButton");
		joinGroupButton.style.display = "none";
		var addMemberButton = document.getElementById("addMemberID");
		addMemberButton.style.display = "none";
	}else if (group_dict.status == "ADMIN"){
		var leaveGroupButton = document.getElementById("leaveGroupButton");
		leaveGroupButton.style.display = "none";
		var joinGroupButton = document.getElementById("joinGroupButton");
		joinGroupButton.style.display = "none";
		var addMemberButton = document.getElementById("addMemberID");
		addMemberButton.style.display = "inline-block";
	}else{
		var joinGroupButton = document.getElementById("joinGroupButton");
		joinGroupButton.style.display = "block";
		var leaveGroupButton = document.getElementById("leaveGroupButton");
		leaveGroupButton.style.display = "none";
		var addMemberButton = document.getElementById("addMemberID");
		addMemberButton.style.display = "none";
	}
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 							CARD LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
var card_picture_dim = 75;
function updateAdminCards(){
	var admin_cont_div = document.getElementById("admin_cont_div");
	for(var i = 0; i < group_dict.admins.length; i++){
		var curr_admin = group_dict.admins[i];
		var col_div = document.createElement("div");
		col_div.className = "cust-card col card-col";
		var card_div = document.createElement("div");
		card_div.className = "cust-card card pr-0";

		var row_div = document.createElement("div");
		row_div.className = "row";
		row_div.style = "padding-left:20px; padding-top:10px;"

		var image_div = document.createElement("div");
		var def_image = base64ToImage(curr_admin.profile_picture);
		def_image.setAttribute("width", card_picture_dim + "px");
		def_image.setAttribute("height", card_picture_dim + "px");
		image_div.className = "float-left";
		image_div.appendChild(def_image);


		var user_text_div = document.createElement("div");
		user_text_div.innerHTML = curr_admin.first_name + " " + curr_admin.last_name + "<br>";
		var alias_div = document.createElement('a');
		alias_div.href = "javascript:redir('redirfb/" + curr_admin.firebase_id + "');";
		alias_div.innerText = "@" + curr_admin.alias;
		user_text_div.style ="display:inline; font-size:20px; padding-left:10px;";
		user_text_div.className = "float-left";
		user_text_div.appendChild(alias_div);


		row_div.appendChild(image_div);
		row_div.appendChild(user_text_div);
		card_div.appendChild(row_div);
		col_div.appendChild(card_div);
		admin_cont_div.appendChild(col_div);
		card_div.setAttribute("width", (user_text_div.getBoundingClientRect().width + card_picture_dim + 100) + "px");
		card_div.setAttribute("height", "120px");
		col_div.setAttribute("height", "120px");
		col_div.setAttribute("width", (user_text_div.getBoundingClientRect().width + card_picture_dim + 100) + "px");
	}
}
function updateMemberCards(){
	var member_cont_div = document.getElementById("member_cont_div");
	for(var i = 0; i < group_dict.members.length; i++){
		var curr_member = group_dict.members[i];
		var isAdmin = false;
		for(var j = 0; j < group_dict.admins.length; j++){
			var curr_admin = group_dict.admins[j];
			if(curr_member.firebase_id == curr_admin.firebase_id){
				isAdmin = true;
				break;
			}
		}
		if(isAdmin){
			continue;
		}
		var col_div = document.createElement("div");
		col_div.className = "cust-card col card-col";
		var card_div = document.createElement("div");
		card_div.className = "cust-card card pr-0";

		var row_div = document.createElement("div");
		row_div.className = "row";
		row_div.style = "padding-left:20px; padding-top:10px;"

		var image_div = document.createElement("div");
		var def_image = base64ToImage(curr_member.profile_picture);
		def_image.setAttribute("width", card_picture_dim + "px");
		def_image.setAttribute("height", card_picture_dim + "px");
		image_div.className = "float-left";
		image_div.appendChild(def_image);


		var user_text_div = document.createElement("div");
		user_text_div.innerHTML = curr_member.first_name + " " + curr_member.last_name + "<br>";
		var alias_div = document.createElement('a');
		alias_div.href = "javascript:redir('redirfb/" + curr_member.firebase_id + "');";
		alias_div.innerText = "@" + curr_member.alias;
		user_text_div.style ="display:inline; font-size:20px; padding-left:10px;";
		user_text_div.className = "float-left";
		user_text_div.appendChild(alias_div);


		row_div.appendChild(image_div);
		row_div.appendChild(user_text_div);
		card_div.appendChild(row_div);
		col_div.appendChild(card_div);
		member_cont_div.appendChild(col_div);
		card_div.setAttribute("width", (user_text_div.getBoundingClientRect().width + card_picture_dim + 100) + "px");
		card_div.setAttribute("height", "120px");
		col_div.setAttribute("height", "120px");
		col_div.setAttribute("width", (user_text_div.getBoundingClientRect().width + card_picture_dim + 100) + "px");
	}
}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 						INVITE DISPLAY LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
$(document).ready(function() {
	populateGroupMemberInviteSelectDropdown();
});
var group_member_invite_ids = [];
function populateGroupMemberInviteSelectDropdown(){
	var friends_to_pop = database_header_info.friend_info;
	var groupMemberInvitesSelectDropdown = document.getElementById("groupMemberInvites_select_dropdown");

	var filtered_friends = [];
	for(var i = 0; i < friends_to_pop.length; i++){
		var curr_friend = friends_to_pop[i];
		var contains_member = false;
		for(var j = 0; j < group_dict.members.length; j++){
			var curr_member = group_dict.members[j];
			if(curr_friend.firebase_id == curr_member.firebase_id){
				contains_member = true;
				break;
			}
		}
		if(contains_member == false){
			filtered_friends.push(curr_friend);
		}
	}


	for(var i = 0; i < filtered_friends.length; i++){
		var curr_friend = filtered_friends[i];
		var curr_a = document.createElement("a");
		curr_a.className = "dropdown-item";
		var temp_id = curr_friend.alias + "_check_gi";
		curr_a.href = "#";
		curr_a.setAttribute("onclick", "checkMemberGroupInviteSelect('" + temp_id + "')");
		var curr_label = document.createElement("label");
		curr_label.className = "check_container";
		curr_label.innerText = curr_friend.first_name + " " + curr_friend.last_name;
		var curr_input = document.createElement("input");
		curr_input.type = "checkbox";
		curr_input.id = temp_id;
		curr_input.setAttribute("alias", curr_friend.alias);
		var curr_span = document.createElement("span");
		curr_span.className = "checkmark";
		curr_label.appendChild(curr_input);
		curr_label.appendChild(curr_span);
		curr_a.appendChild(curr_label);
		var temp_form = document.createElement('form');
		temp_form.appendChild(curr_a);
		groupMemberInvitesSelectDropdown.appendChild(temp_form);
		group_member_invite_ids.push({"check_id" : temp_id, "alias" : curr_friend.alias, "firebase_id" : curr_friend.firebase_id});
	}
}
function checkMemberGroupInviteSelect(sel_id){
	var check_input = document.getElementById(sel_id);
	if(check_input.checked){
		check_input.checked = false;
		check_input.setAttribute("flag", "false");
	}else{
		check_input.checked = true;
		check_input.setAttribute("flag", "true");
	}
	var groupInviteTitle = document.getElementById("groupMemberInviteNameId");
	var str_place = "";
	var groupMemberInvitesSelected = getGroupMemberInvitesSelected();
	for(var i = 0; i < groupMemberInvitesSelected.length; i++){
		str_place += "@" + groupMemberInvitesSelected[i];
		if(i != groupMemberInvitesSelected.length - 1){
			str_place += ", ";
		}
	}
	groupInviteTitle.innerText = str_place;
	if(str_place == ""){
		groupInviteTitle.innerText = 'Select members to invite...'
	}
	remainderEditGroupMembers();
}
function getGroupMemberInvitesSelected(){
	var valid = [];
	for(var i = 0; i < group_member_invite_ids.length; i++){
		var curr_div = document.getElementById(group_member_invite_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(group_member_invite_ids[i].alias);
		}
	}
	return valid;
}
function getGroupMemberInvitesSelectedFirebase(){
	var valid = [];
	for(var i = 0; i < group_member_invite_ids.length; i++){
		var curr_div = document.getElementById(group_member_invite_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(group_member_invite_ids[i].firebase_id);
		}
	}
	return valid;
}
function remainderEditGroupMembers(){

	var form_group_name = document.getElementById("id_GIname");
	form_group_name.value = group_dict.group_name;

	var form_group_inv = document.getElementById("id_GIinvite_members");
	var firebase_selected_group = getGroupMemberInvitesSelectedFirebase();
	var temp_string = "";
	for(var i = 0; i < firebase_selected_group.length; i++){
		temp_string += firebase_selected_group[i];
		if(i != firebase_selected_group.length - 1){
			temp_string += ",";
		}
	}
	console.log("remainderEditGroup invites:", temp_string);
	form_group_inv.value = temp_string;
}
function updateAndClickGroupMembers(){
	console.log("updateAndClickGroup");
	remainderEditGroupMembers();
	var submitButton = document.getElementById("submitInviteMembers");
	submitButton.click();
}