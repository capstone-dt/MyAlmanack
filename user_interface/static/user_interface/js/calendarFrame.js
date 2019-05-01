
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 					FREETIME CHECKED LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
function switchTest(){
	if(window.scrollY != 0){
		_prev_scroll_y = window.scrollY;
	}
	freetimeChecked = !freetimeChecked;
	if(_switchType == "list" || _switchType == "month"){
		switchCalendarView(_cont_id, _switchType);
	}
	smoothScrollTo();
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 					CREATE EVENT DISPLAY LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
function updateEventForm(){
	// Event Name
	var enter_name = document.getElementById("inputEventName");
	var form_name = document.getElementById("id_EIname");
	form_name.value = enter_name.value;
	var enter_desc = document.getElementById("inputEventDesc");
	var form_desc = document.getElementById("id_EIdescription");
	form_desc.value = enter_desc.value;

	var enter_start_date = document.getElementById("inputStartDate");
	var enter_start_time = document.getElementById("inputStartTime");
	
	var form_start = document.getElementById("id_EIstart");
	var start_date_day = new Date(enter_start_date.value + " " + enter_start_time.value);
	form_start.value = start_date_day.getTime() + "";
	// console.log(form_start);
	// ADD DATE FORMATTING

	// form_start.value = enter_start.value;
	var enter_end_date = document.getElementById("inputEndDate");
	var enter_end_time = document.getElementById("inputEndTime");
	var form_end = document.getElementById("id_EIend");
	var end_date_day = new Date(enter_end_date.value + " " + enter_end_time.value);
	form_end.value = end_date_day.getTime() + "";
	// console.log(form_end);
	// ADD DATE FORMATTING

	// form_end.value = enter_end.value;
	var form_repeat = document.getElementById("id_EIrepeat");
	form_repeat.value = _repeatClicked + "";

	var form_repeat_pattern = document.getElementById("id_EIrepeat_pattern");
	var pattern_str = "";
	var check_su = document.getElementById("checkSunday");
	pattern_str += (check_su.checked ? "1" : 0);
	var check_mo = document.getElementById("checkMonday");
	pattern_str += (check_mo.checked ? "1" : 0);
	var check_tu = document.getElementById("checkTuesday");
	pattern_str += (check_tu.checked ? "1" : 0);
	var check_we = document.getElementById("checkWednesday");
	pattern_str += (check_we.checked ? "1" : 0);
	var check_th = document.getElementById("checkThursday");
	pattern_str += (check_th.checked ? "1" : 0);
	var check_fr = document.getElementById("checkFriday");
	pattern_str += (check_fr.checked ? "1" : 0);
	var check_sa = document.getElementById("checkSaturday");
	pattern_str += (check_sa.checked ? "1" : 0);
	form_repeat_pattern.value = pattern_str;

	// Invites
	// var enter_invite = document.getElementById("inputInviteList");
	var form_invite = document.getElementById("id_EIinvite");
	var invite_string = "";
	var invite_sel = getInvitesSelectedFirebase();
	for(var i = 0; i < invite_sel.length; i++){
		invite_string += invite_sel[i];
		if(i != invite_sel.length - 1){
			invite_string += ",";
		}
	}
	form_invite.value = invite_string;

	

	// Whitelist
	// var enter_whitelist = document.getElementById("inputWhitelist");
	var form_whitelist = document.getElementById("id_EIwhitelist");
	var whitelist_string = "";
	var whitelist_sel = getWhitelistSelectedFirebase();
	for(var i = 0; i < whitelist_sel.length; i++){
		whitelist_string += whitelist_sel[i];
		if(i != whitelist_sel.length - 1){
			whitelist_string += ",";
		}
	}
	form_whitelist.value = whitelist_string;


	// Blacklist
	// var enter_blacklist = document.getElementById("inputBlacklist");
	var form_blacklist = document.getElementById("id_EIblacklist");
	var blacklist_string = "";
	var blacklist_sel = getBlacklistSelectedFirebase();
	for(var i = 0; i < blacklist_sel.length; i++){
		blacklist_string += blacklist_sel[i];
		if(i != blacklist_sel.length - 1){
			blacklist_string += ",";
		}
	}
	form_blacklist.value = blacklist_string;

	var blacklistForm_input = document.getElementById("blacklistFormID");
	var whitelistForm_input = document.getElementById("whitelistFormID");


	if(getWhitelistSelectedFirebase().length > 0){
		// Disable blacklist
		blacklistForm_input.style = "display:none;";
		// Clear blacklist string
		form_blacklist.value = "";

	}else if(getWhitelistSelectedFirebase().length == 0){
		// Enable blacklist
		blacklistForm_input.style = "display:block;";

	}
	if(getBlacklistSelectedFirebase().length > 0){
		// Disable whitelist
		whitelistForm_input.style = "display:none;"
	}else if(getBlacklistSelectedFirebase().length == 0){
		whitelistForm_input.style = "display:block;"

	}


}
function validEventForm(){
	var form_name = document.getElementById("id_EIname");
	if(form_name.value == ""){
		return false;
	}
	var form_start = document.getElementById("id_EIstart");
	if(form_start.value == "" || form_start.value == "NaN"){
		return false;
	}
	var form_end = document.getElementById("id_EIend");
	if(form_end.value == "" || form_end.value == "NaN"){
		return false;
	}
	return true;
}

function updateAndSubmit(){
	updateEventForm();
	if(validEventForm() == true){
		var submitButton = document.getElementById("createEventHidden");
		submitButton.click();
	}
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 					CREATE EVENT POPULATE LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

$(document).ready(function() {
	populateInviteSelectDropdown();
	populateWhitelistSelectDropdown();
	populateBlacklistSelectDropdown();
});

// INVITES DROPDOWN
var invite_ids = [];
function populateInviteSelectDropdown(){
	var friends_to_pop = _calendar_struct.calendar_data.member_info;
	var invitesSelectDropdown = document.getElementById("invites_select_dropdown");
	for(var i = 0; i < friends_to_pop.length; i++){
		var curr_friend = friends_to_pop[i];
		var curr_a = document.createElement("a");
		curr_a.className = "dropdown-item";
		var temp_id = curr_friend.alias + "_check_i";
		curr_a.href = "#";
		curr_a.setAttribute("onclick", "checkInviteSelect('" + temp_id + "')");
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
		invitesSelectDropdown.appendChild(temp_form);
		invite_ids.push({"check_id" : temp_id, "alias" : curr_friend.alias, "firebase_id" : curr_friend.firebase_id});
	}
}
function checkInviteSelect(sel_id){
	var check_input = document.getElementById(sel_id);
	if(check_input.checked){
		check_input.checked = false;
		check_input.setAttribute("flag", "false");
	}else{
		check_input.checked = true;
		check_input.setAttribute("flag", "true");
	}
	var inviteTitle = document.getElementById("inviteNameId");
	var str_place = "";
	var invitesSelected = getInvitesSelected();
	for(var i = 0; i < invitesSelected.length; i++){
		str_place += "@" + invitesSelected[i];
		if(i != invitesSelected.length - 1){
			str_place += ", ";
		}
	}
	inviteTitle.innerText = str_place;
	if(str_place == ""){
		inviteTitle.innerText = 'Select members to invite...'
	}
}
function getInvitesSelected(){
	var valid = [];
	for(var i = 0; i < invite_ids.length; i++){
		var curr_div = document.getElementById(invite_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(invite_ids[i].alias);
		}
	}
	return valid;
}
function getInvitesSelectedFirebase(){
	var valid = [];
	for(var i = 0; i < invite_ids.length; i++){
		var curr_div = document.getElementById(invite_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(invite_ids[i].firebase_id);
		}
	}
	return valid;
}

// WHITELIST DROPDOWN
var whitelist_ids = [];

function populateWhitelistSelectDropdown(){
	var friends_to_pop = _calendar_struct.calendar_data.member_info;
	var whitelistSelectDropdown = document.getElementById("whitelist_select_dropdown");
	for(var i = 0; i < friends_to_pop.length; i++){
		var curr_friend = friends_to_pop[i];
		var curr_a = document.createElement("a");
		curr_a.className = "dropdown-item";
		var temp_id = curr_friend.alias + "_check_w";
		curr_a.href = "#";
		curr_a.setAttribute("onclick", "checkWhitelistSelect('" + temp_id + "')");
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
		whitelistSelectDropdown.appendChild(temp_form);
		whitelist_ids.push({"check_id" : temp_id, "alias" : curr_friend.alias, "firebase_id" : curr_friend.firebase_id});
	}
}
function checkWhitelistSelect(sel_id){
	var check_input = document.getElementById(sel_id);
	if(check_input.checked){
		check_input.checked = false;
		check_input.setAttribute("flag", "false");
	}else{
		check_input.checked = true;
		check_input.setAttribute("flag", "true");
	}
	var whitelistTitle = document.getElementById("whitelistNameId");
	var str_place = "";
	var whitelistSelected = getWhitelistSelected();
	for(var i = 0; i < whitelistSelected.length; i++){
		str_place += "@" + whitelistSelected[i];
		if(i != whitelistSelected.length - 1){
			str_place += ", ";
		}
	}
	whitelistTitle.innerText = str_place;
	if(str_place == ""){
		whitelistTitle.innerText = 'Select members to Whitelist...'
	}
	updateEventForm();
}

function getWhitelistSelected(){
	var valid = [];
	for(var i = 0; i < whitelist_ids.length; i++){
		var curr_div = document.getElementById(whitelist_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(whitelist_ids[i].alias);
		}
	}
	return valid;
}
function getWhitelistSelectedFirebase(){
	var valid = [];
	for(var i = 0; i < whitelist_ids.length; i++){
		var curr_div = document.getElementById(whitelist_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(whitelist_ids[i].firebase_id);
		}
	}
	return valid;
}

// BLACKLIST DROPDOWN
var blacklist_ids = [];

function populateBlacklistSelectDropdown(){
	var friends_to_pop = _calendar_struct.calendar_data.member_info;
	var blacklistSelectDropdown = document.getElementById("blacklist_select_dropdown");
	for(var i = 0; i < friends_to_pop.length; i++){
		var curr_friend = friends_to_pop[i];
		var curr_a = document.createElement("a");
		curr_a.className = "dropdown-item";
		var temp_id = curr_friend.alias + "_check_b";
		curr_a.href = "#";
		curr_a.setAttribute("onclick", "checkBlacklistSelect('" + temp_id + "')");
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
		blacklistSelectDropdown.appendChild(temp_form);
		blacklist_ids.push({"check_id" : temp_id, "alias" : curr_friend.alias, "firebase_id" : curr_friend.firebase_id});
	}
}

function checkBlacklistSelect(sel_id){
	var check_input = document.getElementById(sel_id);
	if(check_input.checked){
		check_input.checked = false;
		check_input.setAttribute("flag", "false");
	}else{
		check_input.checked = true;
		check_input.setAttribute("flag", "true");
	}
	var blacklistTitle = document.getElementById("blacklistNameId");
	var str_place = "";
	var blacklistSelected = getBlacklistSelected();
	for(var i = 0; i < blacklistSelected.length; i++){
		str_place += "@" + blacklistSelected[i];
		if(i != blacklistSelected.length - 1){
			str_place += ", ";
		}
	}
	blacklistTitle.innerText = str_place;
	if(str_place == ""){
		blacklistTitle.innerText = 'Select members to Whitelist...'
	}
	updateEventForm();
}

function getBlacklistSelected(){
	var valid = [];
	for(var i = 0; i < blacklist_ids.length; i++){
		var curr_div = document.getElementById(blacklist_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(blacklist_ids[i].alias);
		}
	}
	return valid;
}

function getBlacklistSelectedFirebase(){
	var valid = [];
	for(var i = 0; i < blacklist_ids.length; i++){
		var curr_div = document.getElementById(blacklist_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(blacklist_ids[i].firebase_id);
		}
	}
	return valid;
}

// REPEAT LOGIC
_repeatClicked = false;
function repeatClicked(){
	_repeatClicked = !_repeatClicked;
	var hiddenPattern = document.getElementById("patternHider");
	if(_repeatClicked){
		hiddenPattern.style.display = "block";
	}else{
		hiddenPattern.style.display = "none";

	}
	updateEventForm();
}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 					EDIT EVENT DISPLAY LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
function updateEditEventForm(){
	var enter_name = document.getElementById("inputEditEventName");
	var form_name = document.getElementById("id_EIeditname");
	form_name.value = enter_name.value;
	var enter_desc = document.getElementById("inputEditEventDesc");
	var form_desc = document.getElementById("id_EIeditdescription");
	form_desc.value = enter_desc.value;

	var enter_start_date = document.getElementById("inputEditStartDate");
	var enter_start_time = document.getElementById("inputEditStartTime");
	
	var form_start = document.getElementById("id_EIeditstart");
	var start_date_day = new Date(enter_start_date.value + " " + enter_start_time.value);
	form_start.value = start_date_day.getTime() + "";
	// console.log(form_start);
	// ADD DATE FORMATTING

	// form_start.value = enter_start.value;
	var enter_end_date = document.getElementById("inputEditEndDate");
	var enter_end_time = document.getElementById("inputEditEndTime");
	var form_end = document.getElementById("id_EIeditend");
	var end_date_day = new Date(enter_end_date.value + " " + enter_end_time.value);
	form_end.value = end_date_day.getTime() + "";
}
function validEditEventForm(){
	return true;
}
function updateAndSubmitEdit(){
	updateEditEventForm();
	if(validEditEventForm() == true){
		var submitButton = document.getElementById("editEventSubmitHidden");
		submitButton.click();
	}
}

function updateEventRepeatForm(){
	console.log("updateEventRepeatForm");
	var enter_name = document.getElementById("inputEditRepeatEventName");
	var form_name = document.getElementById("id_EIeditrepeatname");
	form_name.value = enter_name.value;
	var enter_desc = document.getElementById("inputEditRepeatEventDesc");
	var form_desc = document.getElementById("id_EIeditrepeatdescription");
	form_desc.value = enter_desc.value;

	var enter_start_date = document.getElementById("inputEditRepeatStartDate");
	var enter_start_time = document.getElementById("inputEditRepeatStartTime");
	
	var form_start = document.getElementById("id_EIeditrepeatstart");
	var start_date_day = new Date(enter_start_date.value + " " + enter_start_time.value);
	form_start.value = start_date_day.getTime() + "";
	// console.log(form_start);
	// ADD DATE FORMATTING

	// form_start.value = enter_start.value;
	var enter_end_date = document.getElementById("inputEditRepeatEndDate");
	var enter_end_time = document.getElementById("inputEditRepeatEndTime");
	var form_end = document.getElementById("id_EIeditrepeatend");
	var end_date_day = new Date(enter_end_date.value + " " + enter_end_time.value);
	form_end.value = end_date_day.getTime() + "";

	var form_repeat_pattern = document.getElementById("id_EIeditrepeat_pattern");
	var pattern_str = "";
	var check_su = document.getElementById("checkEditSunday");
	pattern_str += (check_su.checked ? "1" : 0);
	var check_mo = document.getElementById("checkEditMonday");
	pattern_str += (check_mo.checked ? "1" : 0);
	var check_tu = document.getElementById("checkEditTuesday");
	pattern_str += (check_tu.checked ? "1" : 0);
	var check_we = document.getElementById("checkEditWednesday");
	pattern_str += (check_we.checked ? "1" : 0);
	var check_th = document.getElementById("checkEditThursday");
	pattern_str += (check_th.checked ? "1" : 0);
	var check_fr = document.getElementById("checkEditFriday");
	pattern_str += (check_fr.checked ? "1" : 0);
	var check_sa = document.getElementById("checkEditSaturday");
	pattern_str += (check_sa.checked ? "1" : 0);
	form_repeat_pattern.value = pattern_str;


}

function updateAndSubmitEditRepeat(){
	updateEventRepeatForm();
	var submitButton = document.getElementById("editRepeatEventSubmitHidden");
	submitButton.click();
}