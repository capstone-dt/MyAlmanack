class Event{
				//c has to be greater that 0
				//
				//dateformat : '03/15/1996-21:30 | 03/15/1996-22:30'
				constructor(name, desc,start_date, end_date){
					this.name= name;
					this.desc = desc;
				//	this.list(timerange);
				}
				list(timerange){
					var start_datetime = new Date(start_date);
					var end_datetime = new Date(end_date);
					var list = [];
					var cap = {};
					cap.start_date = Math.floor((start_datetime) / 1000);
					cap.end_date = Math.floor((end_datetime) / 1000);
					list.push(cap);
					this.list=list;
				}

				rep( su, mo, tu, we, th, fr,sa, c, start_date,end_date, event_id, participating_users){
					var start_datetime = new Date(start_date);
					var end_datetime = new Date(end_date);
					var list = [];
					var cap = {};
					//console.log(start_datetime);
					//console.log(participating_users);
					cap.start_date = Math.floor((start_datetime));
					cap.end_date = Math.floor((end_datetime));
					cap.event_id= event_id;
					cap.participating_users = participating_users;
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
								    var tempdateS = new Date(start_datetime.getTime());
									tempdateS.setDate((start_datetime.getDate()+((7*i)+1)));
									//console.log("asdasdasd"+tempdateS);
									//console.log(start_datetime);
									var tempdateE = new Date(end_datetime.getTime());
									tempdateE.setDate((end_datetime.getDate()+((7*i)+1)));
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
										cap.start_date = Math.floor((tempdateS));
										cap.end_date = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.participating_users = participating_users;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}

									break;
								  case 1:
									var tempdateS = new Date(start_datetime.getTime());
									tempdateS.setDate((start_datetime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(start_datetime);
									var tempdateE = new Date(end_datetime.getTime());
									tempdateE.setDate((end_datetime.getDate()+((7*i)+1)));
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
										cap.start_date = Math.floor((tempdateS));
										cap.end_date = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.participating_users = participating_users;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}

									break;
								  case 2:
									var tempdateS = new Date(start_datetime.getTime());
									tempdateS.setDate((start_datetime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(start_datetime);
									var tempdateE = new Date(end_datetime.getTime());
									tempdateE.setDate((end_datetime.getDate()+((7*i)+1)));
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
										cap.start_date = Math.floor((tempdateS));
										cap.end_date = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.participating_users = participating_users;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}

									break;
								  case 3:
									var tempdateS = new Date(start_datetime.getTime());
									tempdateS.setDate((start_datetime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(start_datetime);
									var tempdateE = new Date(end_datetime.getTime());
									tempdateE.setDate((end_datetime.getDate()+((7*i)+1)));

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
										cap.start_date = Math.floor((tempdateS));
										cap.end_date = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.participating_users = participating_users;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}

									break;
								  case 4:
									var tempdateS = new Date(start_datetime.getTime());
									tempdateS.setDate((start_datetime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(start_datetime);
									var tempdateE = new Date(end_datetime.getTime());
									tempdateE.setDate((end_datetime.getDate()+((7*i)+1)));

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
										cap.start_date = Math.floor((tempdateS));
										cap.end_date = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.participating_users = participating_users;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}

									break;
								  case 5:
									var tempdateS = new Date(start_datetime.getTime());
									tempdateS.setDate((start_datetime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(start_datetime);
									var tempdateE = new Date(end_datetime.getTime());
									tempdateE.setDate((end_datetime.getDate()+((7*i)+1)));
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
										cap.start_date = Math.floor((tempdateS));
										cap.end_date = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.participating_users = participating_users;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}

									break;
								  case 6:
									var tempdateS = new Date(start_datetime.getTime());
									tempdateS.setDate((start_datetime.getDate()+((7*i)+1)));
									//console.log(tempdateS);
									//console.log(start_datetime);
									var tempdateE = new Date(end_datetime.getTime());
									tempdateE.setDate((end_datetime.getDate()+((7*i)+1)));
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
										cap.start_date = Math.floor((tempdateS));
										cap.end_date = Math.floor((tempdateE));
										cap.event_id= event_id;
										cap.participating_users = participating_users;
										list.push(cap);
										//console.log("list UPDATED: "+list);
									}

									break;

								}

							}

						}


					}
					list = list.sort((elemA, elemB) => elemA.start_date - elemB.start_date);
					this.list = list;
					return list;
				}

			}

			class Calendar{
				constructor(name){
					this.name = name;
				}
				genGrid(year, month){
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
						grid[0][i].unix = Math.floor((tempDateB));
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
								grid[x][y].unix = Math.floor((tempDateF));
								grid[x][y].date = curr_date;
								grid[x][y].is_curr = is_curr_month;

							}
						}
					}//console.log(grid);
				}

				events_per_day(list, start_date, end_date){
					var ONE_DAY = 86400000;// milliseconds
					var start_datedate = new Date(start_date);
					var end_datedate = new Date(end_date);

					var arrsize = (Math.abs(end_date - start_date)/ONE_DAY);
					arrsize = Math.floor(arrsize);
					var arr = new Array(arrsize).fill(null);
					var i, j;
					var tempList = [];
					//for (i =0; i< list.length; i++){//iterate through different users
						for (j =0; j< list.length;j++){//iterate through user's events
							var eventtimeS = (new Date(list[j].start_date)).getTime();
							var eventtimeE = (new Date(list[j].end_date)).getTime();
							if ( start_datedate.getTime() < eventtimeS && eventtimeS < end_datedate.getTime() ){
								var distance = Math.floor(Math.abs(eventtimeS - start_datedate.getTime())/ONE_DAY);
								var event = {};
								event.start_date = eventtimeS;
								event.end_date = eventtimeE;
								event.event_id = list[j].event_id;
								event.participating_users = list[j].participating_users;
								event.canView = false;
								tempList.push(event);
								if (arr[distance] == null){
									arr[distance] = [];
								}
								arr[distance].push(event);
							}


						}return arr;
					}
					//console.log(tempList);
				
				freetime_per_day(list, start_date, end_date){
					var ONE_DAY = 86400000;// milliseconds
					var ONE_MINUTE = 60000;
					list.sort((elemA, elemB) => elemA.start_date - elemB.start_date);
					var arrsize = (Math.abs(end_date - start_date)/ONE_DAY);
					arrsize = Math.floor(arrsize);
					var arr = new Array(arrsize+1).fill(null);
					var newArray = [];
					for (w =0; w < list.length; w++){
						var start_getter = new Date(list[w].start_date);
						start_getter.setHours(0);
						start_getter.setMinutes(0);
						var start_of_day = new Date(start_getter.getTime());
						var end_getter = new Date(list[w].end_date);
						end_getter.setHours(23);
						end_getter.setMinutes(59);
						var end_of_day = new Date(end_getter.getTime());
						var startstruc = {};
						var endstruc = {};
						startstruc.start_date=start_of_day.getTime();
						startstruc.end_date=start_of_day.getTime();
						endstruc.start_date=end_of_day.getTime();
						endstruc.end_date=end_of_day.getTime();
						if (newArray.includes(startstruc)== false){
							newArray.push(startstruc);
						}
						
						newArray.push(list[w]);
						if (newArray.includes(endstruc)== false){
							newArray.push(endstruc);
						}
						
						//console.log(startstruc.start_date);
						//console.log(endstruc.start_date);
						//console.log(newArray);
					}
					list = newArray;
					var freetime = this.freeTime(list,0);
					var freetime_list = freetime[1];
					//console.log(freetime_list);
					var i, j, w, indexS=0, indexE;
					var tempList = [];
					

					
					for (i =0; i< arr.length; i++){//
						var dayUnixS = start_date+(ONE_DAY*i);
						var dayUnixE = start_date+(ONE_DAY*i)+ONE_DAY-ONE_MINUTE;
						var start_datedate = new Date(start_date);
						var end_datedate = new Date(start_date);
							var start_datedate = new Date(start_date);
						var end_datedate = new Date(start_date);
						start_datedate.setDate(start_datedate.getDate() + i);
						start_datedate.setHours(0);
						start_datedate.setMinutes(0);
						//console.log("start_datedate2 "+start_datedate);
						end_datedate.setDate(end_datedate.getDate() + i);
						end_datedate.setHours(23);
						end_datedate.setMinutes(59);
						//console.log("end_datedate2 "+end_datedate);
						var tempdate1 = new Date(dayUnixS);
						var tempdate2 = new Date(dayUnixE);
						//console.log("tempdate1 "+tempdate1);
						//console.log("tempdate2 "+tempdate2);
						if (tempdate1.getHours() != 0){
							tempdate1.setHours(0);
							dayUnixS =  tempdate1.getTime();
						}
						if (tempdate2.getHours() != 23){
							dayUnixE =  tempdate2.getTime();
						}
						if (tempdate2.getDate() != tempdate1.getDate()){
							tempdate2.setDate(tempdate1.getDate());
						}

						//console.log("tempdate1 "+tempdate1);
						//console.log("tempdate2 "+tempdate2);
						//console.log("S "+tempdate1.getHours());
						//console.log("E "+tempdate2.getHours());
						//console.log("S1 "+dayUnixS);
						//console.log("E1 "+dayUnixE);
						for (j=0; j< freetime_list.length;j++){
							if (freetime_list[j].start_date == 0){
								freetime_list[j].start_date ==start_date;
							}
							
							if (start_datedate.getTime() <= freetime_list[j].start_date && freetime_list[j].start_date <= end_datedate.getTime()){
						//console.log("dayUnixSdayUnixS ASDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD");

							//console.log("dayUnixSdayUnixS "+dayUnixS);
							//console.log("dayUnixEdayUnixE "+dayUnixE);
								if (arr[i] == null){
									arr[i] = [];
									if (indexS ==0){
										indexS =i;
									}
									indexE= i;
								}
								if (freetime_list[j].end_date == 99999999999999){
									//console.log("HELLOOOOOO "+i);
								//console.log(freetime_list[j].end_date);
								freetime_list[j].end_date = end_datedate.getTime();
								//console.log("HELLOOOOOOSSSS "+dayUnixE);
								//console.log(freetime_list[j].end_date);
								}
								arr[i].push(freetime_list[j]);
							}
						}
					}
						var a;
					for (a=0; a < arr.length;a++){
						var dayUnixS2 = start_date+(ONE_DAY*a);
						var dayUnixE2 = start_date+(ONE_DAY*i)+ONE_DAY-ONE_MINUTE;
						var tempdate3 = new Date(dayUnixS2);
						var tempdate4 = new Date(dayUnixE2);
						var start_datedate = new Date(start_date);
						var end_datedate = new Date(start_date);
						start_datedate.setDate(start_datedate.getDate() + a);
						start_datedate.setHours(0);
						start_datedate.setMinutes(0);
						//console.log("start_datedate2 "+start_datedate);
						end_datedate.setDate(end_datedate.getDate() + a);
						end_datedate.setHours(23);
						end_datedate.setMinutes(59);
						//console.log("end_datedate2 "+end_datedate);
						if (arr[a] == null && a <indexS){
							var struc = {};
							struc.start_date = start_datedate.getTime();
							struc.end_date = end_datedate.getTime();
							arr[a] =[];
							arr[a].push(struc);
						}
						if (arr[a] == null && a >indexE){
							var struc = {};
							struc.start_date = start_datedate.getTime();
							struc.end_date = end_datedate.getTime();
							arr[a] =[];
							arr[a].push(struc);
						}
					}
					//console.log(indexS);
					//console.log(indexE);
					return arr;
			}

				freeTime(list, threshold){
					var i, j;
					var newList = [];
					var user_list = [];
					//for (i = 0; i< list.length ; i++){//iterate through different users
						for (j = 0; j < list.length; j++){//iterate through user's events
							newList.push(list[j]);
							if (user_list.includes(list[j].participating_users)==false){
								user_list.push(list[j].participating_users);
							}
						}

					

					newList.sort((elemA, elemB) => elemA.start_date - elemB.start_date);
					var free = [];

					for (i =0; i< newList.length-1;i++){

						if (i==0){
							var newTime = {};
								newTime.start_date = 0;
								newTime.end_date = newList[i].start_date;
								free.push(newTime);
						}
						if (i== newList.length-2){
							var newTime = {};
								newTime.start_date = newList[i+1].end_date;
								newTime.end_date = 99999999999999;
								free.push(newTime);
						}
						if (newList[i].end_date < newList[i+1].start_date){
							var difference = newList[i+1].start_date - newList[i].end_date;
							//console.log("difference: " + difference);
							if (difference >= threshold){               // 0 == no threshold so return any
								var newTime = {};
								newTime.start_date = newList[i].end_date;
								newTime.end_date = newList[i+1].start_date;
								free.push(newTime);
							}

						}
					}
					var struc = [user_list,free]
					//console.log(struc);
					return struc;
				}

				conflict (event, list){//make sure event is not before or after the list's start_date date and end_date date
															//to avoid conflicts
					var freetime_user_list = this.freeTime(list, 0)[0];
					var freetime_list = this.freeTime(list, 0)[1];
					var start_date = event.start_date;
					var end_date = event.end_date;
					var index1=0, index2=0;
					var i, Scheck=false, Echeck=false;
					for (i = 0; i < freetime_list.length; i++){//start_date checker


						if (start_date >= freetime_list[i].start_date && start_date <= freetime_list[i].end_date){
							Scheck = true;
							index1 = i;
						}
					}
					for (i = 0; i < freetime_list.length; i++){//end_date checker
						if (end_date >= freetime_list[i].start_date && end_date <= freetime_list[i].end_date){
							Echeck = true;
							index2 = i;
						}
					}
					if (Scheck == true && Echeck == true && index1 == index2){
						return false; //not conflicting
					}
					return true; //is conflicting


				}

			}

			function test(){
				let soccer = new Event('soccer','soccer practice', 1552685400000,1552692600000);
				//console.log(soccer);
				var x = soccer.rep('1','0','1','0','0','0','0','1', 1552685400000,1552692600000, 12345, [56789,51231]);
				var y = soccer.rep('1','0','1','1','0','1','0','1', 1552680000000,1552683600000, 32415, [51231]);
				var z = soccer.rep('1','1','1','1','1','1','1','1', 1552680000000,1552683600000, 98992, [56789,12345,56273]);
				//var z = soccer.rep('0','0','0','1','1','1','1','1', '03/15/2019-16:30 | 03/15/2019-23:00');
				//console.log(x);
				//console.log(y);
				var list = [x,y,z];
				var list1 = [];
				var i,j;
				for (i = 0; i< list.length ; i++){//iterate through different users
						for (j = 0; j < list[i].length; j++){//iterate through user's events
					list1.push(list[i][j]);
				}
				}
				//console.log("list");
				//console.log(list);
				//console.log("list1");
				//console.log(list1);


				//Fri Mar 15 1996 21:30:00 GMT-0500 (Eastern Standard Time) | Fri Mar 15 1996 22:30:00 GMT-0500 (Eastern Standard Time)
				let cal = new Calendar('my Calendar');
				cal.genGrid('2019', '02');
				var perday = cal.events_per_day(list1,1551416400000, 1554091200000);
				//console.log(cal);
				//console.log("perday");
				//console.log(perday);
				var event = {};
				//1552862056000
				//1552867159500
				event.start_date = 1551416400000;
				event.end_date = 1552684400000;
				var bool = cal.conflict (event, list1);
				//console.log(bool);
				var threshold = (0); //1hr = 12323600
				var freetime = cal.freeTime(list1 ,threshold);
				//console.log("freetime this:");
				//console.log(freetime);
				//console.log("freetime21231 : ");
				console.log(cal.freetime_per_day(list1,1551416400000,1554091200000 ))
			}
