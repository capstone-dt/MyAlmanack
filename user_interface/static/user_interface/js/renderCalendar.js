//Adds numbers based on the dimensions passed
var _cont_id = "cal_grid_cont";
var _switchType = "month";
var _select_class = "calSelect";
var _select_id = "";
var headerArray_top = [];
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
var _month_selected = "April";
var _year_selected = "2019";
var _day_selected = "1";


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
			break;
		default:
			elongateHeader();
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

function makeList(cont_id){
	console.log("makeList");
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
	var doFocus = false;
	if(switchType === _switchType){
		doFocus = false;
	}else{
		doFocus = true;
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
		}
		if(doFocus == true){
			focusCalendar();
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
function focusCalendar(){
	var cal_head = document.getElementById("cal_head_text");
	var bound = cal_head.getBoundingClientRect();
	if(_switchType === "month"){
		window.scrollTo(0, bound.top);
		return;
	}
	window.scrollTo(0, bound.top + 100);
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
	ret_div.className = "col-1 defLeftHeaderClass";
	ret_div.id = ret_div.className + ":" + row_index;
	var str_to = row_index + "";
	if(str_to.length != 2){
		str_to = "0" + str_to;
	}
	ret_div.innerHTML = str_to;
		return ret_div;
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
		focusCalendar();
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
function fillMonthViewNumbers(){
	var count = 0;
	for (var i = 0; i < calArray.length; i++) {
		for(var j = 0; j < calArray[i].length; j++){
			textInputCalbox(i, j, count + "");
			count++;
		}
	}
}
function textInputCalbox(row_index, col_index, textInput){
	var curr_div = coordinates_to_div(row_index, col_index);
	curr_div.innerHTML = textInput;
	// console.log(curr_div);
}

// -----------------------------------------------------------------
// DRAW EVENTS

function drawEventSafe_d(time_start, length, event_id){
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
	drawEventUnsafe_d(time_start, c_length, event_id);
}
function drawEventSafe_w(start_col, end_col, time_start, length, event_id){
	if(containsID_w(event_id)){
		console.log("Event already exists. Try modifying it instead.");
		return;
	}
	var c_length = length;
	if(length + time_start > 24){
		c_length = 24 - time_start;
	}
	var d_length = end_col - start_col;
	if(d_length < 0){
		d_length = 1;
	}
	if(d_length + start_col > 7){
		d_length = 7 - start_col;
	}
	drawEventUnsafe_w(start_col, d_length, time_start, c_length, event_id);
}
function drawEventSafe_m(start, end, event_id){
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
		drawEventUnsafe_m(curr_start, width, curr_struct.flags, event_id);
	}
}
function drawEventUnsafe_d_s(curr_struct){
	drawEventUnsafe_d(curr_struct.start_time, curr_struct.length, curr_struct.event_id);
}
function drawEventUnsafe_w_s(curr_struct){
	drawEventUnsafe_w(curr_struct.start, curr_struct.day_width, curr_struct.start_time, curr_struct.length, curr_struct.event_id);
}
function drawEventUnsafe_m_s(curr_struct){
	drawEventUnsafe_m(curr_struct.start, curr_struct.day_width, curr_struct.flags, curr_struct.event_id);
}
function drawEventUnsafe_d(start_time, length, event_id){
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
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_id + ");" );
	document.body.appendChild(divToAdd);
	eventDivArray.push(divToAdd);
	var new_struct = {
		start_time:start_time,
		length:length, 
		event_id:event_id
	};
	var contains = containsStruct_d(new_struct);
	if(contains == false){
		populatedEvents_d.push(new_struct);
		console.log(populatedEvents_d);
	}
}
function drawEventUnsafe_w(start, day_width, start_time, length, event_id){
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
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_id + ");" );
	document.body.appendChild(divToAdd);
	eventDivArray.push(divToAdd);
	var new_struct = {
		start:start, 
		day_width:day_width,
		start_time:start_time,
		length:length, 
		event_id:event_id
	};
	var contains = containsStruct_w(new_struct);
	if(contains == false){
		populatedEvents_w.push(new_struct);
		console.log(populatedEvents_w);
	}
}
function drawEventUnsafe_m(start, day_width, flags, event_id){
	var coords = getRowCol(start);
	var ref_week = divRowsArray[coords.row];
	var rect = ref_week.children[coords.col].getBoundingClientRect();
	console.log("ref_week");
	console.log(ref_week);
	var col_width = rect.width;
	var x_perc = 0.10;
	var x_offset_px = x_perc * col_width;
	var x_offset_px_l = 0;
	var x_offset_px_r = 0;
	var y_perc = 0.30;
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
	divToAdd.style = "position:absolute; background-color:blue; z-index:2; height:20px; cursor:pointer;"
	+ "top:" + (rect.top + y_offset_px + window.scrollY) + "px;" 
	+ "left:" + (rect.left + x_offset_px_l) + "px;" 
	+ "width:" + width + "px;";
	divToAdd.setAttribute( "onClick", "javascript: eventClicked(" + event_id + ");" );
	document.body.appendChild(divToAdd);
	eventDivArray.push(divToAdd);
	var new_struct = {start:start, day_width:day_width, flags:flags, event_id:event_id};
	var contains = containsStruct(new_struct);
	if(contains == false){
		populatedEvents.push(new_struct);
		console.log(populatedEvents);
	}
	console.log(divToAdd);
}
function eventClicked(event_id){
	console.log("eventClicked:" + event_id);
}

// CONATINS

function containsID_d(event_id){
	var contains = false;
	for(var i = 0; i < populatedEvents_d.length; i++){
		if(populatedEvents_d[i].event_id == event_id){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsID_w(event_id){
	var contains = false;
	for(var i = 0; i < populatedEvents_w.length; i++){
		if(populatedEvents_w[i].event_id == event_id){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsID(event_id){
	var contains = false;
	for(var i = 0; i < populatedEvents.length; i++){
		if(populatedEvents[i].event_id == event_id){
			contains = true;
			break;
		}
	}
	return contains;
}
function containsStruct(curr_struct){
	var contains = false;
	for(var i = 0; i < populatedEvents.length; i++){
		if(populatedEvents[i].event_id == curr_struct.event_id && 
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
		if(populatedEvents_w[i].event_id == curr_struct.event_id && 
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
		if(populatedEvents_d[i].event_id == curr_struct.event_id && 
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
	var populatedEvents_c = populatedEvents.slice(0);
	for (var i = 0; i < populatedEvents_c.length; i++) {
		drawEventUnsafe_m_s(populatedEvents_c[i]);
	}
}
// -----------------------------------------------------------------


function mainProf(){
	window.addEventListener("resize", windowResized);
	switchCalendarView(_cont_id, "month");
}