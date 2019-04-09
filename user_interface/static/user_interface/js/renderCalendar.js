//Adds numbers based on the dimensions passed
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
var _days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
var _days_of_week_abv = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"];
var _days_of_week_abv_abv = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
var _months_of_year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var _times_of_day_12 = ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"];
var _month_selected = "03";
var _year_selected = "2019";
var _day_selected = "1";
var _week_selected = [];
var _curr_month = "currMonth";
var _curr_month_not = "currMonthNot";
var _dummy_events_json;
var _dummy_profiles_json;
var _dummy_contacts_json;
var _dummy_user_json;

var user_contact_list;
var user_events_all = [];
var user_color = "rgba(114,138,255,0.6)";
var member_color = "rgba(128,0,128,0.4)";
var member_events_all = [];
var member_check_ids = [];
// Friends enabled test

/*
JS OUTLINE:
RESIZING
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

function drawColorGrid(isRainbow){
	var retArray = [];
	if(isRainbow == false){
		switchCalendarView(_cont_id, _switchType);
	}
	for(var i = 0; i < calArray.length; i++){
		for(var j = 0; j < calArray[i].length; j++){
			var curr_elem = calArray[i][j];
			if(isRainbow == false){
				curr_elem.style.backgroundColor = "white";
			}else{
				var randNum = Math.random();
				var randColor = getColorForPercentage(randNum);
				console.log(randColor);
				curr_elem.style.backgroundColor =  
					"rgba(" + randColor.red + ", " + randColor.green + ", " 
					+ randColor.blue + ", 0.2)";
			}
			retArray.push(curr_elem);
		}
	}
	return retArray;
}

function friendsEnabled(){
	return false;
}

function makeList(cont_id){
	console.log("makeList");
}

function makeSharedGrid(cont_id, rowClass, colClass, name, ){
	// Overflow x scroll
	// Different tabs for different people
	// Header for each tab
	// Select friends from a list of friends (selective selection)
	// 
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
}
function switchCalendarView(cont_id, switchType){
	var cont_div = document.getElementById(cont_id);
	cont_div.innerHTML = "";
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
		}
}
function clearEvents(){
	for(var i = 0; i < eventDivArray.length; i++){
		var curr_event = eventDivArray[i];
		document.body.removeChild(curr_event);
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
		var curr_filtered = filterAlias(event_array, alias_array[i]);
		for(var j = 0; j < curr_filtered.length; j++){
			retArray.push(curr_filtered[j]);
		}
	}
	return retArray;
}

function getAllEventStructsCurrMonthAlias(alias){
	var allCurr = getAllEventStructsCurrMonth();
	return filterAlias(allCurr, alias);
}
function getAllEventStructsCurrMonth(){
	var retArr = [];
	var month_start = new Date(_year_selected, _month_selected, 1);
	month_start.setHours(0,0,0);
	var start_unix = month_start.getTime();
	var month_end = new Date(_year_selected, _month_selected + 1, 0);
	month_end.setHours(23,59,59);
	var end_unix = month_end.getTime();
	for(var i = 0; i < _dummy_events_json.length; i++){
		var curr_event = _dummy_events_json[i];
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
	var month_start = new Date(_year_selected, _month_selected, 1);
	month_start.setHours(0,0,0);
	var start_unix = month_start.getTime();
	var month_end = new Date(_year_selected, _month_selected + 1, 0);
	month_end.setHours(23,59,59);
	var end_unix = month_end.getTime();
	for(var i = 0; i < populatedEvents.length; i++){
		var curr_event = populatedEvents[i].event_object;
		if(inRange(start_unix, curr_event.start_date, end_unix) || 
			inRange(start_unix, curr_event.end_date, end_unix)){
			retArr.push(populatedEvents[i]);
		}
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
	for(var i = 0; i < user_events.length; i++){
		var curr_event = user_events[i];
		if(inRange(start_unix, curr_event.start_date, end_unix) || 
			inRange(start_unix, curr_event.end_date, end_unix)){
			retArr.push(user_events[i]);
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
	var selected_members = getMembersSelected();
	if(selected_members.length == 0){
		return [];
	}
	var curr_month_members = getEventsCurrMonthMembers();
	var retArray = filterAliasArray(curr_month_members, selected_members);
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
	for(var i= 0; i < populatedEvents.length; i++){
		var curr_event = populatedEvents[i].event_object;
		if(inRange(_week_selected[0].getTime(), curr_event.start_date, _week_selected[1].getTime())
			|| inRange(_week_selected[0].getTime(), curr_event.end_date, _week_selected[1].getTime())){
			retArr.push(curr_event);
		}
	}
	return retArr;
}
function getEventsOnDate(date_obj){
	var beginning_day = new Date(date_obj.getFullYear(), date_obj.getMonth(), date_obj.getDate());
	var end_day = new Date(date_obj.getFullYear(), date_obj.getMonth(), date_obj.getDate());
	end_day.setHours(23,59,59);
	var retArr = [];
	for(var i= 0; i < populatedEvents.length; i++){
		var curr_event = populatedEvents[i].event_object;
		if(inRange(beginning_day.getTime(), curr_event.start_date, end_day.getTime())
			|| inRange(beginning_day.getTime(), curr_event.end_date, end_day.getTime())){
			retArr.push(curr_event);
		}
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
	ret_div.innerHTML = "Tempday ##/##/####";
	return ret_div;
}
function weekDatesHeader(col_index){
	var ret_div = document.createElement('div');
	ret_div.className = "col text-center defTopHeaderClass";
	ret_div.id = ret_div.className + ":" + col_index;
	ret_div.style = "min-width:10px";
	ret_div.innerHTML = _days_of_week[col_index] + "<br/>##";
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
	var month_sel = document.getElementById("month_sel");
	var year_sel = document.getElementById("year_sel");
	month_sel.value = parseMonthi(new_month);
	year_sel.value = new_year;
	_month_selected = new_month;
	_year_selected = new_year;
	populateDay();
	selectDayHard(1);
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}
function dayWeekUpdate(){
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
function leftArrowClick(){
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
			updateMonthYear(_month_selected, _year_selected);
			_day_selected = temp_date.getDate();
			selectDayHard(_day_selected);
			break;
		case "day":
			console.log("left day");
			var temp_date = new Date(_year_selected, parseInt(_month_selected), _day_selected);
			temp_date.setDate(temp_date.getDate() - 1);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			updateMonthYear(_month_selected, _year_selected);
			_day_selected = temp_date.getDate();
			selectDayHard(_day_selected);
			break;
		default:
	}
}
function currButtonClick(){
	switch(_switchType){
		case "month":
			setCurrTime();
			selectDayHard(_day_selected);
			clearEvents();
			switchCalendarView(_cont_id, _switchType);
			addEvents();
			break;
		case "week":
			setCurrTime();
			selectDayHard(_day_selected);
			clearEvents();
			switchCalendarView(_cont_id, _switchType);
			addEvents();
			break;
		case "day":
			setCurrTime();
			selectDayHard(_day_selected);
			clearEvents();
			switchCalendarView(_cont_id, _switchType);
			addEvents();
			break;
		default:
	}
}
function rightArrowClick(){
	switch(_switchType){
		case "month":
			var temp_date = new Date(_year_selected, parseInt(_month_selected) + 1, 1);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			updateMonthYear(_month_selected, _year_selected);
			break;
		case "week":
			console.log("right week");
			var temp_date = new Date(_year_selected, parseInt(_month_selected), _day_selected);
			temp_date.setDate(temp_date.getDate() + 7);
			console.log(temp_date);
			_month_selected = temp_date.getMonth();
			_year_selected = temp_date.getFullYear();
			updateMonthYear(_month_selected, _year_selected);
			_day_selected = temp_date.getDate();
			selectDayHard(_day_selected);
			break;
		case "day":
			console.log("left day");
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
}
function populateFriendsSelectDropdown(){
	var friendsSelectDropdown = document.getElementById("friend_select_dropdown");
	var friends_to_pop = getFriendsUserData();
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
	var check_input = document.getElementById(sel_id);
	if(check_input.checked){
		check_input.checked = false;
		check_input.setAttribute("flag", "false");
	}else{
		check_input.checked = true;
		check_input.setAttribute("flag", "true");
	}
	getMembersSelected();
}

function getMembersSelected(){
	var valid = [];
	for(var i = 0; i < member_check_ids.length; i++){
		var curr_div = document.getElementById(member_check_ids[i].check_id);
		if(curr_div.getAttribute("flag") == "true"){
			valid.push(member_check_ids[i].alias);
		}
	}
	console.log(valid);
	return valid;
}

function getMembersSelectedEvents(){
	var members_selected = getMembersSelected();
	var retArray = [];
	for(var i = 0; i < members_selected.length; i++){
		for(var j = 0; j < member_events_all.length; j++){
			if(member_events_all[j].event_creator_alias == members_selected[i]){
				retArray.push(member_events_all[j]);
			}
		}
	}
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
	switchCalendarView(_cont_id, _switchType);
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
	console.log("select_new:" + select_id);
	toSelect.className += " " + _select_class;
	toSelect.setAttribute("selected", "true");
}
function dayClickM(click_id){
	console.log("dayClick:" + click_id);
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
	drawEventUnsafe_d(time_start, c_length, event_object);
}
function drawEventSafe_w(start_col, end_col, time_start, length, event_object){
	var event_id = event_object.event_id;
	if(containsID_w(event_id)){
		console.log("Event already exists. Try modifying it instead.");
		return;
	}
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
	drawEventUnsafe_w(start_col, d_length, time_start, c_length, event_id);
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
		drawEventUnsafe_m(curr_start, width, curr_struct.flags, event_object);
	}
}
function drawEventSafe_m_color(start, end, event_object, color){
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
		drawEventUnsafe_m_color(curr_start, width, curr_struct.flags, event_object, color);
	}
}
function drawEventUnsafe_d_s(curr_struct){
	drawEventUnsafe_d(curr_struct.start_time, curr_struct.length, curr_struct.event_object);
}
function drawEventUnsafe_w_s(curr_struct){
	drawEventUnsafe_w(curr_struct.start, curr_struct.day_width, curr_struct.start_time, curr_struct.length, curr_struct.event_object);
}
function drawEventUnsafe_m_s(curr_struct){
	drawEventUnsafe_m_color(curr_struct.start, curr_struct.day_width, curr_struct.flags, curr_struct.event_object, curr_struct.event_color);
}
function drawEventUnsafe_d(start_time, length, event_object){
	var start = 0;
	var day_width = 1;
	var day_div = calArray[0][start];
	var rect = day_div.getBoundingClientRect();
	var col_width = rect.width;
	var row_height = rect.height;
	var x_offset_px_l = 10;
	var x_offset_px_r = 10;
	var y_perc = 0.30;
	var y_offset_px = start_time*row_height;
	var width = day_width*col_width - x_offset_px_l - x_offset_px_r;
	var height = row_height*length;
	var divToAdd = document.createElement('div');
	divToAdd.style = "position:absolute; background-color:blue; z-index:2; height:20px; cursor:pointer;"
	+ "top:" + (rect.top + y_offset_px + window.scrollY) + "px;" 
	+ "left:" + (rect.left + x_offset_px_l) + "px;" 
	+ "width:" + width + "px;" 
	+ "height:" + height + "px;";
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_object.event_id + ");" );
	document.body.appendChild(divToAdd);
	eventDivArray.push(divToAdd);
	var new_struct = {
		start_time:start_time,
		length:length, 
		event_object:event_object
	};
	var contains = containsStruct_d(new_struct);
	if(contains == false){
		populatedEvents_d.push(new_struct);
		// console.log(populatedEvents_d);
	}
}
function drawEventUnsafe_w(start, day_width, start_time, length, event_object){
	var day_div = calArray[0][start];
	var rect = day_div.getBoundingClientRect();
	var col_width = rect.width;
	var row_height = rect.height;
	var x_offset_px_l = 10;
	var x_offset_px_r = 10;
	var y_perc = 0.30;
	var y_offset_px = start_time*row_height;
	var width = day_width*col_width - x_offset_px_l - x_offset_px_r;
	var height = row_height*length;
	var divToAdd = document.createElement('div');
	divToAdd.style = "position:absolute; background-color:blue; z-index:2; height:20px; cursor:pointer;"
	+ "top:" + (rect.top + y_offset_px + window.scrollY) + "px;" 
	+ "left:" + (rect.left + x_offset_px_l) + "px;" 
	+ "width:" + width + "px;" 
	+ "height:" + height + "px;";
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_object.event_id + ");" );
	document.body.appendChild(divToAdd);
	eventDivArray.push(divToAdd);
	var new_struct = {
		start:start, 
		day_width:day_width,
		start_time:start_time,
		length:length, 
		event_object:event_object
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
	var y_perc = 0.50;
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
	var divToAdd = document.createElement('div');
	divToAdd.style = "position:absolute; background-color:" + color + "; z-index:2; height:20px; cursor:pointer;"
	+ "top:" + (rect.top + y_offset_px + window.scrollY) + "px;" 
	+ "left:" + (rect.left + x_offset_px_l) + "px;" 
	+ "width:" + width + "px;";
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_object.event_id + ");" );
	document.body.appendChild(divToAdd);
	eventDivArray.push(divToAdd);
	var new_struct = {start:start, 
		day_width:day_width, 
		flags:flags, 
		event_object:event_object,
		event_color:color
	};
	var contains = containsStruct(new_struct);
	if(contains == false){
		populatedEvents.push(new_struct);
		// console.log(populatedEvents);
	}
	// console.log(divToAdd);
}
function populateEventStructure_m(curr_event, color){
	var event_id = curr_event.event_id;
	if(containsID(event_id)){
		console.log("Event already exists. Try modifying it instead.");
		return;
	}
	var temp_start = new Date(Number(curr_event.start_date));
	var temp_end = new Date(Number(curr_event.end_date));
	var day_pos_start = getDayPosition(temp_start.getDate(), temp_start.getFullYear(), temp_start.getMonth());
	var day_pos_end = getDayPosition(temp_end.getDate(), temp_end.getFullYear(), temp_end.getMonth());
	drawEventSafe_m_color(day_pos_start, day_pos_end, curr_event, color);
}


function drawUserEvents_m(){
	// Draw events in blue on calendar

}

function drawMemberEvents_m(){
	// Different color
	// Members to draw
	// Draw the events of those members
	// If event is hidden, draw grey.

}
function drawUserEvents_w(){
	// Draw events in blue on calendar
}

function drawMemberEvents_w(){
	// Different color
	// Members to draw
	// Draw the events of those members
	// If event is hidden, draw grey.
}

function drawUserEvents_d(){
	// Draw events in blue on calendar
}

function drawMemberEvents_d(){
	// Different color
	// Members to draw
	// Draw the events of those members
	// If event is hidden, draw grey.
}








function eventClicked(event_id){
	console.log("eventClicked:" + event_id);
	var temp_struct = getEventStruct(event_id);
	console.log(temp_struct);
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
			populatedEvents[i].day_width == curr_struct.day_width){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsStruct_w(curr_struct){
	var contains = false;
	for(var i = 0; i < populatedEvents_w.length; i++){
		if(populatedEvents_w[i].event_object.event_id == curr_struct.event_object.event_id && 
			populatedEvents_w[i].start == curr_struct.start && 
			populatedEvents_w[i].day_width == curr_struct.day_width){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsStruct_d(curr_struct){
	var contains = false;
	for(var i = 0; i < populatedEvents_d.length; i++){
		if(populatedEvents_d[i].event_object.event_id == curr_struct.event_object.event_id && 
			populatedEvents_d[i].start_time == curr_struct.start_time && 
			populatedEvents_d[i].length == curr_struct.length){
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
}
function addEventsD(){
	var count = 0;
	var populatedEvents_c = populatedEvents_d.slice(0);
	for (var i = 0; i < populatedEvents_c.length; i++) {
		drawEventUnsafe_d_s(populatedEvents_c[i]);
	}
}
function addEventsW(){
	var count = 0;
	var populatedEvents_c = populatedEvents_w.slice(0);
	for (var i = 0; i < populatedEvents_c.length; i++) {
		drawEventUnsafe_w_s(populatedEvents_c[i]);
	}
}
function addEventsM(){
	var count = 0;
	var populatedEvents_c = getEventsCurrMonth();
	for (var i = 0; i < populatedEvents_c.length; i++) {
		drawEventUnsafe_m_s(populatedEvents_c[i]);
	}
}
// -----------------------------------------------------------------

// DUMMY DATA

function getEventStruct(_event_id){
	for(var i = 0; i < _dummy_events_json.length; i++){
		var curr_event = _dummy_events_json[i];
		if(curr_event.event_id == _event_id){
			return curr_event;
		}
	}
}

function loadUserEvents(){
	for(var i = 0; i < user_events_all.length; i++){
		var curr_event = user_events_all[i];
		populateEventStructure_m(curr_event, user_color);
	}
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}
function loadMemberEvents(){
	for(var i = 0; i < member_events_all.length; i++){
		var curr_event = member_events_all[i];
		populateEventStructure_m(curr_event, member_color);
	}
	clearEvents();
	switchCalendarView(_cont_id, _switchType);
	addEvents();
}

function loadUserData(){
	var name_div = document.getElementById("name_display");
	name_div.innerText = _dummy_user_json.first_name + " " + _dummy_user_json.last_name;
	var alias_div = document.getElementById("alias_display");
	alias_div.innerText = "@" + _dummy_user_json.alias;
	var desc_div = document.getElementById("description_display");
	desc_div.innerText = _dummy_user_json.user_desc;
}
function validateEvents(){
	for(var i = 0; i < _dummy_events_json.length; i++){
		var curr_event = _dummy_events_json[i];
		var start_time = new Date(parseInt(curr_event.start_date));
		var end_time = new Date(parseInt(curr_event.end_date));
		console.log("Name:" + curr_event.event_creator_alias);
		console.log("Start:" + start_time);
		console.log("End:" + end_time);
	}
}
function parseQuotesJson(json_string){
	return JSON.parse(json_string.replace(/&quot;/g,'\"').replace(/&#39;/g,"\'"));
}
function loadProfileDummyData(event_data, profile_data, contact_data, user, contact_list){
	_dummy_events_json = parseQuotesJson(event_data);
	_dummy_profiles_json = parseQuotesJson(profile_data);
	_dummy_contacts_json = parseQuotesJson(contact_data);
	_dummy_user_json = parseQuotesJson(user)[0];
	user_contact_list = parseQuotesJson(contact_list);
	console.log(_dummy_events_json, _dummy_profiles_json, _dummy_contacts_json, _dummy_user_json);
	loadUserData();
	validateEvents();
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
function getContactListRow(){
	console.log(_dummy_user_json);
	var contact_list_id = user_contact_list.contact_list_id;
	for(var i = 0; i < _dummy_contacts_json.length; i++){
		var curr_contact = _dummy_contacts_json[i];
		if(contact_list_id == curr_contact.contact_list_id){
			return curr_contact;
		}
	}
	return null;
}
function getFriendsUserData(){
	var contact_list = getContactListRow();
	var contact_names = contact_list.contact_names.split(", ");
	var retArr = [];
	for(var c_index = 0; c_index < contact_names.length; c_index++){
		for(var i = 0; i < _dummy_profiles_json.length; i++){
			var curr_profile = _dummy_profiles_json[i];
			if(curr_profile.alias == contact_names[c_index]){
				retArr.push(curr_profile);
			}
		}
	}
	return retArr;
}
function getFriendsProfilePictures(){
	// stubbed
}

function loadCalendarDataProfile(user_events_data, friend_events_data){
	var user_events_json = parseQuotesJson(user_events_data);
	var friend_events_json = parseQuotesJson(friend_events_data);
	for(var i = 0; i < user_events_json.length; i++){
		user_events_all.push(user_events_json[i]);
	}
	for(var j = 0; j < friend_events_json.length; j++){
		member_events_all.push(friend_events_json[j]);
	}
}


// -----------------------------------------------------------------


function mainProf(){
	window.addEventListener("resize", windowResized);
	switchCalendarView(_cont_id, "month");	
	loadUserEvents();
	loadMemberEvents();
	populateMonthYear();
	populateDay();
	setCurrTime();
	dayWeekUpdate();
	populateFriendsSelectDropdown();
	windowResized();
}
