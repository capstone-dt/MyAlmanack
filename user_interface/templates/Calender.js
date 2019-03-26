class Event{
				//c has to be greater that 0
				//
				//dateformat : '03/15/1996-21:30 | 03/15/1996-22:30'
				constructor(name, desc,timerange){
					this.name= name;
					this.desc = desc;
					this.list(timerange);
				}
				list(timerange){
					var stringStart = timerange.substring(0,16);
					var stringEnd = timerange.substring(19, timerange.length);
					var starttime = new Date(stringStart);
					var endtime = new Date(stringEnd);
					var list = [];
					var cap = {};
					cap.start = Math.floor((starttime) / 1000);
					cap.end = Math.floor((endtime) / 1000);
					list.push(cap);
					this.list=list;
				}
				
				rep( su, mo, tu, we, th, fr,sa, c, timerange, event_id, user_id){
					var stringStart = timerange.substring(0,16);
					var stringEnd = timerange.substring(19, timerange.length);
					var starttime = new Date(stringStart);
					var endtime = new Date(stringEnd);
					var list = [];
					var cap = {};
					//console.log(starttime);
					//console.log(user_id);
					cap.start = Math.floor((starttime));
					cap.end = Math.floor((endtime));
					cap.event_id= event_id;
					cap.user_id = user_id;
					list.push(cap);
					var pattern = su+mo+tu+we+th+fr+sa; //pattern
					//console.log("pattern :"+pattern);
					var i, j, indexS, indexE;
					var w = parseInt(c, 10) -1;
					//console.log("w is "+w);
					for (i = 0; i < c ; i++){// how many occurances of the pattern
						for (j = 0; j < pattern.length; j++){
							if (pattern.charAt(j)== 1){
								switch(j) {
								  case 0:
								    var tempdateS = new Date(starttime.getTime());
									tempdateS.setDate((starttime.getDate()+((7*i)+1)));
									//console.log("asdasdasd"+tempdateS);
									//console.log(starttime);
									var tempdateE = new Date(endtime.getTime());
									tempdateE.setDate((endtime.getDate()+((7*i)+1)));
									//console.log("is it making it in?" + tempdateS.getDay());
									
									while(tempdateS.getDay() != 0){
										//console.log("did it make it in?" + tempdateS.getDay());
										
										tempdateS.setDate(tempdateS.getDate()+1);
										tempdateE.setDate(tempdateE.getDate()+1);
										//console.log("after "+tempdateS);
									}
									if (tempdateS.getDay() == 0){
										//console.log("Is a sunday");
										var cap = {};
										cap.start = Math.floor((tempdateS));
										cap.end = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.user_id = user_id;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}
									
									break;
								  case 1:
									var tempdateS = new Date(starttime.getTime());
									tempdateS.setDate((starttime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(starttime);
									var tempdateE = new Date(endtime.getTime());
									tempdateE.setDate((endtime.getDate()+((7*i)+1)));
									//console.log("is it making it in?" + tempdateS.getDay());
									
									while(tempdateS.getDay() != 1){
										//console.log("did it make it in?" + tempdateS.getDay());
										
										//console.log("before "+tempdateS);
										tempdateS.setDate(tempdateS.getDate()+1);
										tempdateE.setDate(tempdateE.getDate()+1);
										//console.log("after "+tempdateS);
									}
									if (tempdateS.getDay() == 1){
										//console.log("Is a sunday");
										var cap = {};
										cap.start = Math.floor((tempdateS));
										cap.end = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.user_id = user_id;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}
									
									break;
								  case 2:
									var tempdateS = new Date(starttime.getTime());
									tempdateS.setDate((starttime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(starttime);
									var tempdateE = new Date(endtime.getTime());
									tempdateE.setDate((endtime.getDate()+((7*i)+1)));
									//console.log("num: "+j);
									//console.log("is it making it in?" + tempdateS.getDay());
									while(tempdateS.getDay() != 2){
										//console.log("did it make it in?" + tempdateS.getDay());
										
										//console.log("before "+tempdateS);
										tempdateS.setDate(tempdateS.getDate()+1);
										tempdateE.setDate(tempdateE.getDate()+1);
										//console.log("after "+tempdateS);
									}
									if (tempdateS.getDay() == 2){
										//console.log("Is a sunday");
										var cap = {};
										cap.start = Math.floor((tempdateS));
										cap.end = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.user_id = user_id;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}
									
									break;
								  case 3:
									var tempdateS = new Date(starttime.getTime());
									tempdateS.setDate((starttime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(starttime);
									var tempdateE = new Date(endtime.getTime());
									tempdateE.setDate((endtime.getDate()+((7*i)+1)));
									
									//console.log("is it making it in?" + tempdateS.getDay());
									while(tempdateS.getDay() != 3){
										//console.log("did it make it in?" + tempdateS.getDay());
										
										//console.log("before "+tempdateS);
										tempdateS.setDate(tempdateS.getDate()+1);
										tempdateE.setDate(tempdateE.getDate()+1);
										//console.log("after "+tempdateS);
									}
									if (tempdateS.getDay() == 3){
										//console.log("Is a sunday");
										var cap = {};
										cap.start = Math.floor((tempdateS));
										cap.end = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.user_id = user_id;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}
									
									break;
								  case 4:
									var tempdateS = new Date(starttime.getTime());
									tempdateS.setDate((starttime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(starttime);
									var tempdateE = new Date(endtime.getTime());
									tempdateE.setDate((endtime.getDate()+((7*i)+1)));
									
									//console.log("is it making it in?" + tempdateS.getDay());
									while(tempdateS.getDay() != 4){
										//console.log("did it make it in?" + tempdateS.getDay());
										
										//console.log("before "+tempdateS);
										tempdateS.setDate(tempdateS.getDate()+1);
										tempdateE.setDate(tempdateE.getDate()+1);
										//console.log("after "+tempdateS);
									}
									if (tempdateS.getDay() == 4){
										//console.log("Is a sunday");
										var cap = {};
										cap.start = Math.floor((tempdateS));
										cap.end = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.user_id = user_id;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}
									
									break;
								  case 5:
									var tempdateS = new Date(starttime.getTime());
									tempdateS.setDate((starttime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(starttime);
									var tempdateE = new Date(endtime.getTime());
									tempdateE.setDate((endtime.getDate()+((7*i)+1)));
									//console.log("is it making it in?" + tempdateS.getDay());
									while(tempdateS.getDay() != 5){
										//console.log("did it make it in?" + tempdateS.getDay());
										
										//console.log("before "+tempdateS);
										tempdateS.setDate(tempdateS.getDate()+1);
										tempdateE.setDate(tempdateE.getDate()+1);
										//console.log("after "+tempdateS);
									}
									if (tempdateS.getDay() == 5){
										//console.log("Is a sunday");
										var cap = {};
										cap.start = Math.floor((tempdateS));
										cap.end = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.user_id = user_id;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}
									
									break;
								  case 6:
									var tempdateS = new Date(starttime.getTime());
									tempdateS.setDate((starttime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(starttime);
									var tempdateE = new Date(endtime.getTime());
									tempdateE.setDate((endtime.getDate()+((7*i)+1)));
									//console.log(tempdateE);
									//console.log("is it making it in?" + tempdateS.getDay());
									while(tempdateS.getDay() != 6){
										//console.log("did it make it in?" + tempdateS.getDay());
										
										//console.log("before "+tempdateS);
										tempdateS.setDate(tempdateS.getDate()+1);
										tempdateE.setDate(tempdateE.getDate()+1);
										//console.log("after "+tempdateS);
									}
									if (tempdateS.getDay() == 6){
										//console.log("Is a sunday");
										var cap = {};
										cap.start = Math.floor((tempdateS));
										cap.end = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.user_id = user_id;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}
									
									break;
									
								}
								
							}
						
						}
					
					
					}
					list = list.sort((elemA, elemB) => elemA.start - elemB.start);
					this.list = list;
					return list;
				}
				
			}
			
			class Calendar{
				constructor(name){ 
					this.name = name;
				}
				genGrid(year, month, list){
					var grid = [...Array(6)].map(e => Array(7).fill(null));
					var date = new Date(year, month);
					var month = date.getMonth();
					this.grid = grid;
					var i = date.getDay();
					var tempDateB = date;
					for (; i >= 0 ; i--){ //backwards
						grid[0][i] = {};
						var curr_date = tempDateB.getDate().toString(); 
						var is_curr_month = false;
						var month2 = tempDateB.getMonth();
						if (month == month2){
							is_curr_month = true;
						}
						grid[0][i].date = curr_date;
						grid[0][i].is_curr = is_curr_month;
						tempDateB = new Date(tempDateB.setDate(tempDateB.getDate()-1));
						
					}
					var x, y; //[x][y]
					var tempDateF = date;
					tempDateF = new Date(tempDateF.setDate(tempDateF.getDate()+1));
					for (x =0; x <6; x++){ //forwards
						for (y =0; y <7; y++){
							if (grid[x][y] == null){
								tempDateF = new Date(tempDateF.setDate(tempDateF.getDate()+1));
								grid[x][y] = {};
								var curr_date = tempDateF.getDate().toString();
								var is_curr_month = false;
								var month2 = tempDateF.getMonth();
								
								if (month == month2){
									is_curr_month = true;
								}
								grid[x][y].date = curr_date;
								grid[x][y].is_curr = is_curr_month;
								
							}
						}
					}
				}
				
				events_per_day(list, start, end){
					var ONE_DAY = 86400000;// milliseconds
					var startdate = new Date(start);
					var enddate = new Date(end);
					
					var arrsize = (Math.abs(end - start)/ONE_DAY);
					arrsize = Math.floor(arrsize);
					//console.log("daysss "+arrsize);
					var arr = new Array(arrsize).fill(null);
					//console.log(arr.length);
					var i, j;
					var tempList = [];
					for (i =0; i< list.length; i++){
						for (j =0; j< list[i].length;j++){
							var eventtimeS = (new Date(list[i][j].start)).getTime();
							var eventtimeE = (new Date(list[i][j].end)).getTime();
							if ( startdate.getTime() < eventtimeS && eventtimeS < enddate.getTime() ){
								var distance = Math.floor(Math.abs(eventtimeS - startdate.getTime())/ONE_DAY);
								var event = {};
								event.start = eventtimeS;
								event.end = eventtimeE;
								event.event_id = list[i][j].event_id;
								event.user_id = list[i][j].user_id;
								tempList.push(event);
								if (arr[distance] == null){
									arr[distance] = [];
								}
								arr[distance].push(event);
							}
							
							
						}
					}console.log(arr);
					//console.log(tempList);
				}
				
				freeTime(list, threshold){
					//console.log(list);
					var i, j;	
					var newList = [];
					var user_list = [];
					for (i = 0; i< list.length ; i++){
						for (j = 0; j < list[i].length; j++){
							newList.push(list[i][j]);
							if (user_list.includes(list[i][j].user_id)==false){
								user_list.push(list[i][j].user_id);
							}
						}
						
					}
					
					newList.sort((elemA, elemB) => elemA.start - elemB.start);
					var free = [];
					var struc = [user_list,free]
					for (i =0; i< newList.length-1;i++){
						if (newList[i].end < newList[i+1].start){
							var difference = newList[i+1].start - newList[i].end;
							//console.log("difference: " + difference);
							if (difference > threshold){
								var newTime = {};
								newTime.start = newList[i].end;
								newTime.end = newList[i+1].start;
								free.push(newTime);
							}
							
						}
					}
					//console.log(newList);
					console.log(struc);
					//console.log(startS);
					//console.log(endS);

				}
			}
			
			let soccer = new Event('soccer','soccer practice', '03/15/2019-21:30 | 03/15/2019-22:30');
			console.log(soccer);
			var x = soccer.rep('1','0','1','0','0','0','0','1', '03/15/2019-21:30 | 03/15/2019-22:30', 12345, 56789);
			var y = soccer.rep('1','0','1','1','0','1','0','1', '03/15/2019-20:00 | 03/15/2019-21:00', 32415, 51231);
			var z = soccer.rep('1','1','1','1','1','1','1','1', '03/15/2019-20:00 | 03/15/2019-21:00', 98992, 56273);
			//var z = soccer.rep('0','0','0','1','1','1','1','1', '03/15/2019-16:30 | 03/15/2019-23:00');
			//console.log(x);
			//console.log(y);
			var list = [x,y,z];
			//console.log(list);
			
			//Fri Mar 15 1996 21:30:00 GMT-0500 (Eastern Standard Time) | Fri Mar 15 1996 22:30:00 GMT-0500 (Eastern Standard Time)
			let cal = new Calendar('my calendar');
			cal.genGrid('2019', '02', list);
			cal.events_per_day(list,1551416400000, 1554091200000);
			console.log(cal);
			var threshold = 3600; //1hr
			cal.freeTime(list ,threshold);