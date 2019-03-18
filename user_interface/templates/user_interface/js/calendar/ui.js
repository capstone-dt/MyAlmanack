function makeGrid(cont_id, rowClass, colClass, name, dim_x, dim_y, onclick_func){
		var cont_div = document.getElementById(cont_id);
		var children = cont_div.childNodes;
		while (cont_div.hasChildNodes()) {
		    cont_div.removeChild(cont_div.lastChild);
		}
		for(var i=0; i< dim_y; i++){
			var curr_row = document.createElement('div');
			curr_row.className = "row " + rowClass;
			curr_row.id = rowClass + "_r" + i;
			for(var j=0; j < dim_x; j++){
				var curr_col = document.createElement('div');
				curr_col.className = "col " + colClass;
				curr_col.id = name + "_r:" + i + ",c:"+  j; 
				curr_col.onclick = function(){
					onclick_func(this.id);
				};
				curr_row.appendChild(curr_col);
			}
			cont_div.appendChild(curr_row);
		}
	}
	function switchCalendarView(cont_id, switchType){
		var cont_div = document.getElementById(cont_id);
		cont_div.innerHTML = "";
		_switchType = switchType;
		switch(switchType){
			case "day":
				makeGrid(cont_id, "calDayD", "defStyle calHour", "D", 1, 24, hourClickD);
				break;
			case "week":
				makeGrid(cont_id, "calDayW", "defStyle calHour", "W", 7, 24, hourClickW);
				break;
			case "month":
			default:
			makeGrid(cont_id, "calWeek", "defStyle calDay", "M", 7, 6, dayClickM);
		}
	}
	function selectUnique(cont_id, select_id){
		// console.log("select unique:" + select_id + " in <div>:" + cont_id);
		switchCalendarView(_cont_id, _switchType);
		select(select_id);
	}

	function select(select_id){
		var toSelect = document.getElementById(select_id);
		if(toSelect == null){
			return;
		}
		console.log("select_new:" + select_id);
		toSelect.className += " " + _select_class;
		toSelect.setAttribute("selected", "true");
	}

	function dayClickM(click_id){
		console.log("dayClick:" + click_id);
		// console.log("week selected");
		selectUnique(_cont_id, click_id)
		// switchCalendarView(_cont_id, "week");
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