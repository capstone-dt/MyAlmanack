// GLOBALS
var _cont_id = "cal_grid_cont";
var _switchType = "month";
var _select_class = "calSelect";
var _select_id = "";
var headerArray_top = [];
var _header_top_div = null ;
var headerArray_side = [];
var gridArray = [];
var calArray = [];
var divRowsArray =[];
var eventDivArray = [];
var populatedEvents = [];
var populatedEvents_w = [];
var populatedEvents_d = [];
var x_offset = 0, y_offset = 0;
var _month_selected = "03";
var _year_selected = "2019";
var _day_selected = "1";
var _week_selected = [];
var _curr_month = "currMonth";
var _curr_month_not = "currMonthNot";
var _prev_scroll_y = 0;

var _calendar_mode = "";
var _name_selected = "";
var _calendar_struct = {};
var user_contact_list;
var user_events_all = [];
var user_color = "rgba(114,138,255,0.5)";
var user_events_rep = [];
var member_events_all = [];
var member_color = "rgba(128,0,128,0.4)";
var member_check_ids = [];
var member_events_rep = [];
var freetimeChecked = false;
var timeout_mil = 20;
var hidden_color = "rgba(0, 0, 0, 0.3)";
var select_color = "rgb(214, 214, 216)";


/*
JS OUTLINE:
RESIZING
MODALS
CALENDAR
EVENTS
MAIN
*/


// -----------------------------------------------------------------
// RESIZING

function windowResized(){
	var breakpoint = getResponsiveBreakpoint();
	switch(breakpoint){
		case "xs":
			elongateHeader();
			abbreviateHeader_xs();
			break;
		case "sm":
			elongateHeader();
			abbreviateHeader();
			if(_switchType == "week" && _header_top_div != null){
				_header_top_div.style = "padding-left:28px;";
			}
			break;
		default:
			elongateHeader();
			if(_switchType == "week" && _header_top_div != null){
				_header_top_div.style = "padding-left:0px;";
			}
	}
	ensureBoxSize();
	clearEvents();
	addEvents();
}
function clickAnywhere(event){
	if(window.scrollY != 0){
		_prev_scroll_y = window.scrollY;
	}
	var clientX = event.clientX;
	var clientY = event.clientY;
	// Go through all divs and see which divs are affected
	var clicked_divs = [];
	for(var i = 0; i < eventDivArray.length; i++){
		var boundingRect = eventDivArray[i].getBoundingClientRect();
		if(clientX >= boundingRect.left && clientX <= boundingRect.right && clientY >= boundingRect.top && clientY <= boundingRect.bottom){
			clicked_divs.push(eventDivArray[i]);
		}
	}
	var clicked_ids = [];
	for(var i = 0; i < clicked_divs.length; i++){
		var curr_div = clicked_divs[i];
		var onclickattrib = curr_div.getAttribute("onclick");
		var firstPar = onclickattrib.indexOf("(");
		var lastPar = onclickattrib.indexOf(")");
		var temp_id = onclickattrib.substring(firstPar + 1, lastPar);
		if(temp_id == "-1"){
			continue;
		}
		var temp_cont = false;
		for(var j = 0; j < clicked_ids.length; j++){
			if(clicked_ids[j] == temp_id){
				temp_cont=true;
				break;
			}
		}
		if(temp_cont == false){
			clicked_ids.push(temp_id);
		}
	}
	var clicked_structs = [];
	var clicked_repeat = [];
	for(var i = 0; i < clicked_ids.length; i++){
		var curr_id = clicked_ids[i];
		var curr_struct = getEventStruct(curr_id);
		if(curr_struct.repeat == undefined){
			clicked_structs.push(curr_struct);
		}else{
			clicked_repeat.push(curr_struct);
		}
	}
	var clicked_combined = [];
	for(var i = 0; i < clicked_structs.length; i++){
		clicked_combined.push(clicked_structs[i]);
	}
	for(var i = 0; i < clicked_repeat.length; i++){
		clicked_combined.push(clicked_repeat[i]);
	}
	if(clicked_ids.length > 0){
		console.log("clicked_ids", clicked_ids);
	}

	if(clicked_combined.length > 0 && allModalsClosed() && allDropdownsClosed()){
		if(clicked_structs.length == 1 && clicked_repeat.length == 0){
			var temp_event_struct = clicked_structs[0];
			clickedViewSelect(temp_event_struct.event_id);
		}else if(clicked_repeat.length == 1 && clicked_structs.length == 0){
			var temp_event_repeat = clicked_repeat[0];
			clickedViewRepeatSelect(temp_event_repeat.event_id);
		}else{
			clearShowEvents();
			populateShowEvents(clicked_combined);
			showEventsModal();
		}
	}
}

function ensureBoxSize(){
	// console.log(calArray);
	switch(_switchType){
		case "month":
			// change height of each row to be the width of one column
			var curr_width;
			var dayBound = calArray[0][0].getBoundingClientRect();
			var rows = document.getElementsByClassName("calWeek");
			for(var i = 0; i < rows.length; i++){
				rows[i].style.height = dayBound.width 
				+ "px";
			}
			break;
		default:
	}
}
function getResponsiveBreakpoint() {
    var envs = ["xs", "sm", "md", "lg"];
    var env = "";

    var $el = $("<div>");
    $el.appendTo($("body"));

    for (var i = envs.length - 1; i >= 0; i--) {
        env = envs[i];
        $el.addClass("d-" + env + "-none");;
        if ($el.is(":hidden")) {
            break; // env detected
        }
    }
    $el.remove();
    return env;
}


// -----------------------------------------------------------------

// MODALS

function clearShowEvents(){
	var view_events_div = document.getElementById("viewEventsScrollCont");
	while(view_events_div.firstChild){
		view_events_div.removeChild(view_events_div.firstChild);
	}
}

function getEventCreatorFirebaseID(event_id){
	for(var i = 0; i < member_events_all.length; i++){
		var curr_event = member_events_all[i];
		if(curr_event.event_id == event_id){
			return curr_event.event_creator_firebase_id;
		}
	}
	for(var i = 0; i < user_events_all.length; i++){
		var curr_event = user_events_all[i];
		if(curr_event.event_id == event_id){
			return curr_event.event_creator_firebase_id;
		}
	}
	return null;
}

function getEventById(event_id){
	for(var i = 0; i < member_events_all.length; i++){
		var curr_event = member_events_all[i];
		if(curr_event.event_id == event_id){
			return curr_event;
		}
	}
	for(var i = 0; i < user_events_all.length; i++){
		var curr_event = user_events_all[i];
		if(curr_event.event_id == event_id){
			return curr_event;
		}
	}
	return null;
}

function populateViewSelect(event_id){
	var displayEventCreator = document.getElementById("displayEventCreator");
	var displayEventName = document.getElementById("displayEventName");
	var displayEventDescription = document.getElementById("displayEventDescription");
	var displayEventStart = document.getElementById("displayEventStart");
	var displayEventEnd = document.getElementById("displayEventEnd");
	var view_event = getEventById(event_id);
	// console.log("populate", view_event);
	displayEventCreator.innerText = "@" + view_event.event_creator_alias;
	displayEventCreator.setAttribute("href", "javascript:redir('redirfb/" + view_event.event_creator_firebase_id + "');");
	displayEventName.innerText = view_event.event_title;
	displayEventDescription.innerText = view_event.description;
	if(view_event.description == ""){
		displayEventDescription.innerText = "No description has been provided.";
		displayEventDescription.style.color = "grey";
	}
	var start_str = customDateString(new Date(view_event.start_date)) + " " + customTimeString(new Date(view_event.start_date));
	displayEventStart.innerText = start_str;
	var end_str = customDateString(new Date(view_event.end_date)) + " " + customTimeString(new Date(view_event.end_date));
	displayEventEnd.innerText = end_str;
}

function formatDateHTML(dateObj){
	return dateObj.getFullYear() + "-" + ('0' + (dateObj.getMonth() + 1)).slice(-2) + "-" + ('0' + dateObj.getDate()).slice(-2);
}

function formatTimeHTML(dateObj){
	var h = dateObj.getHours();
	var m = dateObj.getMinutes();
	if(h < 10){
		h = "0" + h;
	}
	if(m < 10){
		m = "0" + m;
	}
	return h + ":" + m;
}

function populateEditSelect(event_id){
	var edit_event_id = document.getElementById("id_EIediteventid");
	edit_event_id.value = event_id;
	var inputEditEventName = document.getElementById("inputEditEventName");
	var inputEditEventDesc = document.getElementById("inputEditEventDesc");
	var inputEditStartDate = document.getElementById("inputEditStartDate");
	var inputEditEndDate = document.getElementById("inputEditEndDate");
	var inputEditStartTime = document.getElementById("inputEditStartTime");
	var inputEditEndTime = document.getElementById("inputEditEndTime");
	var edit_event = getEventById(event_id);
	inputEditEventName.value = edit_event.event_title;
	inputEditEventDesc.value = edit_event.description;
	var startDateObj = new Date(edit_event.start_date);
	var startDateStr = formatDateHTML(startDateObj);
	inputEditStartDate.value = startDateStr;
	var endDateObj = new Date(edit_event.end_date);
	var endDateStr = formatDateHTML(endDateObj);
	inputEditEndDate.value = endDateStr;
	inputEditStartTime.value = formatTimeHTML(startDateObj);
	inputEditEndTime.value = formatTimeHTML(endDateObj);
}

function clickedViewSelect(event_id_clicked){
	closeAllModals();
	var fb_clicked = getEventCreatorFirebaseID(event_id_clicked);
	if(fb_clicked == _calendar_struct.calendar_data.user_info.firebase_id){
		populateEditSelect(event_id_clicked);
		var editSelectButton = document.getElementById("viewEditEventButton");
		editSelectButton.click();
	}else{
		populateViewSelect(event_id_clicked);
		var viewSelectButton = document.getElementById("viewSelectEventButton");
		viewSelectButton.click();
	}
}

function clickedViewRepeatSelect(event_id_clicked){
	closeAllModals();
	console.log("event_id_clicked", event_id_clicked);
	var fb_clicked = getRepeatEventCreatorFirebaseID(event_id_clicked);
	console.log("fb_clicked", fb_clicked);
	if(fb_clicked == _calendar_struct.calendar_data.user_info.firebase_id){
		populateEditRepeatSelect(event_id_clicked);
		var editSelectButton = document.getElementById("viewEditRepeatEventButton");
		editSelectButton.click();
	}else{
		populateViewRepeatSelect(event_id_clicked);
		var viewSelectButton = document.getElementById("viewSelectRepeatEventButton");
		viewSelectButton.click();
	}
}

function getRepeatEventCreatorFirebaseID(event_id){
	for(var i = 0; i < member_events_rep.length; i++){
		var curr_event = member_events_rep[i];
		if(curr_event.event_id == event_id){
			return curr_event.event_creator_firebase_id;
		}
	}
	for(var i = 0; i < user_events_rep.length; i++){
		var curr_event = user_events_rep[i];
		if(curr_event.event_id == event_id){
			return curr_event.event_creator_firebase_id;
		}
	}
	return null;
}

function getRepeatEventById(event_id){
	for(var i = 0; i < member_events_rep.length; i++){
		var curr_event = member_events_rep[i];
		if(curr_event.event_id == event_id){
			return curr_event;
		}
	}
	for(var i = 0; i < user_events_rep.length; i++){
		var curr_event = user_events_rep[i];
		if(curr_event.event_id == event_id){
			return curr_event;
		}
	}
	return null;
}


function populateEditRepeatSelect(event_id){
	var edit_event_id = document.getElementById("id_EIeditrepeateventid");
	edit_event_id.value = event_id;
	var inputEditEventName = document.getElementById("inputEditRepeatEventName");
	var inputEditEventDesc = document.getElementById("inputEditRepeatEventDesc");
	var inputEditStartDate = document.getElementById("inputEditRepeatStartDate");
	var inputEditEndDate = document.getElementById("inputEditRepeatEndDate");
	var inputEditStartTime = document.getElementById("inputEditRepeatStartTime");
	var inputEditEndTime = document.getElementById("inputEditRepeatEndTime");
	var edit_event = getRepeatEventById(event_id);
	inputEditEventName.value = edit_event.event_title;
	inputEditEventDesc.value = edit_event.description;
	var startDateObj = new Date(edit_event.start_date);
	var startDateStr = formatDateHTML(startDateObj);
	inputEditStartDate.value = startDateStr;
	var endDateObj = new Date(edit_event.end_date);
	var endDateStr = formatDateHTML(endDateObj);
	inputEditEndDate.value = endDateStr;
	inputEditStartTime.value = formatTimeHTML(startDateObj);
	inputEditEndTime.value = formatTimeHTML(endDateObj);
	var repeat_pattern = edit_event.week_arr;
	var week_arr = repeat_pattern.split('');
	var checkbox_divs = [];
	checkbox_divs.push(document.getElementById("checkEditSunday"));
	checkbox_divs.push(document.getElementById("checkEditMonday"));
	checkbox_divs.push(document.getElementById("checkEditTuesday"));
	checkbox_divs.push(document.getElementById("checkEditWednesday"));
	checkbox_divs.push(document.getElementById("checkEditThursday"));
	checkbox_divs.push(document.getElementById("checkEditFriday"));
	checkbox_divs.push(document.getElementById("checkEditSaturday"));
	for(var i = 0; i < week_arr.length; i++){
		if(week_arr[i] == "1"){
			if(checkbox_divs[i].checked == false){
				checkbox_divs[i].click();
			}
		}else{
			if(checkbox_divs[i].checked == true){
				checkbox_divs[i].click();
			}
		}
	}

}

function populateViewRepeatSelect(event_id){
	var displayEventCreator = document.getElementById("displayRepeatEventCreator");
	var displayEventName = document.getElementById("displayRepeatEventName");
	var displayEventDescription = document.getElementById("displayRepeatEventDescription");
	var displayEventStart = document.getElementById("displayRepeatEventStart");
	var displayEventEnd = document.getElementById("displayRepeatEventEnd");
	var displayRepeatEventPattern = document.getElementById("displayRepeatEventPattern");
	var view_event = getRepeatEventById(event_id);
	console.log("repeat:", event_id);
	// console.log("populate", view_event);
	displayEventCreator.innerText = "@" + view_event.event_creator_alias;
	displayEventCreator.setAttribute("href", "javascript:redir('redirfb/" + view_event.event_creator_firebase_id + "');");
	displayEventName.innerText = view_event.event_title;
	displayEventDescription.innerText = view_event.description;
	if(view_event.description == ""){
		displayEventDescription.innerText = "No description has been provided.";
		displayEventDescription.style.color = "grey";
	}
	var start_str = customDateString(new Date(view_event.start_date)) + " " + customTimeString(new Date(view_event.start_date));
	displayEventStart.innerText = start_str;
	var end_str = customDateString(new Date(view_event.end_date)) + " " + customTimeString(new Date(view_event.end_date));
	displayEventEnd.innerText = end_str;

	var repeat_pattern = view_event.week_arr;
	var week_arr = repeat_pattern.split('');
	var repeat_text = "";
	var repeat_days = [];
	for(var i = 0; i < week_arr.length; i++){
		if(week_arr[i] == 1){
			repeat_days.push(_days_of_week[i]);
		}
	}
	for(var i = 0; i < repeat_days.length; i++){
		repeat_text += repeat_days[i];
		if(i < repeat_days.length - 1){
			repeat_text += ", ";
		}
	}
	displayRepeatEventPattern.innerText = repeat_text;
}


function populateShowEvents(clicked_structs){
	var view_events_div = document.getElementById("viewEventsScrollCont");
	// console.log("populateShowEvents");
	for(var i = 0; i < clicked_structs.length; i++){
		var curr_struct = clicked_structs[i];
		var curr_elem = document.createElement("a");
		curr_elem.className = "dropdown-item";
		curr_elem.id = "ve_" + curr_struct.event_id;
		curr_elem.href = "#";
		if(curr_struct.repeat == undefined){
			curr_elem.setAttribute("onclick", "clickedViewSelect('" + curr_struct.event_id + "')"); 
		}else{
			curr_elem.setAttribute("onclick", "clickedViewRepeatSelect('" + curr_struct.event_id + "')"); 
		}
		var event_text_div = document.createElement("div");
		event_text_div.innerHTML = curr_struct.event_title;
		var event_creator_alias = firebaseIDtoAlias(curr_struct.event_creator_firebase_id);
		// console.log("populate:", curr_struct, "\nfirebase_id:", curr_struct.event_creator_firebase_id);
		// console.log("event_creator_alias:"+ event_creator_alias);
		event_text_div.innerHTML += "<br>@" + event_creator_alias;
		curr_elem.appendChild(event_text_div);
		view_events_div.appendChild(curr_elem);
	}
}

function showEventsModal(){
	var open_events = document.getElementById("viewEventsOpenButton");
	open_events.click();
}

function allModalsClosed(){
	var allModals = document.getElementsByClassName("modal");
	for(var i = 0; i < allModals.length; i++){
		var curr_modal = allModals[i];
		if(curr_modal.className.includes(" show")){
			return false;
		}
	}
	return true;
}

function allDropdownsClosed(){
	var allDropdowns = document.getElementsByClassName("dropdown-menu");
	for(var i = 0; i < allDropdowns.length; i++){
		var curr_dropdown = allDropdowns[i];
		if(curr_dropdown.className.includes(" show")){
			return false;
		}
	}
	return true;
}



// -----------------------------------------------------------------

// DRAW CALENDAR

var percentColors = [
    { pct: 0.0, color: { r: 0xff, g: 0x00, b: 0 } },
    { pct: 0.5, color: { r: 0xff, g: 0xff, b: 0 } },
    { pct: 1.0, color: { r: 0x00, g: 0xff, b: 0 } } ];

var getColorForPercentage = function(pct) {
    for (var i = 1; i < percentColors.length - 1; i++) {
        if (pct < percentColors[i].pct) {
            break;
        }
    }
    var lower = percentColors[i - 1];
    var upper = percentColors[i];
    var range = upper.pct - lower.pct;
    var rangePct = (pct - lower.pct) / range;
    var pctLower = 1 - rangePct;
    var pctUpper = rangePct;
    var color = {
        red: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
        green: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
        blue: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
    };
    return color;
    // or output as hex if preferred
}  
function convertEventListPooya(mike_structs){
	var retArray = [];
	for(var i = 0; i < mike_structs.length; i++){
		var curr_event = mike_structs[i];
		var new_struct = {};
		new_struct.start_date = Number(curr_event.start_date);
		new_struct.end_date = Number(curr_event.end_date);
		new_struct.participating_users = [];
		new_struct.event_id = Number(curr_event.event_id);
		retArray.push(new_struct);
	}
	return retArray;
}
function acuumulateDeltas(events_passed){
	var retNum = 0;
	for(var i = 0; i < events_passed.length; i++){
		var curr_delt = events_passed[i].end_date - events_passed[i].start_date;
		retNum += curr_delt;
	}
	return retNum;
}

function testDaysAffected(){
	var s1 = new Date(2019,3,5);
	s1.setHours(12,0,0);
	var e1 = new Date(2019,3,7);
	e1.setHours(15,0,0);
	var s2 = new Date(2019,3,8);
	s2.setHours(4,0,0);
	var e2 = new Date(2019,3,15);
	e2.setHours(17,0,0);
	var test_events = [
	{start_date:s1.getTime(), end_date:e1.getTime()}, 
	{start_date:s2.getTime(), end_date:e2.getTime()}
	];
	console.log(getEventsDays(test_events));

}

function getHoursAffected(event_passed){
	var daysAffected = getDaysAffected(event_passed);
	if(daysAffected.length == 1){
		return [(event_passed.end_date - event_passed.start_date)/1000/60/60];
	}
	var start_hours = daysAffected[1].getTime() - event_passed.start_date;
	var end_hours = event_passed.end_date - daysAffected[daysAffected.length - 1].getTime(); 
	var temp_array = [];
	temp_array.push(start_hours);
	for(var i = 1; i < daysAffected.length - 1; i++){
		temp_array.push(24*60*60*1000);
	}
	temp_array.push(end_hours);
	var retArray = [];
	for(var i = 0; i < temp_array.length; i++){
		var toAdd = temp_array[i]/1000/60/60;
		retArray.push(toAdd);
	}
	return retArray;
}

function getDaysAffected(event_passed){
	var start_date = new Date(event_passed.start_date);
	start_date.setHours(0,0,0);
	var end_date = new Date(event_passed.end_date);
	end_date.setDate(end_date.getDate() + 1);
	end_date.setHours(0,0,0);
	var retArray = [];
	var curr_date = new Date(start_date.getTime());
	do{
		retArray.push(new Date(curr_date.getTime()));
		curr_date.setDate(curr_date.getDate() + 1);
	}while(curr_date.getTime() < end_date.getTime());
	return retArray;
}

function getEventsDays(events){
	var freeArray = [];
	for(var i = 0; i < events.length; i++){
		var curr_event = events[i];
		var days_affected = getDaysAffected(curr_event);
		var hours_affected = getHoursAffected(curr_event);
		for(var j = 0; j < days_affected.length; j++){
			var contains = false;
			for(var k = 0; k < freeArray.length; k++){
				var curr_day_map = freeArray[k];
				if(curr_day_map.time == days_affected[j].getTime()){
					contains = true;
					curr_day_map.hours += hours_affected[j];
					break;
				}
			}
			if(contains == false){
				var temp_struct = {};
				temp_struct.time = days_affected[j].getTime();
				temp_struct.hours = hours_affected[j];
				freeArray.push(temp_struct);
			}
		}
	}
	var retArray = [];
	for(var i = 0; i < freeArray.length; i++){
		var temp_struct = freeArray[i];
		retArray.push({start_time:temp_struct.time, hours:Math.min(24, temp_struct.hours)});
	}
	return retArray;
}
function eventsSplitDays(events){
	var freeArray = [];
	for(var i = 0; i < events.length; i++){
		var curr_event = events[i];
		var days_affected = getDaysAffected(curr_event);
		var hours_affected = getHoursAffected(curr_event);
		for(var j = 0; j < days_affected.length; j++){
			var contains = false;
			for(var k = 0; k < freeArray.length; k++){
				var curr_day_map = freeArray[k];
				if(curr_day_map.time == days_affected[j].getTime()){
					contains = true;
					curr_day_map.hours += hours_affected[j];
					break;
				}
			}
			if(contains == false){
				var temp_struct = {};
				temp_struct.time = days_affected[j].getTime();
				temp_struct.hours = hours_affected[j];
				freeArray.push(temp_struct);
			}
		}
	}
	var retArray = [];
	for(var i = 0; i < freeArray.length; i++){
		var temp_struct = freeArray[i];
		retArray.push({start_time:temp_struct.time, hours:Math.min(24, temp_struct.hours)});
	}
	return retArray;
}
function eventHoursSplit(event_passed){
	var daysAffected = getDaysAffected(event_passed);
	if(daysAffected.length == 1){
		return [{end_date:Number(event_passed.end_date), start_date:Number(event_passed.start_date),
			event_id:event_passed.event_id}];
	}
	var start_hours = daysAffected[1].getTime() - event_passed.start_date;
	var end_day_start = new Date(event_passed.start_date);
	end_day_start.setHours(23,59,59);
	var start_struct = {start_date:Number(event_passed.start_date), end_date:end_day_start.getTime(),
		event_id:event_passed.event_id};
	var beg_day_end = new Date(event_passed.end_date);
	beg_day_end.setHours(0,0,0);
	var end_hours = event_passed.end_date - daysAffected[daysAffected.length - 1].getTime(); 
	var end_struct =  {start_date:beg_day_end.getTime(), end_date:Number(event_passed.end_date),
		event_id:event_passed.event_id};
	var temp_array = [];
	temp_array.push(start_struct);
	for(var i = 1; i < daysAffected.length - 1; i++){
		var temp_day_end = new Date(daysAffected[i].getTime());
		temp_day_end.setHours(23,59,59);
		var temp_struct = {start_date:daysAffected[i].getTime(), end_date:temp_day_end.getTime(),
			event_id:event_passed.event_id};
		temp_array.push(temp_struct);
	}
	temp_array.push(end_struct);
	return temp_array;
}
function testEventHoursSplit(){
	var s1 = new Date(Number("1555732800000"));
	var e1 = new Date(Number("1556078340000"));
	var temp_struct = {start_date:s1.getTime(), end_date:e1.getTime(), event_id:100};
	console.log(eventHoursSplit(temp_struct));
}

function testCombineEventsDayAffected(){
	var test1 = {
		start_date : new Date("April 4 2019 10:00 AM").getTime(),
		end_date : new Date("April 4 2019 3:00 PM").getTime()
	};
	var test2 = {
		start_date : new Date("April 4 2019 1:00 PM").getTime(),
		end_date : new Date("April 4 2019 5:00 PM").getTime()
	};
	var test3 = {
		start_date : new Date("April 5 2019 5:00 PM").getTime(),
		end_date : new Date("April 5 2019 10:00 PM").getTime()
	};
	var test4 = {
		start_date : new Date("April 5 2019 8:00 PM").getTime(),
		end_date : new Date("April 5 2019 11:00 PM").getTime()
	};
	var res = combineEventsDayAffected([test1, test2, test3, test4]);
	for(var i = 0; i < res.length; i++){
		var curr_struct = res[i];
		console.log(curr_struct.affected);
		for(var j = 0; j < curr_struct.events.length; j++){
			var curr_event = curr_struct.events[j];
			console.log("start", new Date(curr_event.start_date), "end", new Date(curr_event.end_date));
		}
	}
}

// Assumes already split using splitEventStructure(event)
function combineEventsDayAffected(event_arr_passed){
	var retArray = [];
	var dates_affected = [];
	for(var i = 0; i < event_arr_passed.length; i++){
		var curr_event = event_arr_passed[i];
		var date_affected = new Date(new Date(curr_event.start_date).setHours(0,0,0));
		var loc_contains = false;
		for(var j = 0; j < dates_affected.length; j++){
			if(dates_affected[j].getTime() == date_affected.getTime()){
				loc_contains = true;
				break;
			}
		}
		if(loc_contains == false){
			dates_affected.push(date_affected);
		}
	}
	for(var k=0; k < dates_affected.length; k++){
		var affected_array = [];
		for(var i = 0; i < event_arr_passed.length; i++){
			var curr_event = event_arr_passed[i];
			var date_affected = new Date(new Date(curr_event.start_date).setHours(0,0,0));
			if(date_affected.getTime() == dates_affected[k].getTime()){
				affected_array.push(curr_event);
			}
		}
		var tempDict = {};
		tempDict.affected = dates_affected[k];
		tempDict.events = affected_array;
		retArray.push(tempDict);
	}
	return retArray;
}

function unionEventsTwo(event1, event2){
	if(inRange(event1.start_date, event2.start_date, event1.end_date) ||
		inRange(event1.start_date, event2.end_date, event1.end_date)
		|| inRange(event2.start_date, event1.start_date, event2.end_date) ||
		inRange(event2.start_date, event1.end_date, event2.end_date)){
		var unionedEvent = {};
		unionedEvent.start_date = Math.min(event1.start_date, event2.start_date);
		unionedEvent.end_date = Math.max(event1.end_date, event2.end_date);
		return [unionedEvent];
	}else{
		return [event1, event2];
	}
}

function testUnionEvents(){
	var test1 = {
		start_date : new Date("April 4 2019 10:00 AM").getTime(),
		end_date : new Date("April 4 2019 3:00 PM").getTime()
	};
	var test2 = {
		start_date : new Date("April 4 2019 1:00 PM").getTime(),
		end_date : new Date("April 4 2019 5:00 PM").getTime()
	};
	var test3 = {
		start_date : new Date("April 4 2019 5:00 PM").getTime(),
		end_date : new Date("April 4 2019 10:00 PM").getTime()
	};
	var test4 = {
		start_date : new Date("April 4 2019 8:00 PM").getTime(),
		end_date : new Date("April 4 2019 11:00 PM").getTime()
	};
	var res = unionEvents([test1, test2, test3, test4]);
	for(var i = 0; i < res.length; i++){
		console.log("start", new Date(res[i].start_date), "end", new Date(res[i].end_date));
	}
}

// Creates a convex hull in one dimension
function unionEvents(event_arr_passed){
	var allOne = false;
	var deep_clone = [];
	for(var i = 0; i < event_arr_passed.length; i++){
		var curr_event = event_arr_passed[i];
		var cloned = {};
		cloned.start_date = curr_event.start_date;
		cloned.end_date = curr_event.end_date;
		deep_clone.push(cloned);
	}
	while(allOne == false){
		var forAll = true;
		for(var i =0; i < deep_clone.length; i++){
			var curr_event = deep_clone[i];
			for(var j=0; j < deep_clone.length; j++){
				// Don't union with self
				if(i == j){
					break;
				}
				var postUnion = unionEventsTwo(curr_event, deep_clone[j]);
				if(postUnion.length == 2){
					forAll &= true;
					continue;
				}else{
					deep_clone.splice(i, 1);
					deep_clone.splice(j, 1);
					deep_clone.push(postUnion[0]);
					forAll = false;
					continue;
				}

			}
		}
		allOne = forAll;
	}
	return deep_clone;
}


function testUnionDaysAffected(){
	var test2 = {
		start_date : new Date("April 17 2019 12:00 AM").getTime(),
		end_date : new Date("April 17 2019 11:59 PM").getTime()
	};
	var test1 = {
		start_date : new Date("April 17 2019 11:00 AM").getTime(),
		end_date : new Date("April 17 2019 12:00 PM").getTime()
	};
	var res = unionEventsTwo(test1, test2);
	for(var i = 0; i < res.length; i++){
		console.log("start", new Date(res[i].start_date), "end", new Date(res[i].end_date));
	}
}

// Assumes events passed are already split
function unionDaysAffected(event_arr_passed){
	var retArray = [];
	var combinedDaysAffected = combineEventsDayAffected(event_arr_passed);
	for(var i = 0; i < combinedDaysAffected.length; i++){
		var curr_struct = combinedDaysAffected[i];
		var unioned_day = unionEvents(curr_struct.events);
		for(var j = 0; j < unioned_day.length; j++){
			// console.log("start", new Date(unioned_day[j].start_date), "end", new Date(unioned_day[j].end_date));
			unioned_day[j].reg_date = new Date(unioned_day[j].start_date);
			unioned_day[j].delta = Math.abs(unioned_day[j].end_date - unioned_day[j].start_date)/(1000*60*60);
			retArray.push(unioned_day[j]);
		}
	}
	return retArray;
}


function combinedFreeToHours(combined_free, month_start, month_end){
	var retArray = [];
	// Populate retarray with basic structures
	for(var currDate = new Date(month_start.getTime());
		currDate.getTime() <= month_end.getTime();
		currDate = new Date(new Date(currDate.getTime()).setDate(currDate.getDate() + 1))
		){
		var currStruct = {};
		currStruct.date = new Date(currDate.getTime());
		currStruct.hours = 0;
		retArray.push(currStruct);
	}
	for(var i = 0; i < combined_free.length; i++){
		var currFree = combined_free[i];
		var curr_split = splitEventStructure(combined_free[i]);
		// console.log("curr_split:",curr_split);
		for(var j = 0; j < curr_split.length; j++){
			// console.log("j:" + j,"start_date", new Date(curr_split[j].start_date), "end_date", new Date(curr_split[j].end_date));
			var delta_h = Math.abs(curr_split[j].end_date - curr_split[j].start_date)/(1000*60*60);
			// console.log("delta_h", delta_h);
			var date_affected = new Date(new Date(curr_split[j].start_date).setHours(0,0,0));
			// console.log("date_affected", date_affected);
			var temp_hours = 0;
			var index_found = -1;
			for(var k = 0; k < retArray.length; k++){
				if(retArray[k].date.getTime() == date_affected.getTime()){
					temp_hours += delta_h;
					index_found = k;
					break;
				}
			}
			if(index_found != -1){
				retArray[index_found].hours += temp_hours;
			}
			// console.log(delta_h);
		}
	}
	// for(var i = 0; i < retArray.length; i++){
	// 	retArray[i].hours %= 24;
	// }
	// console.log("combined_free", retArray);
	return retArray;
}

function drawColorGrid(isRainbow) {
	var retArray = [];
	if(_switchType != "month"){
		return retArray;
	}
	var member_events = getMembersSelectedEvents();
	var combinedEvents = [];
	for(var i = 0; i < user_events_all.length; i++){
		combinedEvents.push(user_events_all[i]);
	}
	for(var i = 0; i < member_events.length; i++){
		combinedEvents.push(member_events[i]);
	}
	combinedEvents = combinedEvents.sort(function(a,b){return a.start_date - b.start_date});
	var temp_convert_split = [];

	for(var i = 0; i < combinedEvents.length; i++){
		var sub_array = splitEventStructure(combinedEvents[i]);
		for(var j = 0; j < sub_array.length; j++){
			sub_array[j].event_id = combinedEvents[i].event_id;
			temp_convert_split.push(sub_array[j]);
		}
	}
	// console.log("temp_convert_split", temp_convert_split);
	var combined_affected = combineEventsDayAffected(temp_convert_split);
	// console.log("combined_affected", combined_affected);
	var unioned_split = unionDaysAffected(temp_convert_split);
	// console.log("unioned_split", unioned_split);
	// for(var i = 0; i < unioned_split.length; i++){
	// 	console.log("start", new Date(unioned_split[i].start_date), "end", new Date(unioned_split[i].end_date));
	// }
	// console.log("temp_convert_split", temp_convert_split);
	var month_start = new Date(_year_selected, _month_selected, 1);
	var month_end = new Date(_year_selected, _month_selected + 1, 0);
	month_end = new Date(month_end.setHours(23,59,59));
	var temp_cal = new Calendar("temp_cal");
	var freetimeArray = temp_cal.freetime_per_day(unioned_split, month_start.getTime(), month_end.getTime());
	var combined_free = [];

	// console.log("freetimeArray", freetimeArray);
	for(var i = 0; i < freetimeArray.length; i++){
		var curr_arr = freetimeArray[i];
		if(curr_arr != null){
			// console.log("non null");
			for(var j = 0; j < curr_arr.length; j++){
				// console.log(curr_arr);
				if(curr_arr[j].end_date == 99999999999999){
					// CRASHES AT 99999999999999
					var temp_end = new Date(month_end.getTime() + 5*1000*24*60*60);
					curr_arr[j].end_date = temp_end.getTime();
				}
				combined_free.push(curr_arr[j]);
			}
		}
	}			
	// console.log("combinedFree", combined_free);
	// console.log("month_start", month_start, "month_end", month_end);
	var hours_temp = combinedFreeToHours(combined_free, month_start, month_end);
	// console.log("hours_temp", hours_temp);
	var count = 0;
	for(var i = 0; i < calArray.length; i++){
		for(var j = 0; j < calArray[i].length; j++){
			var curr_elem = calArray[i][j];
			if(curr_elem.className.includes(_curr_month_not)){
				continue;
			}
			var month_day = Number(curr_elem.innerText);
			var temp_date = new Date(_year_selected, _month_selected, month_day);
			temp_date = temp_date.setHours(0,0,0);
			var hoursFree = 24;
			// console.log(temp_date);
			for(var k = 0; k < hours_temp.length; k++){
				// console.log(eventsHours[k]);
				if(temp_date == hours_temp[k].date.getTime()){
					// console.log("FOUND");
					// console.log("temp_date", temp_date, "hours_temp[k]", hours_temp[k]);
					hoursFree = hours_temp[k].hours;
					if(hoursFree > 23){
						for(var L = 0; L < unioned_split.length; L++){
							var curr_un = unioned_split[L];
							if(Number(temp_date) == new Date(curr_un.reg_date.getTime()).setHours(0,0,0)){
								if(curr_un.delta > 23){
									hoursFree = 24 - curr_un.delta;
									break;
								}
							}
						}
					}
					break;
				}
			}
			// console.log("hours free:", hoursFree);
			var hoursOcc = 24 - hoursFree;
			var alpha = 0;
			if(hoursFree < 8){
				alpha = 0;
			}else{
				alpha = (hoursFree - 8)/16;
			}
			if(getEventsCurrMonthUser().length == 0 && getEventsCurrMonthSelected().length == 0){
				alpha = 1;
			}

			var randColor = getColorForPercentage(alpha);
			curr_elem.style.backgroundColor =  
				"rgba(" + randColor.red + ", " + randColor.green + ", " 
				+ randColor.blue + ", 0.2)";
			retArray.push(curr_elem);
			count += 1;
		}
	}
	return retArray;
}

function clickUserEvent(event_id_clicked){
	if(_redirecting){
		// console.log("redirecting, no action");
		return;
	}
	// console.log("all good!");
	clickedViewSelect(event_id_clicked);
}

function clickUserRepeatEvent(event_id_clicked){
	if(_redirecting){
		// console.log("redirecting, no action");
		return;
	}
	// console.log("all good!");
	clickedViewRepeatSelect(event_id_clicked);
}

function clickFreetime(start_end_date){
	console.log("clickFreetime");
	var create_event_button = document.getElementById("createNewEventButton");
	create_event_button.click();
	var start_end_arr = start_end_date.split("$");
	var start_date = start_end_arr[0];
	var end_date = start_end_arr[1];
	console.log(start_date, end_date);
	var enter_start_date = document.getElementById("inputStartDate");
	var enter_start_time = document.getElementById("inputStartTime");
	var enter_end_date = document.getElementById("inputEndDate");
	var enter_end_time = document.getElementById("inputEndTime");
	var startDateObj = new Date(parseInt(start_date));
	var startDateStr = formatDateHTML(startDateObj);
	enter_start_date.value = startDateStr;
	var endDateObj = new Date(parseInt(end_date));
	var endDateStr = formatDateHTML(endDateObj);
	enter_end_date.value = endDateStr;
	enter_start_time.value = formatTimeHTML(startDateObj);
	enter_end_time.value = formatTimeHTML(endDateObj);
	// closeAllModals();
	console.log(startDateObj, endDateObj);
	console.log(create_event_button);
	console.log(enter_start_date, enter_start_time, enter_end_date, enter_end_time);
}


function makeList(cont_id){
	// console.log("makeList");
	clearEvents();
	// Make actual list div
	var cont_div = document.getElementById(cont_id);
	while (cont_div.hasChildNodes()) {
	    cont_div.removeChild(cont_div.lastChild);
	}
	var list_div = document.createElement("div");
	// <ul class="nav nav-pills nav-stacked" id="height_list">
	var sub_list = document.createElement("ul");
	sub_list.className = "nav nav-pills nav-stacked";
	sub_list.style.overflowY = "scroll";
	sub_list.style.height = "500px";
	sub_list.style.border = "black";
	sub_list.style.borderStyle = "solid";
	sub_list.style.borderWidth = "1px";
	// Freetime not checked.
	var createFuncEvent = function(external_div, arr, i){
		var list_elem = document.createElement('li');
		list_elem.className = "nav-item";
		list_elem.style.width = "100%";
		var a_elem = document.createElement('a');
		a_elem.className = "navbar-text calListDiv";
		if(arr[i].repeat == undefined){
			a_elem.setAttribute("onclick", "clickUserEvent('" + arr[i].event_id + "');");
		}else{
			a_elem.setAttribute("onclick", "clickUserRepeatEvent('" + arr[i].event_id + "');");
		}
		a_elem.innerHTML = arr[i].event_title  + "<br>";
		var event_creator_alias = firebaseIDtoAlias(arr[i].event_creator_firebase_id);
		var alias_elem = document.createElement('a');
		alias_elem.innerText = "@" + event_creator_alias;
		alias_elem.href = "javascript:redir('redirfb/" + arr[i].event_creator_firebase_id + "');";
		alias_elem.setAttribute("onclick", "_redirecting = true;");
		a_elem.appendChild(alias_elem);
		var temp_date_time = new Date(Number(arr[i].start_date));
		var date_string_start = customDateString(temp_date_time);
		var time_string_start = customTimeString(temp_date_time);
		a_elem.innerHTML += " <br> " + date_string_start + "  " + time_string_start;
		temp_date_time = new Date(Number(arr[i].end_date));
		var date_string_end = customDateString(temp_date_time);
		var time_string_end = customTimeString(temp_date_time);
		a_elem.innerHTML += " - " + date_string_end + "  " + time_string_end;
		a_elem.style.width = "100%";
		a_elem.style.borderBottom = "1px solid grey";
		a_elem.style.paddingLeft = "20px";
		list_elem.appendChild(a_elem);
		external_div.appendChild(list_elem);
	};
	var createFuncFree = function(external_div, arr, i){
		var list_elem = document.createElement('li');
		list_elem.className = "nav-item calListDiv";
		list_elem.style.width = "100%";
		var a_elem = document.createElement('a');
		a_elem.className = "navbar-text";
		a_elem.innerHTML =  "Freetime <br>";
		var s_e_string = arr[i].start_date + "$" + arr[i].end_date;
		a_elem.setAttribute("onclick", "clickFreetime('" + s_e_string + "');");
		var temp_date_time = new Date(Number(arr[i].start_date));
		var date_string_start = customDateString(temp_date_time);
		var time_string_start = customTimeString(temp_date_time);
		a_elem.innerHTML += date_string_start + "  " + time_string_start;
		temp_date_time = new Date(Number(arr[i].end_date));
		var date_string_end = customDateString(temp_date_time);
		var time_string_end = customTimeString(temp_date_time);
		a_elem.innerHTML += " - " + date_string_end + "  " + time_string_end;
		a_elem.style.width = "100%";
		a_elem.style.borderBottom = "1px solid grey";
		a_elem.style.paddingLeft = "20px";
		list_elem.appendChild(a_elem);
		external_div.appendChild(list_elem);
	};
	var selected_events = getMembersSelectedEvents();
	var combinedEvents = [];
	for(var i = 0; i < user_events_all.length; i++){
		combinedEvents.push(user_events_all[i]);
	}
	for(var i = 0; i < selected_events.length; i++){
		combinedEvents.push(selected_events[i]);
	}
	combinedEvents.sort(function(a, b){return a.start_date - b.start_date});
	if(combinedEvents.length > 0){
		if(freetimeChecked == false){
			for(var i = 0; i < combinedEvents.length; i++){
				if(combinedEvents[i].isHidden != undefined && combinedEvents[i].isHidden){
					continue;
				}
				createFuncEvent(sub_list, combinedEvents, i);
			}
		}else{
			// Get freetime of all people

			var pooya_array = convertEventListPooya(combinedEvents);
			// console.log("pooya_array", pooya_array);
			
			var month_start = new Date(new Date(_year_selected, _month_selected, _day_selected).setHours(0,0,0));
			var month_end = new Date(new Date(month_start.getTime()).setMonth(month_start.getMonth() + 1));
			console.log("makeList free", pooya_array);
			console.log(month_start, month_end);
			if(month_start.getDate() > month_end.getDate()){
				month_start = new Date(new Date(_year_selected, _month_selected, 1).setHours(0,0,0));
			}
			combinedEvents = combinedEvents.sort(function(a,b){return a.start_date - b.start_date});
			var temp_convert_split = [];

			for(var i = 0; i < combinedEvents.length; i++){
				var sub_array = splitEventStructure(combinedEvents[i]);
				for(var j = 0; j < sub_array.length; j++){
					sub_array[j].event_id = combinedEvents[i].event_id;
					temp_convert_split.push(sub_array[j]);
				}
			}
			var unioned_split = unionDaysAffected(temp_convert_split);
			console.log("unioned_split", unioned_split);
			var temp_cal = new Calendar("temp_cal");
			var freetimeArray = temp_cal.freetime_per_day(unioned_split, month_start.getTime(), month_end.getTime());
			var combined_free = [];
			console.log(freetimeArray);
			var forAllNull = true;
			for (var i = 0; i < freetimeArray.length; i++) {
				var curr_free = freetimeArray[i];
				if(curr_free != null){
					forAllNull = false;
					break;
				}
			}
			for(var i = 0; i < freetimeArray.length; i++){
				var curr_arr = freetimeArray[i];
				if(forAllNull){
					// create new freetime event;
					var curr_ev_new = {};
					curr_ev_new.start_date = new Date(new Date(month_start.getTime()).setHours(0,0,0)).setDate(month_start.getDate() + i);
					curr_ev_new.end_date = new Date(new Date(month_start.getTime()).setHours(23,59,59)).setDate(month_start.getDate() + i);
					curr_arr = [curr_ev_new];
					combined_free.push(curr_ev_new);
				}else if (curr_arr != null){
					// console.log("non null");
					for(var j = 0; j < curr_arr.length; j++){
						// console.log(curr_arr);
						var start_date_obj = new Date(curr_arr[j].start_date);
						if( start_date_obj.getHours() == 23 && start_date_obj.getMinutes() == 59){
							curr_arr[j].start_date = new Date(new Date(curr_arr[j].start_date).setDate(start_date_obj.getDate() + 1)).setHours(0,0,0);
							// console.log("Set equals", curr_arr[j], new Date(curr_arr[j].start_date), start_date_obj);
						}
						var end_date_obj = new Date(curr_arr[j].end_date);
						if(curr_arr[j].end_date == new Date(curr_arr[j].end_date).setHours(0,0,0)){
							curr_arr[j].end_date = new Date(new Date(curr_arr[j].end_date).setDate(end_date_obj.getDate() - 1)).setHours(23,59,0);
							// console.log("Set equals", curr_arr[j], new Date(curr_arr[j].end_date), end_date_obj);
						}
						if(curr_arr[j].end_date - curr_arr[j].start_date > 600000 && curr_arr[j].end_date > curr_arr[j].start_date){
							curr_arr[j].delta = (curr_arr[j].end_date - curr_arr[j].start_date)/(600000);
							curr_arr[j].start_date_obj = new Date(curr_arr[j].start_date);
							combined_free.push(curr_arr[j]);
						}
					}
				}
			}
			console.log(combined_free);
			for(var i = 0; i < combined_free.length; i++){
				createFuncFree(sub_list, combined_free, i);
			}
		}
	
	}
	// list_div.style.height = "100%";
	list_div.style.width = "100%";
	list_div.appendChild(sub_list);
	cont_div.appendChild(list_div);
	addEvents();
}

function makeGrid(cont_id, rowClass, colClass, name, dim_x, dim_y, onclick_func, generateTopHeader_func, generateSideHeader_func){
	var cont_div = document.getElementById(cont_id);
	var children = cont_div.childNodes;
	x_offset = (generateSideHeader_func(0) == null ? 0 : 1);
	y_offset = (generateTopHeader_func(0) == null ? 0 : 1);
	while (cont_div.hasChildNodes()) {
	    cont_div.removeChild(cont_div.lastChild);
	}
	gridArray = [];
	calArray = [];
	headerArray_top = [];
	headerArray_side = [];
	divRowsArray = [];
	clearEvents();
	var top_row = document.createElement('div');
	top_row.className = "row";
	var row_array = [];
	if(generateSideHeader_func(0) != null){
		var padding = document.createElement('div');
		padding.className = "col-1";
		top_row.appendChild(padding);
		row_array.push(padding);
	}

	for (var i = 0; i < dim_x; i++) {
		var curr_col = generateTopHeader_func(i);
		top_row.appendChild(curr_col);
		headerArray_top.push(curr_col);
		row_array.push(curr_col);
	}
	_header_top_div = top_row;
	cont_div.appendChild(top_row);
	gridArray.push(row_array);
	for(var i=0; i< dim_y; i++){
		var curr_row = document.createElement('div');
		var col_wrapper = document.createElement('div');
		col_wrapper.id = "wrapper_r:" + i;
		curr_row.className = "row " + rowClass;
		curr_row.id = rowClass + "_r" + i;
		row_array = [];
		var cal_row = [];
		var side_header = generateSideHeader_func(i);
		if(side_header != null){
			curr_row.appendChild(side_header);
			headerArray_side.push(side_header);
			row_array.push(side_header);
		}
		for(var j=0; j < dim_x; j++){
			var curr_col = document.createElement('div');
			curr_col.className = "col " + colClass;
			curr_col.id = name + "_r:" + i + ",c:"+  j; 
			curr_col.onclick = function(){
				onclick_func(this.id);
			};
			curr_row.appendChild(curr_col);
			row_array.push(curr_col);
			cal_row.push(curr_col);
		}
		col_wrapper.appendChild(curr_row);
		cont_div.appendChild(col_wrapper);
		gridArray.push(row_array);
		calArray.push(cal_row);
		divRowsArray.push(curr_row);
	}
	// console.log(gridArray);
	windowResized();
	addEvents();	
	if(_prev_scroll_y != 0){
		window.scrollTo(0, _prev_scroll_y);
	}
}

function switchCalendarView(cont_id, switchType){
	var cont_div = document.getElementById(cont_id);
	cont_div.innerHTML = "";
	if(window.scrollY != 0){
		_prev_scroll_y = window.scrollY;
		// console.log("scroll_y", _prev_scroll_y);
	}
	_switchType = switchType;
	clearEvents();
	switch(switchType){
		case "list":
			makeList(cont_id);
			break;
		case "day":
			makeGrid(cont_id, "calDayD", "defStyle calHour", "D", 1, 24, hourClickD, dayTopHeader, hourLeftHeader);
			break;
		case "week":
			makeGrid(cont_id, "calDayW", "defStyle calHour", "W", 7, 24, hourClickW, weekDatesHeader, hourLeftHeader);
			break;
		case "month":
		default:
			makeGrid(cont_id, "calWeek", "defStyle calDay", "M", 7, 6, dayClickM, weekDaysHeader, noLeftHeader);
			fillMonthViewNumbers();
			if(freetimeChecked){
				drawColorGrid(freetimeChecked);
			}
		}
	smoothScrollTo();
	
}
function smoothScrollTo(){
	window.setTimeout(
		function(){window.scrollTo({
			top: _prev_scroll_y,
			left: 0,
			behavior: 'smooth'
			});}, 100);
}

function clearEvents(){
	for(var i = 0; i < eventDivArray.length; i++){
		var curr_event = eventDivArray[i];
		curr_event.parentElement.removeChild(curr_event);
	}
	eventDivArray = [];
}
function splitEvent(start, end){
	var start_week = getWeek(start);
	var end_week = getWeek(end);
	var dw = end_week - start_week;
	var retStruct = {range:[],flags:[]};
	if(start_week == end_week){
		retStruct.range = [start, end];
		retStruct.flags = [];
		return [retStruct];
	}
	var retArr = [];
	var curr_start = start;
	for(var week_index = start_week; week_index <= end_week; week_index++){
		var end_of_week = (week_index + 1)*7 - 1;
		retStruct = {range:[],flags:[]};
		if(curr_start != start){
			retStruct.flags.push("l");
		}
		// < && != end
		if(end_of_week < end){
			retStruct.flags.push("r");
			retStruct.range=[curr_start, end_of_week];
		}
		if(end <= end_of_week){
			retStruct.range=[curr_start, end];
		}
		curr_start = (week_index + 1)*7;
		retArr.push(retStruct);
	}
	return retArr;
}

function aliasToFirebaseID(alias){
	if(alias == _calendar_struct.calendar_data.user_info.alias){
		return _calendar_struct.calendar_data.user_info.firebase_id;
	}
	var temp_member_info = _calendar_struct.calendar_data.member_info;
	// console.log("temp_member_info", temp_member_info);
	for(var i = 0; i < temp_member_info.length; i++){
		var curr_member_info = temp_member_info[i];
		// console.log("curr_member_info", curr_member_info);
		if(alias == curr_member_info.alias){
			// console.log("MATCH");
			return temp_member_info[i].firebase_id;
		}
	}
}

function firebaseIDtoAlias(firebase_id){
	if(firebase_id == _calendar_struct.calendar_data.user_info.firebase_id){
		return _calendar_struct.calendar_data.user_info.alias;
	}
	var temp_member_info = _calendar_struct.calendar_data.member_info;
	for(var i = 0; i < temp_member_info.length; i++){
		if(firebase_id == temp_member_info[i].firebase_id){
			return temp_member_info[i].alias;
		}
	}
}

function filterAlias(array, alias){
	var filtered = [];
	for(var i = 0; i < array.length; i++){
		var curr = array[i];
		if(curr.event_creator_alias == alias){
			filtered.push(curr);
		}
	}
	return filtered;
}
function filterAliasArray(event_array, alias_array){
	var retArray = [];
	for(var i = 0; i < alias_array.length; i++){
		var temp_firebase_id = aliasToFirebaseID(alias_array[i]);
		var curr_filtered = filterEventsFirebaseID(event_array, temp_firebase_id);
		for(var j = 0; j < curr_filtered.length; j++){
			retArray.push(curr_filtered[j]);
		}
	}
	return retArray;
}

function filterEventsFirebaseID(array, firebase_id){
	var firebase_events = _calendar_struct.calendar_data.member_events;
	var temp_events_all = [];
	for(var i =0; i < firebase_events.length; i++){
		if(firebase_events[i].firebase_id == firebase_id){
			temp_events_all = firebase_events[i].participating_events;
			break;
		}
	}
	var retArray = [];
	for(var i = 0; i < temp_events_all.length; i++){
		for(var j = 0; j < array.length; j++){
			if(temp_events_all[i].event_id == array[j].event_id){
				retArray.push(array[j]);
			}
		}
	}
	return retArray;
}

function getAllEventStructsCurrMonthAlias(alias){
	var allCurr = getAllEventStructsCurrMonth();
	var firebase_id = aliasToFirebaseID(alias);
	return filterEventsFirebaseID(allCurr, firebase_id);
}
function getAllEventStructsCurrMonth(){
	var retArr = [];
	var month_start = new Date(_year_selected, _month_selected, 1);
	month_start.setHours(0,0,0);
	var start_unix = month_start.getTime();
	var month_end = new Date(_year_selected, _month_selected + 1, 0);
	month_end.setHours(23,59,59);
	var end_unix = month_end.getTime();
	for(var i = 0; i < user_events_all.length; i++){
		var curr_event = user_events_all[i];
		if((curr_event.start_date >= start_unix  &&curr_event.start_date <= end_unix) || 
			(curr_event.end_date <= end_unix && curr_event.end_date >= end_unix)){
			retArr.push(curr_event);
		}
	}
	for(var i = 0; i < member_events_all.length; i++){
		var curr_event = member_events_all[i];
		if((curr_event.start_date >= start_unix  &&curr_event.start_date <= end_unix) || 
			(curr_event.end_date <= end_unix && curr_event.end_date >= end_unix)){
			retArr.push(curr_event);
		}
	}
	return retArr;
}
function inRange(start, test, end){
	var retBool = (test >= start && test <= end);
	return retBool;
}

function getEventsCurrMonth(){
	var retArr = [];
	var all_selected = getEventsCurrMonthSelected();
	var all_user = getEventsCurrMonthUser();
	var month_start = new Date(_year_selected, _month_selected, 1);
	month_start = new Date(month_start.setHours(0,0,0));
	var start_unix = month_start.getTime();
	var month_end = new Date(_year_selected, _month_selected + 1, 0);
	month_end = new Date(month_end.setHours(23,59,59));
	var end_unix = month_end.getTime();
	// console.log(month_start, month_end);
	var populated_month = [];
	for(var i = 0; i < populatedEvents.length; i++){
		var curr_event = populatedEvents[i].event_object;
		if(inRange(start_unix, curr_event.start_date, end_unix) || 
			inRange(start_unix, curr_event.end_date, end_unix)){
			populated_month.push(populatedEvents[i]);
		}
	}
	for(var i = 0; i < populated_month.length; i++){
		var curr_event = populated_month[i].event_object;
		var member_cont = false;
		for(var j = 0; j < all_selected.length; j++){
			if(all_selected[j].event_id == curr_event.event_id){
				member_cont = true;
				break;
			}
		}
		var user_cont = false;
		for(var j = 0; j < all_user.length; j++){
			if(all_user[j].event_id == curr_event.event_id){
				user_cont = true;
				break;
			}
		}
		if(member_cont == false && user_cont == false){
			continue;
		}
		retArr.push(populated_month[i]);
	}
	return retArr;
}

function getEventsCurrMonthUser(){
	var retArr = [];
	var month_start = new Date(_year_selected, _month_selected, 1);
	month_start.setHours(0,0,0);
	var start_unix = month_start.getTime();
	var month_end = new Date(_year_selected, _month_selected + 1, 0);
	month_end.setHours(23,59,59);
	var end_unix = month_end.getTime();
	for(var i = 0; i < user_events_all.length; i++){
		var curr_event = user_events_all[i];
		if(inRange(start_unix, curr_event.start_date, end_unix) || 
			inRange(start_unix, curr_event.end_date, end_unix)){
			retArr.push(user_events_all[i]);
		}
	}
	return retArr;
}
function getEventsCurrMonthMembers(){
	var retArr = [];
	var month_start = new Date(_year_selected, _month_selected, 1);
	month_start.setHours(0,0,0);
	var start_unix = month_start.getTime();
	var month_end = new Date(_year_selected, _month_selected + 1, 0);
	month_end.setHours(23,59,59);
	var end_unix = month_end.getTime();
	for(var i = 0; i < member_events_all.length; i++){
		var curr_event = member_events_all[i];
		if(inRange(start_unix, curr_event.start_date, end_unix) || 
			inRange(start_unix, curr_event.end_date, end_unix)){
			retArr.push(member_events_all[i]);
		}
	}
	return retArr;
}

function getEventsCurrMonthSelected(){
	// console.log("getEventsCurrMonthSelected");
	var selected_members = getMembersSelected();
	// console.log(selected_members);
	if(selected_members.length == 0){
		return [];
	}
	var curr_month_members = getEventsCurrMonthMembers();
	var retArray = [];
	for(var i = 0; i < curr_month_members.length; i++){
		if(selected_members.includes(curr_month_members[i].event_creator_alias)){
			retArray.push(curr_month_members[i]);
		}
	}
	// var retArray = filterAliasArray(curr_month_members, selected_members);
	return retArray;
}


function getEventsCurrWeekUser(){
	var retArr = [];
	for(var i= 0; i < user_events.length; i++){
		var curr_event = user_events[i];
		if(inRange(_week_selected[0].getTime(), curr_event.start_date, _week_selected[1].getTime())
			|| inRange(_week_selected[0].getTime(), curr_event.end_date, _week_selected[1].getTime())){
			retArr.push(curr_event);
		}
	}
	return retArr;
}

function getEventsCurrWeekMembers(){
	var retArr = [];
	for(var i= 0; i < member_events_all.length; i++){
		var curr_event = member_events_all[i];
		if(inRange(_week_selected[0].getTime(), curr_event.start_date, _week_selected[1].getTime())
			|| inRange(_week_selected[0].getTime(), curr_event.end_date, _week_selected[1].getTime())){
			retArr.push(curr_event);
		}
	}
	return retArr;
}

function getEventsCurrWeek(){
	var retArr = [];
	var all_selected = getMembersSelectedEvents();
	for(var i= 0; i < populatedEvents_w.length; i++){
		var curr_event = populatedEvents_w[i].event_object;
		var mem_cont = false;
		for(var j = 0; j < all_selected.length; j++){
			if(all_selected[j].event_id == curr_event.event_id){
				mem_cont = true;
				break;
			}
		}
		var user_cont = false;
		for(var j = 0; j < user_events_all.length; j++){
			if(user_events_all[j].event_id == curr_event.event_id){
				user_cont = true;
				break;
			}
		}
		if(mem_cont == false && user_cont == false){
			continue;
		}
		if(inRange(_week_selected[0].getTime(), curr_event.start_date, _week_selected[1].getTime())
			|| inRange(_week_selected[0].getTime(), curr_event.end_date, _week_selected[1].getTime())){
			retArr.push(populatedEvents_w[i]);
		}
	}
	return retArr;
}
function getEventsOnDate(date_obj){
	var beginning_day = new Date(date_obj.getFullYear(), date_obj.getMonth(), date_obj.getDate());
	var end_day = new Date(date_obj.getFullYear(), date_obj.getMonth(), date_obj.getDate());
	end_day.setHours(23,59,59);
	var retArr = [];
	var all_selected = getMembersSelectedEvents();
	for(var i= 0; i < populatedEvents_d.length; i++){
		var curr_event = populatedEvents_d[i].event_object;
		var mem_cont = false;
		for(var j = 0; j < all_selected.length; j++){
			if(all_selected[j].event_id == curr_event.event_id){
				mem_cont = true;
				break;
			}
		}
		var user_cont = false;
		for(var j = 0; j < user_events_all.length; j++){
			if(user_events_all[j].event_id == curr_event.event_id){
				user_cont = true;
				break;
			}
		}
		if(mem_cont == false && user_cont == false){
			continue;
		}
		if(inRange(beginning_day.getTime(), curr_event.start_date, end_day.getTime())
			|| inRange(beginning_day.getTime(), curr_event.end_date, end_day.getTime())){
			retArr.push(populatedEvents_d[i]);
			continue;
		}
		var day_aff = new Date(new Date(curr_event.start_date).setHours(0,0,0));
		console.log("day_aff", day_aff, "curr_event", curr_event);
		// if(day_aff = date_obj.getTime()){
		// 	retArr.push(populatedEvents_d[i]);
		// }
	}
	return retArr;
}

function getEventsCurrDay(){
	var curr_day = new Date(_year_selected, _month_selected, _day_selected);
	return getEventsOnDate(curr_day);
}

// CALENDAR HEADERS

function dayTopHeader(col_index){
	var ret_div = document.createElement('div');
	ret_div.className = "col text-center defTopHeaderClass";
	ret_div.id = ret_div.className + ":" + col_index;
	var temp_date = new Date(_year_selected, _month_selected, _day_selected);
	var formatted_string = _days_of_week[temp_date.getDay()];
	formatted_string += ", " + _months_of_year[temp_date.getMonth()];
	formatted_string += " " + temp_date.getDate() + ", " + temp_date.getFullYear();
	ret_div.innerHTML = formatted_string;
	return ret_div;
}
function weekDatesHeader(col_index){
	var ret_div = document.createElement('div');
	ret_div.className = "col text-center defTopHeaderClass";
	ret_div.id = ret_div.className + ":" + col_index;
	ret_div.style = "min-width:10px";
	var start_week = _week_selected[0]
	var temp_day = new Date(start_week.getFullYear(), start_week.getMonth(), start_week.getDate() + col_index);
	ret_div.innerHTML = _months_of_year[temp_day.getMonth()] + " " + temp_day.getDate();
	ret_div.innerHTML += "<br/>" + _days_of_week[col_index];
	return ret_div;
}
function weekDaysHeader(col_index){
	var ret_div = document.createElement('div');
	ret_div.className = "col text-center defTopHeaderClass";
	ret_div.id = ret_div.className + ":" + col_index;
	ret_div.innerHTML = _days_of_week[col_index];
	return ret_div;
}
function noLeftHeader(row_index){
	return null;
}
function hourLeftHeader(row_index){
	var ret_div = document.createElement('div');
	ret_div.className = "col-1 defLeftHeaderClass float-right text-right";
	ret_div.id = ret_div.className + ":" + row_index;
	var str_to = _times_of_day_12[row_index];
	if(str_to.length < 4){
		str_to = "0" + str_to;
	}
	ret_div.innerHTML = str_to;
	return ret_div;
}
function fillMonthViewNumbers(){
	var tempCal = new Calendar('temp_cal');
	tempCal.genGrid(_year_selected, _month_selected, null);
	var num_grid = tempCal.grid;
	var count = 0;
	for (var i = 0; i < calArray.length; i++) {
		for(var j = 0; j < calArray[i].length; j++){
			textInputCalbox(i, j, num_grid[i][j].date);
			var clazz = _curr_month;
			if(num_grid[i][j].is_curr == false){
				clazz = _curr_month_not;
			}
			classCalbox(i, j, clazz);
			count++;
		}
	}
}
function textInputCalbox(row_index, col_index, textInput){
	var curr_div = coordinates_to_div(row_index, col_index);
	curr_div.innerHTML = textInput;
}

function classCalbox(row_index, col_index, clazz){
	var curr_div = coordinates_to_div(row_index, col_index);
	curr_div.className += " "  + clazz;
	// console.log(curr_div);
}

function setCurrTime(){
	var month_sel = document.getElementById("month_sel");
	var year_sel = document.getElementById("year_sel");
	var day_sel = document.getElementById("day_sel");
	month_sel.value = parseMonthi(new Date().getMonth());
	year_sel.value = new Date().getFullYear();
	day_sel.value = new Date().getDate();
	_month_selected = new Date().getMonth();
	_year_selected = new Date().getFullYear();
	_day_selected = new Date().getDate();
	// console.log(_month_selected, _day_selected, _year_selected);
}
function parseMonthi(int_val){
	return _months_of_year[int_val];
}
function parseMonth(sel_value){
	for(var i = 0; i < _months_of_year.length; i++){
		if(_months_of_year[i] == sel_value){
			return i;
		}
	}
	return -1;
}
function monthYearUpdate(){
	clearEvents();
	var month_sel = document.getElementById("month_sel");
	var year_sel = document.getElementById("year_sel");
	_month_selected = parseMonth(month_sel.value);
	_year_selected = year_sel.value;
	console.log(_month_selected, _year_selected);
	populateDay();
	selectDayHard(1);
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}
function updateMonthYear(new_month, new_year){
	updateMonthYearHard(new_month, new_year, 1);
}
function updateMonthYearHard(new_month, new_year, hard){
	var month_sel = document.getElementById("month_sel");
	var year_sel = document.getElementById("year_sel");
	month_sel.value = parseMonthi(new_month);
	year_sel.value = new_year;
	_month_selected = new_month;
	_year_selected = new_year;
	populateDay();
	selectDayHard(hard);
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}
function dayWeekUpdate(){
	clearEvents();
	var day_sel = document.getElementById("day_sel");
	_day_selected = day_sel.value;
	_week_selected = [0, 0];
	var date_selected = new Date(_year_selected, _month_selected, _day_selected);
	var curr_day_of_week = date_selected.getDay();
	var delta_sun = 0 - curr_day_of_week;
	var prev_sun = new Date(date_selected.getFullYear(), date_selected.getMonth(), date_selected.getDate() + delta_sun);
	var delta_sat = 6 - curr_day_of_week;
	var next_sat = new Date(date_selected.getFullYear(), date_selected.getMonth(), date_selected.getDate() + delta_sat);
	next_sat.setHours(23, 59, 59);
	_week_selected = [prev_sun, next_sat];
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}
function populateMonthYear(){
	var month_sel = document.getElementById("month_sel");
	for(var i=0; i < _months_of_year.length; i++){
		var curr_opt = document.createElement('option');
		curr_opt.className = "monthOpt";
		curr_opt.innerText = _months_of_year[i];
		month_sel.appendChild(curr_opt);
	}
	var year_sel = document.getElementById("year_sel");
	for(var i=1970; i < 2037; i++){
		var curr_opt = document.createElement('option');
		curr_opt.className = "yearOpt";
		curr_opt.innerText = i;
		year_sel.appendChild(curr_opt);
	}
}
function populateDay(){
	var day_sel = document.getElementById("day_sel");
	while(day_sel.children.length > 0){
		day_sel.removeChild(day_sel.lastElementChild);
	}

	var month_start = new Date(_year_selected, _month_selected, 1);
	var curr_day = new Date(_year_selected, _month_selected, 1);
	var dayArr = [];
	for(var i = 1; i < 32; i++){
		curr_day = new Date(month_start.getFullYear(), month_start.getMonth(), i);
		if(curr_day.getMonth() != month_start.getMonth()){
			break;
		}
		dayArr.push(i);
	}
	for(var i = 0; i < dayArr.length; i++){
		var curr_opt = document.createElement("option");
		curr_opt.className = "dayOpt";
		curr_opt.innerText = dayArr[i];
		day_sel.appendChild(curr_opt);
	}
	return dayArr;
}
function selectDayHard(day_select){
	var day_sel = document.getElementById("day_sel");
	day_sel.value = day_select;
	dayWeekUpdate();
}
function scrollAdjust(){
	if(_prev_scroll_y != 0){
		window.scrollTo(0, _prev_scroll_y);
	}
}
function leftArrowClick(){
	if(_switchType == "list"){
		return;
	}
	clearEvents();
	switch(_switchType){
		case "month":
			var temp_date = new Date(_year_selected, parseInt(_month_selected) - 1, 1);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			updateMonthYear(_month_selected, _year_selected);
			break;
		case "week":
			var temp_date = new Date(_year_selected, parseInt(_month_selected), _day_selected);
			temp_date.setDate(temp_date.getDate() - 7);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			_day_selected = temp_date.getDate();
			// console.log(temp_date);
			// console.log(_day_selected);
			updateMonthYear(_month_selected, _year_selected);
			_day_selected = temp_date.getDate();
			selectDayHard(_day_selected);
			break;
		case "day":
			var temp_date = new Date(_year_selected, parseInt(_month_selected), _day_selected);
			temp_date.setDate(temp_date.getDate() - 1);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			_day_selected = temp_date.getDate();
			updateMonthYear(_month_selected, _year_selected);
			_day_selected = temp_date.getDate();
			selectDayHard(_day_selected);
			break;
		default:
	}
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}
function currButtonClick(){
	clearEvents();
	setCurrTime();
	selectDayHard(_day_selected);
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}
function rightArrowClick(){
	if(_switchType == "list"){
		return;
	}
	clearEvents();
	switch(_switchType){
		case "month":
			var temp_date = new Date(_year_selected, parseInt(_month_selected) + 1, 1);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			updateMonthYear(_month_selected, _year_selected);
			break;
		case "week":
			var temp_date = new Date(_year_selected, parseInt(_month_selected), _day_selected);
			temp_date.setDate(temp_date.getDate() + 7);
			// console.log(temp_date);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			updateMonthYear(_month_selected, _year_selected);
			_day_selected = temp_date.getDate();
			selectDayHard(_day_selected);
			break;
		case "day":
			var temp_date = new Date(_year_selected, parseInt(_month_selected), _day_selected);
			temp_date.setDate(temp_date.getDate() + 1);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			updateMonthYear(_month_selected, _year_selected);
			_day_selected = temp_date.getDate();
			selectDayHard(_day_selected);
			break;
		default:
	}
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}
function populateFriendsSelectDropdown(){
	var friendsSelectDropdown = document.getElementById("members_select_dropdown");
	var friendsSelectDropdownButton = document.getElementById("members_select_dropdown_button");
	switch(_calendar_mode){
		case "USER":
			break;
		case "FRIEND":
			console.log(friendsSelectDropdown);
			friendsSelectDropdownButton.style.display = "none";
			return;
		case "GROUP":
			friendsSelectDropdownButton.innerText = "Members";
			break;
		default:
	}
	var friends_to_pop = _calendar_struct.calendar_data.member_info;
	for(var i = 0; i < friends_to_pop.length; i++){
		var curr_friend = friends_to_pop[i];
		var curr_a = document.createElement("a");
		curr_a.className = "dropdown-item";
		var temp_id = curr_friend.alias + "_check";
		curr_a.href = "#";
		curr_a.setAttribute("onclick", "checkFriendSelect('" + temp_id + "')");
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
		friendsSelectDropdown.appendChild(curr_a);
		member_check_ids.push({"check_id" : temp_id, "alias" : curr_friend.alias});
	}
}

function checkFriendSelect(sel_id){
	// console.log("checkFriendSelect", sel_id);
	_prev_scroll_y = window.scrollY;
	var check_input = document.getElementById(sel_id);
	if(check_input.checked){
		check_input.checked = false;
		check_input.setAttribute("flag", "false");
	}else{
		check_input.checked = true;
		check_input.setAttribute("flag", "true");
	}
	switchCalendarView(_cont_id, _switchType);
}


function getMembersSelected(){
	var valid = [];
	for(var i = 0; i < member_check_ids.length; i++){
		var curr_div = document.getElementById(member_check_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(member_check_ids[i].alias);
		}
	}
	return valid;
}

function getMembersSelectedEvents(){
	var members_selected = getMembersSelected();
	var retArray = [];
	for(var i = 0; i < member_events_all.length; i++){
		if(members_selected.includes(member_events_all[i].event_creator_alias)){
			retArray.push(member_events_all[i]);
		}
	}
	// for(var i = 0; i < members_selected.length; i++){
	// 	var curr_firebase_id = aliasToFirebaseID(members_selected[i]);
	// 	var curr_events = []
	// 	for(var j = 0; j < _calendar_struct.calendar_data.member_events.length; j++){
	// 		if(_calendar_struct.calendar_data.member_events[j].firebase_id == curr_firebase_id){
	// 			curr_events = _calendar_struct.calendar_data.member_events[j].participating_events;
	// 			break;
	// 		}
	// 	}
	// 	for(var j = 0; j < curr_events.length; j++){
	// 		retArray.push(curr_events[j]);
	// 	}
	// }
	return retArray;
}


// HEADER ABBREVIATION

function abbreviateHeader_xs(){
	for (var i = 0; i < headerArray_top.length; i++) {
		var curr_head = headerArray_top[i];
		if(curr_head.innerHTML.includes(_days_of_week[i])){
			var new_inner = curr_head.innerHTML.replace(_days_of_week[i], _days_of_week_abv_abv[i]);
			curr_head.innerHTML = new_inner;
		}
		// console.log(curr_head);
	}
}
function abbreviateHeader(){
	for (var i = 0; i < headerArray_top.length; i++) {
		var curr_head = headerArray_top[i];
		if(curr_head.innerHTML.includes(_days_of_week[i])){
			var new_inner = curr_head.innerHTML.replace(_days_of_week[i], _days_of_week_abv[i]);
			curr_head.innerHTML = new_inner;
		}
		// console.log(curr_head);
	}
}
function elongateHeader(){
	for (var i = 0; i < headerArray_top.length; i++) {
		var curr_head = headerArray_top[i];
		if(curr_head.innerHTML.includes(_days_of_week[i]) == false){
			if(curr_head.innerHTML.includes(_days_of_week_abv[i])){
				var new_inner = curr_head.innerHTML.replace(_days_of_week_abv[i], _days_of_week[i]);
				curr_head.innerHTML = new_inner;
			}else if(curr_head.innerHTML.includes(_days_of_week_abv_abv[i])){
				var new_inner = curr_head.innerHTML.replace(_days_of_week_abv_abv[i], _days_of_week[i]);
				curr_head.innerHTML = new_inner;
			}
		}
		// console.log(curr_head);
	}
}

// CALENDAR CLICK

function select_id_to_coordinates(select_id){
	var retArr = null;
	for (var i = 0; i < gridArray.length; i++) {
		for (var j = 0; j < gridArray[i].length; j++) {
			var curr_div = gridArray[i][j];
			if(curr_div.id === select_id){
				retArr = [i - y_offset, j - x_offset];
				return retArr;
			}
		}
	}
	return retArr;
}
function selectUnique(cont_id, select_id){
	// switchCalendarView(_cont_id, _switchType);
	select(select_id);
	var coords = select_id_to_coordinates(select_id);
	// 
}
function select(select_id){
	var toSelect = document.getElementById(select_id);
	if(toSelect == null){
		return;
	}
	_select_id = select_id;
	// console.log("select_new:" + select_id);
}
function dayClickM(click_id){
	// console.log("dayClick:" + click_id);
	_prev_scroll_y = window.scrollY;
	var temp_div = document.getElementById(click_id);
	if(temp_div.className.includes(_curr_month_not)){
		return;
	}
	var pre_check = (temp_div.style.backgroundColor == select_color);
	selectDayHard(Number(temp_div.innerText));
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
	if(pre_check == false){
		// console.log(temp_div.style.backgroundColor);
		temp_div = document.getElementById(click_id);
		temp_div.style.backgroundColor = select_color;
	}

	// console.log("week selected");
	selectUnique(_cont_id, click_id)
	// switchCalendarView(_cont_id, "week");
		// focusCalendar();
}
function hourClickW(click_id){
	console.log("hourClickW:" + click_id);
	selectUnique(_cont_id, click_id)
	// switchCalendarView(_cont_id, "day");
}
function hourClickD(click_id){
	console.log("hourClickD:" + click_id);
	selectUnique(_cont_id, click_id)
	// switchCalendarView(_cont_id, "month");
}

// CALENDAR POS UTILS

function getRowCol(dateVal){
	var _row = Math.floor(dateVal/7);
	var _col = Math.floor(dateVal % 7);
	return {row:_row, col:_col};
}
function getWeek(dateArg){
	return Math.floor(dateArg / 7.0);
}
function coordinates_to_div(row_index, col_index){
	if(row_index + y_offset < 0 || row_index + y_offset > gridArray.length){
		return null;
	}
	if(col_index + x_offset < 0 || col_index + x_offset > gridArray[0].length){
		return null;
	}
	var curr_div = gridArray[row_index + y_offset][col_index + x_offset];
	return curr_div;
}

// -----------------------------------------------------------------
// DRAW EVENTS

function drawEventSafe_d(time_start, length, event_object){
	drawEventSafe_d_color(time_start, length, event_object, user_color);
}
function drawEventSafe_d_color(time_start, length, event_object, color){
	var event_id = event_object.id;
	if(containsID_d(event_id)){
		console.log("Event already exists. Try modifying it instead.");
		return;
	}
	if(time_start < 0){
		time_start = 0;
	}
	var c_length = length;
	if(length + time_start > 24){
		c_length = 24 - time_start;
	}
	drawEventUnsafe_d_color(time_start, c_length, event_object, color);
}
function drawEventSafe_w(start_col, end_col, time_start, length, event_object){
	drawEventSafe_w_color(start_col, end_col, time_start, length, event_object, user_color);
}
function drawEventSafe_w_color(start_col, end_col, time_start, length, event_object, color){
	var c_length = length;
	if(length + time_start > 24){
		c_length = 24 - time_start;
	}
	var d_length = end_col - start_col + 1;
	if(d_length < 0){
		d_length = 1;
	}
	if(d_length + start_col > 7){
		d_length = 7 - start_col;
	}
	drawEventUnsafe_w_color(start_col, d_length, time_start, c_length, event_object, color);
}
function drawEventSafe_m(start, end, event_object){
	var event_id = event_object.event_id;
	if(containsID(event_id)){
		console.log("Event already exists. Try modifying it instead.");
		return;
	}
	var event_split = splitEvent(start, end);
	for(var index = 0; index < event_split.length; index++){
		var curr_struct = event_split[index];
		var curr_start = curr_struct.range[0];
		var width = curr_struct.range[1] - curr_start + 1;
		// console.log(curr_struct);
		event_object.split_tag = index;
		drawEventUnsafe_m(curr_start, width, curr_struct.flags, event_object);
	}
}
function drawEventSafe_m_color(start, end, event_object, color){
	var event_id = event_object.event_id;
	var event_split = splitEvent(start, end);
	if(event_object.event_id == 24){
		console.log(event_split);
	}
	for(var index = 0; index < event_split.length; index++){
		var curr_struct = event_split[index];
		var curr_start = curr_struct.range[0];
		var width = curr_struct.range[1] - curr_start + 1;
		// console.log(curr_struct);
		event_object.split_tag = index;
		drawEventUnsafe_m_color(curr_start, width, curr_struct.flags, event_object, color);
	}
}
function drawEventUnsafe_d_s(curr_struct){
	drawEventUnsafe_d_color(curr_struct.start_time, curr_struct.length, curr_struct.event_object, curr_struct.color);
}
function drawEventUnsafe_w_s(curr_struct){
	drawEventUnsafe_w_color(curr_struct.start, curr_struct.day_width, curr_struct.start_time, curr_struct.length, curr_struct.event_object, curr_struct.color);
}
function drawEventUnsafe_m_s(curr_struct){
	drawEventUnsafe_m_color(curr_struct.start, curr_struct.day_width, curr_struct.flags, curr_struct.event_object, curr_struct.event_color);
}
function drawEventUnsafe_d(start_time, length, event_object){
	drawEventUnsafe_d_color(start_time, length, event_object, user_color);
}
function drawEventUnsafe_d_color(start_time, length, event_object, color){
	var start = 0;
	var day_width = 1;
	var day_div = calArray[0][start];
	var rect = day_div.getBoundingClientRect();
	var col_width = rect.width;
	var row_height = rect.height;
	var x_offset_px_l = 0;
	var x_offset_px_r = 0;
	var y_perc = 0.30;
	var y_offset_px = start_time*row_height;
	var width = day_width*col_width - x_offset_px_l - x_offset_px_r;
	var height = row_height*length;
	var divToAdd = document.createElement('div');
	divToAdd.style = "position:absolute; background-color:"+ color + "; z-index:2; height:20px; cursor:pointer;"
	+ "top:" + (rect.top + y_offset_px + window.scrollY) + "px;" 
	+ "left:" + (rect.left + x_offset_px_l) + "px;" 
	+ "width:" + width + "px;" 
	+ "height:" + height + "px;";
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_object.event_id + ");" );
	divToAdd.id = "d" + event_object.event_id + "" + event_object.start_date + "-" + event_object.end_date;
	if(document.getElementById(divToAdd.id) == null){
		document.body.appendChild(divToAdd);
		eventDivArray.push(divToAdd);
	}
	var new_struct = {
		start_time:start_time,
		length:length, 
		event_object:event_object,
		color:color
	};
	var contains = containsStruct_d(new_struct);
	if(contains == false){
		populatedEvents_d.push(new_struct);
		// console.log(populatedEvents_d);
	}
}
function drawEventUnsafe_w(start, day_width, start_time, length, event_object){
	drawEventUnsafe_w_color(start,day_width,start_time, length, event_object, user_color);
}
function drawEventUnsafe_w_color(start, day_width, start_time, length, event_object, color){
	// console.log(event_object);
	var day_div = calArray[0][start];
	var rect = day_div.getBoundingClientRect();
	var col_width = rect.width;
	var row_height = rect.height;
	var x_offset_px_l = 0;
	var x_offset_px_r = 0;
	var y_perc = 0.30;
	var y_offset_px = start_time*row_height;
	var width = day_width*col_width - x_offset_px_l - x_offset_px_r;
	var height = row_height*length;
	var divToAdd = document.createElement('div');
	divToAdd.style = "position:absolute; background-color:" + color+ "; z-index:2; height:20px; cursor:pointer;"
	+ "top:" + (rect.top + y_offset_px + window.scrollY) + "px;" 
	+ "left:" + (rect.left + x_offset_px_l) + "px;" 
	+ "width:" + width + "px;" 
	+ "height:" + height + "px;";
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_object.event_id + ");" );
	divToAdd.id = "w" + event_object.event_id + "" + event_object.start_date + "-" + event_object.end_date;
	if(document.getElementById(divToAdd.id) == null){
		document.body.appendChild(divToAdd);
		eventDivArray.push(divToAdd);
	}
	var new_struct = {
		start:start, 
		day_width:day_width,
		start_time:start_time,
		length:length, 
		event_object:event_object,
		color:color,
		contain_div: divToAdd
	};
	var contains = containsStruct_w(new_struct);
	if(contains == false){
		populatedEvents_w.push(new_struct);
		// console.log(populatedEvents_w);
	}
}
function drawEventUnsafe_m(start, day_width, flags, event_object){
	drawEventUnsafe_m_color(start, day_width, flags, event_object, user_color);
}
function drawEventUnsafe_m_color(start, day_width, flags, event_object, color){
	var coords = getRowCol(start);
	// console.log("drawEventUnsafe_m:");
	// console.log(coords);
	var ref_week = divRowsArray[coords.row];
	var rect = ref_week.children[coords.col].getBoundingClientRect();
	// console.log("ref_week");
	// console.log(ref_week);
	var col_width = rect.width;
	var x_perc = 0.10;
	var x_offset_px = x_perc * col_width;
	var x_offset_px_l = 0;
	var x_offset_px_r = 0;
	var y_perc = 0.40;
	var y_offset_px = y_perc * rect.height;
	if(flags.includes("l")){
		x_offset_px_l = 0;
	}else{
		x_offset_px_l = x_offset_px;
	}
	if(flags.includes("r")){
		x_offset_px_r = 0;
	}else{
		x_offset_px_r = x_offset_px;
	}
	var width = day_width*col_width - x_offset_px_l - x_offset_px_r;
	var height = Math.max(20, 0.15*col_width);
	var divToAdd = document.createElement('div');
	divToAdd.style = "position:absolute; background-color:" + color + "; z-index:2; height:" + height + "px; cursor:pointer;"
	+ "top:" + (rect.top + y_offset_px + window.scrollY) + "px;" 
	+ "left:" + (rect.left + x_offset_px_l) + "px;" 
	+ "width:" + width + "px;";
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_object.event_id + ");" );
	divToAdd.id = "m" + event_object.event_id + flags + "" + event_object.start_date + "-" + event_object.end_date + "_" + event_object.split_tag
	+ "_" + start + ":" + day_width;

	if(document.getElementById(divToAdd.id) == null){
		document.body.appendChild(divToAdd);
		eventDivArray.push(divToAdd);
	}
	var new_struct = {start:start, 
		day_width:day_width, 
		flags:flags, 
		event_object:event_object,
		event_color:color,
		contain_div: divToAdd
	};
	var contains = containsStruct(new_struct);
	if(contains == false){
		populatedEvents.push(new_struct);
		// console.log(populatedEvents);
	}else{
		
	}
	// console.log(divToAdd);
}
function populateEventStructure_m(curr_event, color){
	var temp_start = new Date(Number(curr_event.start_date));
	var temp_end = new Date(Number(curr_event.end_date));
	var day_pos_start = getDayPosition(temp_start.getDate(), temp_start.getFullYear(), temp_start.getMonth());
	var day_pos_end = getDayPosition(temp_end.getDate(), temp_end.getFullYear(), temp_end.getMonth());
	drawEventSafe_m_color(day_pos_start, day_pos_end, curr_event, color);
}
function splitEventStructure(curr_event){
	// Split into multiple weeks affected.
	var day_event_starts = new Date((new Date(Number(curr_event.start_date))).setHours(0,0,0));
	var day_event_ends =  new Date((new Date(Number(curr_event.end_date))).setHours(23,59,59));
	if(day_event_starts.getTime() == day_event_ends.getTime()){
		return [curr_event];
		console.log("SAME TIME");
	}
	var day_affected_start = new Date(new Date(curr_event.start_date).setHours(0,0,0));
	var day_affected_end = new Date(new Date(curr_event.end_date).setHours(0,0,0));
	if(day_affected_start.getTime() == day_affected_end.getTime()){
		return [curr_event];
		console.log("IN SAME DAY");
	}
	var retArray = [];
	var initDate = {};
	initDate.start_date = curr_event.start_date;
	initDate.end_date =  (new Date(day_event_starts.getTime())).setHours(23,59,59);
	retArray.push(initDate);
	// Start Next Day
	for(var currDate =  new Date(new Date(day_event_starts.getTime()).setDate(day_event_starts.getDate() + 1));
		currDate.getTime() < new Date(day_event_ends.getTime()).setDate(day_event_ends.getDate() - 1);
		currDate =  new Date(new Date(currDate.getTime()).setDate(currDate.getDate() + 1))){
		var currStruct = {};
		currStruct.start_date = currDate.getTime();
		currStruct.end_date =  new Date(currDate.getTime()).setHours(23,59,59);
		retArray.push(currStruct);
	}
	var finalDate = {};
	finalDate.start_date = new Date(day_event_ends.getTime()).setHours(0,0,0);
	finalDate.end_date = curr_event.end_date;
	retArray.push(finalDate);
	return retArray;
}
function populateEventStructure_w(passed_event, color){
	// console.log(curr_event);
	var split_array = splitEventStructure(passed_event);
	for(var i = 0; i < split_array.length; i++){
		var curr_event = split_array[i];
		curr_event.event_id = passed_event.event_id;
		var temp_start = new Date(Number(curr_event.start_date));
		var temp_end = new Date(Number(curr_event.end_date));
		// Get length of event
		var end_time_day = temp_end.getHours()*60 + temp_end.getMinutes();
		var start_time_day = temp_start.getHours()*60 + temp_start.getMinutes();
		var duration = Math.abs((end_time_day - start_time_day)/60);
		var daywidth = Math.abs(curr_event.end_date - curr_event.start_date)/(1000*60*60*24);
		// console.log(daywidth);
		if(daywidth < 1){
			daywidth = 1;
		}
		//drawEventUnsafe_w_color(2,1,6,3,{event_id:-1},user_color)
		drawEventSafe_w_color(temp_start.getDay(), temp_start.getDay()+ Math.ceil(daywidth) - 1, start_time_day / 60, duration, curr_event, color);
	}
	
}

function populateEventStructure_d(passed_event, color){
	var split_array = splitEventStructure(passed_event);
	for(var i = 0; i < split_array.length; i++){
		var curr_event = split_array[i];
		curr_event.event_id = passed_event.event_id;
		var temp_start = new Date(Number(curr_event.start_date));
		var temp_end = new Date(Number(curr_event.end_date));
		var end_time_day = temp_end.getHours()*60 + temp_end.getMinutes();
		var start_time_day = temp_start.getHours()*60 + temp_start.getMinutes();
		var duration = Math.abs((end_time_day - start_time_day)/60);
		//drawEventSafe_d(time_start, length, event_object)
		drawEventSafe_d_color(start_time_day/60, duration, curr_event, color);
	}

}

function eventClicked(event_id){
	// STUBBED
	// console.log("eventClicked:" + event_id);
	// var temp_struct = getEventStruct(event_id);
	// console.log(temp_struct);
}

// CONATINS

function containsID_d(event_id){
	var contains = false;
	for(var i = 0; i < populatedEvents_d.length; i++){
		if(populatedEvents_d[i].event_object.event_id == event_id){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsID_w(event_id){
	var contains = false;
	for(var i = 0; i < populatedEvents_w.length; i++){
		if(populatedEvents_w[i].event_object.event_id == event_id){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsID(event_id){
	var contains = false;
	for(var i = 0; i < populatedEvents.length; i++){
		if(populatedEvents[i].event_object.event_id == event_id){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsStruct(curr_struct){
	var contains = false;
	for(var i = 0; i < populatedEvents.length; i++){
		if(populatedEvents[i].event_object.event_id == curr_struct.event_object.event_id && 
			populatedEvents[i].start == curr_struct.start && 
			populatedEvents[i].day_width == curr_struct.day_width && 
			populatedEvents[i].event_object.tag_id == curr_struct.event_object.tag_id && 
			populatedEvents[i].event_object.split_tag == curr_struct.event_object.split_tag && 
			populatedEvents[i].event_object.start_date == curr_struct.event_object.start_date &&
			populatedEvents[i].event_object.end_date == curr_struct.event_object.end_date){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsStruct_w(curr_struct){
	var contains = false;
	for(var i = 0; i < populatedEvents_w.length; i++){
		if(populatedEvents_w[i].event_object.start_date == curr_struct.event_object.start_date
			&& populatedEvents_w[i].event_object.end_date == curr_struct.event_object.end_date &&
			populatedEvents_w[i].event_object.event_id == curr_struct.event_object.event_id &&
			populatedEvents_w[i].event_object.tag_id == curr_struct.event_object.tag_id){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsStruct_d(curr_struct){
	var contains = false;
	for(var i = 0; i < populatedEvents_d.length; i++){
		if(populatedEvents_d[i].event_object.start_date == curr_struct.event_object.start_date
			&& populatedEvents_d[i].event_object.end_date == curr_struct.event_object.end_date &&
			populatedEvents_d[i].event_object.event_id == curr_struct.event_object.event_id && 
			populatedEvents_d[i].event_object.tag_id == curr_struct.event_object.tag_id){
			contains = true;
			break;
		}
	}
	return contains;
}
function addEvents(){
	switch(_switchType){
		case "day":
			addEventsD();
			break;
		case "week":
			addEventsW();
			break;
		case "month":
			addEventsM();
			break;
		default:
			return;
	}
	scrollAdjust();
}
function addEventsD(){
	var count = 0;
	var populatedEvents_c = getEventsCurrDay();
	for (var i = 0; i < populatedEvents_c.length; i++) {
		drawEventUnsafe_d_s(populatedEvents_c[i]);
	}
}
function addEventsW(){
	var count = 0;
	var populatedEvents_c = getEventsCurrWeek();
	for (var i = 0; i < populatedEvents_c.length; i++) {
		drawEventUnsafe_w_s(populatedEvents_c[i]);
	}
}
function addEventsM(){
	// console.log("addEventsM");
	var count = 0;
	var populatedEvents_c = getEventsCurrMonth();
	for (var i = 0; i < populatedEvents_c.length; i++) {
		drawEventUnsafe_m_s(populatedEvents_c[i]);
	}
}
// -----------------------------------------------------------------

// EVENT HANDLING

function getEventStruct(_event_id){
	// console.log("getEventStruct", _event_id);
	for(var i = 0; i < user_events_all.length; i++){
		var curr_event = user_events_all[i];
		if(curr_event.event_id == _event_id){
			return curr_event;
		}
	}
	for(var i = 0; i < member_events_all.length; i++){
		var curr_event = member_events_all[i];
		if(curr_event.event_id == _event_id){
			return curr_event;
		}
	}
}

function testMultiMonthSplit(){
	var e1 = {};
	e1.start_date = new Date("April 1 2019").getTime();
	e1.end_date = new Date("July 20 2019").getTime();
	e1.event_id = 20;
	var res1 = multiMonthSplit(e1);
	for(var i = 0;  i < res1.length; i++){
		console.log(new Date(res1[i].start_date), new Date(res1[i].end_date));
	}
	console.log(res1);

}

// Deep cloning functions don't work for multi month split
function noviceEventClone(event_passed){
	var retClone = {};
	retClone.start_date = event_passed.start_date;
	retClone.end_date = event_passed.end_date;
	retClone.event_id = event_passed.event_id;
	return retClone;
}

function getTotalMonths(event_passed){
	var startDateObj = new Date(event_passed.start_date);
	var endDateObj = new Date(event_passed.end_date);
	console.log(startDateObj, endDateObj);
	var d_m = endDateObj.getMonth() - startDateObj.getMonth();
	var d_y = parseInt(endDateObj.getFullYear()) - parseInt(startDateObj.getFullYear());
	var totalMonths = d_m + d_y*12;
	return totalMonths;
}

function multiMonthSplit(event_passed){
	var startDateObj = new Date(event_passed.start_date);
	var endDateObj = new Date(event_passed.end_date);
	if(startDateObj.getMonth() == endDateObj.getMonth() &&
		startDateObj.getFullYear() == endDateObj.getFullYear()){
		event_passed.tag_id = "0";
		return [event_passed];
	}
	var d_m = endDateObj.getMonth() - startDateObj.getMonth();
	var d_y = parseInt(endDateObj.getFullYear()) - parseInt(startDateObj.getFullYear());
	var totalMonths = d_m + d_y*12;
	var retArray = [];
	var initDate = noviceEventClone(event_passed);
	initDate.start_date = event_passed.start_date;
	var start_curr_month_affected = new Date(new Date(event_passed.start_date).setHours(23, 59, 59));
	start_curr_month_affected = new Date(start_curr_month_affected.setMonth(start_curr_month_affected.getMonth() + 1));
	start_curr_month_affected = new Date(start_curr_month_affected.setDate(0));
	initDate.end_date = start_curr_month_affected.getTime();
	initDate.tag_id = "0";
	retArray.push(initDate);
	for (var i = 1; i < totalMonths; i++) {
		var deep_clone = noviceEventClone(event_passed);
		var curr_month_affected_s = new Date(event_passed.start_date);
		curr_month_affected_s = new Date(curr_month_affected_s.setHours(0,0,0));
		curr_month_affected_s = new Date(curr_month_affected_s.setMonth(curr_month_affected_s.getMonth() + i));
		curr_month_affected_s = new Date(curr_month_affected_s.setDate(1));
		deep_clone.start_date = curr_month_affected_s.getTime();
		var curr_month_affected_e = new Date(curr_month_affected_s.getTime());
		curr_month_affected_e = new Date(curr_month_affected_e.setHours(23,59,59));
		curr_month_affected_e = new Date(curr_month_affected_e.setMonth(curr_month_affected_e.getMonth() + 1));
		curr_month_affected_e = new Date(curr_month_affected_e.setDate(0));
		deep_clone.end_date = curr_month_affected_e.getTime();
		deep_clone.tag_id = "" + i;
		retArray.push(deep_clone);
	}
	var postDate = noviceEventClone(event_passed);
	postDate.end_date = event_passed.end_date;
	var end_curr_month_affected = new Date(new Date(event_passed.end_date).setHours(0, 0, 0));
	end_curr_month_affected = new Date(end_curr_month_affected.setMonth(end_curr_month_affected.getMonth()));
	end_curr_month_affected = new Date(end_curr_month_affected.setDate(1));
	postDate.start_date = end_curr_month_affected.getTime();
	postDate.tag_id = "" + totalMonths;
	retArray.push(postDate);

	return retArray;
}

function loadUserEvents(){
	var split_all = [];
	for(var i = 0; i < user_events_all.length; i++){
		var curr_event = user_events_all[i];
		var res1 = multiMonthSplit(curr_event);
		for(var j = 0;  j < res1.length; j++){
			split_all.push(res1[j]);
		}
	}
	for(var i = 0; i < split_all.length; i++){
		var curr_event = split_all[i];
		populateEventStructure_m(curr_event, user_color);
		populateEventStructure_w(curr_event, user_color);
		populateEventStructure_d(curr_event, user_color);
	}
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}

function loadMemberEvents(){
	var split_all = [];
	for(var i = 0; i < member_events_all.length; i++){
		var curr_event = member_events_all[i];
		var res1 = multiMonthSplit(curr_event);
		for(var j = 0;  j < res1.length; j++){
			split_all.push(res1[j]);
		}
	}
	for(var i = 0; i < split_all.length; i++){
		var curr_event = split_all[i];
		console.log("curr_member", curr_event);
		if(curr_event.isHidden != undefined && curr_event.isHidden){
			populateEventStructure_m(curr_event, hidden_color);
			populateEventStructure_w(curr_event, hidden_color);
			populateEventStructure_d(curr_event, hidden_color);
			continue;
		}
		populateEventStructure_m(curr_event, member_color);
		populateEventStructure_w(curr_event, member_color);
		populateEventStructure_d(curr_event, member_color);
		
	}
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}

function getDayPosition(day_num, year, month){
	var count = 0;
	var temp_cal = new Calendar("tempCal");
	temp_cal.genGrid(year, month, null);
	var grid = temp_cal.grid;
	for(var i = 0; i < grid.length; i++){
		for(var j = 0; j < grid[i].length; j++){
			var curr_struct = grid[i][j];
			if(curr_struct.date == day_num &&curr_struct.is_curr){
				return count;
			}
			count++;
		}
	}
}

function repeatToAllEvents(repeat_event){
	var retArray = [];
	// Start and end
	var start_date = repeat_event.start_date;
	var start_date_obj = new Date(start_date);
	var end_date = repeat_event.end_date;
	var end_date_obj = new Date(end_date);
	// Convert rep_pattern to array
	var rep_array = repeat_event.week_arr.split('');
	// Find first day of repeat pattern
	var curr_date_obj = new Date(start_date);
	var found_date_start = null;
	for(;curr_date_obj.getTime() < end_date; curr_date_obj = new Date(new Date(curr_date_obj.getTime()).setDate(curr_date_obj.getDate() + 1))){
		var curr_day = curr_date_obj.getDay();
		if(rep_array[curr_day] == "1"){
			found_date_start = curr_date_obj;
			break;
		}
	}
	if(found_date_start == null){
		return retArray;
	}
	curr_date_obj = new Date(end_date);
	var found_date_end = null;
	for(; curr_date_obj.getTime() >= start_date; curr_date_obj = new Date(new Date(curr_date_obj.getTime()).setDate(curr_date_obj.getDate() - 1))){
		var curr_day = curr_date_obj.getDay();
		if(rep_array[curr_day] == "1"){
			found_date_end = curr_date_obj;
			break;
		}
	}
	if(found_date_end == null){
		return retArray;
	}
	var custom_start = new Date(found_date_start.getTime());
	var start_hours = custom_start.getHours();
	var start_minutes = custom_start.getMinutes();
	var custom_end = new Date(found_date_start.getTime());
	var end_hours = end_date_obj.getHours();
	var end_minutes = end_date_obj.getMinutes();
	custom_end = new Date(custom_end.setHours(end_hours,end_minutes));

	curr_date_obj = new Date(custom_start.getTime());
	for(;curr_date_obj.getTime() < found_date_end.getTime(); curr_date_obj = new Date(new Date(curr_date_obj.getTime()).setDate(curr_date_obj.getDate() + 1))){
		var curr_day = curr_date_obj.getDay();
		if(rep_array[curr_day] == "1"){
			var temp_start = new Date(curr_date_obj.getTime());
			temp_start = new Date(temp_start.setHours(start_hours, start_minutes));
			var temp_end = new Date(curr_date_obj.getTime());
			temp_end = new Date(temp_end.setHours(end_hours, end_minutes));
			var temp_slice = {};
			temp_slice.start_date = temp_start.getTime();
			temp_slice.end_date = temp_end.getTime();
			temp_slice.event_id = repeat_event.event_id;
			temp_slice.repeat = true;
			temp_slice.event_creator_firebase_id = repeat_event.event_creator_firebase_id;
			temp_slice.event_creator_alias = repeat_event.event_creator_alias;
			temp_slice.event_title = repeat_event.event_title;
			if(repeat_event.isHidden != undefined && repeat_event.isHidden == "true"){
				temp_slice.isHidden = repeat_event.isHidden;
			}
			retArray.push(temp_slice);
		}
	}


	// Find how many weeks affected
	var start_week_obj = new Date(start_date);
	start_week_obj = new Date(start_week_obj.setHours(0,0,0));
	var end_week_obj = new Date(end_date);
	end_week_obj = new Date(end_week_obj.setHours(0,0,0));
	var delta_days = (end_week_obj.getTime() - start_week_obj.getTime()) / (1000*60*60*24);
	return retArray;
}

function testPooyaRepeat(){
	var start_date = 1552685400000;
	var end_date = 1552692600000;
	console.log("starts:", new Date(start_date));
	console.log("ends:", new Date(end_date));
	let soccer = new Event('soccer','soccer practice', start_date, end_date);
	var x = soccer.rep('1','0','1','0','0','0','0','1', 1, start_date, end_date, 12345, [56789,51231]);
	console.log(x);

}

// -----------------------------------------------------------------


function main_renderCalendar(calendar_struct){
	_calendar_struct = calendar_struct;
	user_events_all = _calendar_struct.calendar_data.user_events;
	user_events_rep = _calendar_struct.calendar_data.user_rep;
	member_event_dict = _calendar_struct.calendar_data.member_events;
	for(var i =0; i < member_event_dict.length; i++){
		var curr_dict = member_event_dict[i];
		// console.log("curr_dict", curr_dict);
		for(var j=0; j < curr_dict.participating_events.length; j++){
			member_events_all.push(curr_dict.participating_events[j]);
		}
		for (var j = 0; j < curr_dict.repeat_events.length; j++) {
			member_events_rep.push(curr_dict.repeat_events[j]);
		}
	}
	for(var i = 0; i < user_events_rep.length; i++){
		var rep_split = repeatToAllEvents(user_events_rep[i]);
		for(var j = 0; j < rep_split.length; j++){
			user_events_all.push(rep_split[j]);
		}
	}
	for(var i = 0; i < member_events_rep.length; i++){
		var rep_split = repeatToAllEvents(member_events_rep[i]);
		for(var j = 0; j < rep_split.length; j++){
			member_events_all.push(rep_split[j]);
		}
	}

	console.log("user_events_rep", user_events_rep);
	console.log("member_events_rep", member_events_rep);
	console.log("main_renderCalendar", _calendar_struct);
	window.addEventListener("resize", windowResized);
	document.body.addEventListener('click', clickAnywhere, true); 
	switchCalendarView(_cont_id, "month");	
	loadUserEvents();
	loadMemberEvents();
	populateMonthYear();
	populateDay();
	setCurrTime();
	dayWeekUpdate();
	_calendar_mode = calendar_struct.mode;
	console.log("CALENDAR MODE", _calendar_mode);
	populateFriendsSelectDropdown();
	windowResized();
	console.log("member_events_all", member_events_all);
	console.log("calendar_data.member_events",  _calendar_struct.calendar_data.member_events);
	if(_calendar_mode == "FRIEND"){
		var friend_alias = _calendar_struct.calendar_data.member_info[0].alias;
		var temp_id = friend_alias + "_check";
		var invis_div = document.createElement('div');
		invis_div.id = temp_id;
		invis_div.style = "display:none;";
		document.body.appendChild(invis_div);
		member_check_ids.push({"check_id" : temp_id, "alias" : friend_alias});
		checkFriendSelect(temp_id);
	}
}


// -----------------------------------------------------------------

