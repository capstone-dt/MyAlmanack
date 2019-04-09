class Event{
				//c has to be greater that 0
				//
				//dateformat : '03/15/1996-21:30 | 03/15/1996-22:30'
				constructor(name, desc,start, end){
					this.name= name;
					this.desc = desc;
				//	this.list(timerange);
				}
				list(timerange){
					var starttime = new Date(start);
					var endtime = new Date(end);
					var list = [];
					var cap = {};
					cap.start = Math.floor((starttime) / 1000);
					cap.end = Math.floor((endtime) / 1000);
					list.push(cap);
					this.list=list;
				}

				rep( su, mo, tu, we, th, fr,sa, c, start,end, event_id, user_id){
					var starttime = new Date(start);
					var endtime = new Date(end);
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
					}console.log(grid);
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
					for (i =0; i< list.length; i++){//iterate through different users
						for (j =0; j< list[i].length;j++){//iterate through user's events
							var eventtimeS = (new Date(list[i][j].start)).getTime();
							var eventtimeE = (new Date(list[i][j].end)).getTime();
							if ( startdate.getTime() < eventtimeS && eventtimeS < enddate.getTime() ){
								var distance = Math.floor(Math.abs(eventtimeS - startdate.getTime())/ONE_DAY);
								var event = {};
								event.start = eventtimeS;
								event.end = eventtimeE;
								event.event_id = list[i][j].event_id;
								event.user_id = list[i][j].user_id;
								event.canView = false;
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
				freetime_per_day(list, start, end){
					var ONE_DAY = 86400000;// milliseconds
					var startdate = new Date(start);
					var enddate = new Date(end);
					list.sort((elemA, elemB) => elemA.start - elemB.start);
					var arrsize = (Math.abs(end - start)/ONE_DAY);
					arrsize = Math.floor(arrsize);
					//console.log("daysss "+arrsize);
					var arr = new Array(arrsize).fill(null);
					//console.log(arr.length);
					var freetime = this.freeTime(list,0);
					console.log("%%freetime%%");
					console.log(freetime);
					var freetime_list = freetime[1];
					console.log(freetime_list);
					var i, j, indexS=0, indexE;
					var tempList = [];
					for (i =0; i< arr.length; i++){//
						var dayUnixS = start+(86400000*i);
						var dayUnixE = start+(86400000*i)+86400000;
						console.log(dayUnixS);
						console.log(dayUnixE);
						for (j=0; j< freetime_list.length;j++){
							if (freetime_list[j].start == 0){
								freetime_list[j].start ==freetime_list[j].end-86400000;
							}
							if (freetime_list[j].end == 9999999999999999999){
								indexE= j;
								freetime_list[j].end == freetime_list[j].start+86400000;
							}
							if (dayUnixS < freetime_list[j].start && freetime_list[j].start < dayUnixE){
								if (arr[i] == null){
									arr[i] = [];
									if (indexS ==0){
										console.log("ASDaSFAWRASFAS");
										console.log("ASDaSFAWRASFAS   "+i);
										console.log("ASDaSFAWRASFAS    IN "+indexS);
										indexS =i;
									}
								}
								arr[i].push(freetime_list[j]);
							}
						}
					}
						var a;
					for (a=0; a < arr.length;a++){
						console.log(a);
						var dayUnixS = start+(86400000*a);
						var dayUnixE = start+(86400000*a)+86400000;
						console.log("indexS "+indexS);
						console.log("indexE "+indexE);
						if (arr[a] == null && a <indexS){
							var struc = {};
							struc.start = dayUnixS;
							struc.end = dayUnixE;
							arr[a] =struc;
						}
						if (arr[a] == null && a >indexE){
							var struc = {};
							struc.start = dayUnixS;
							struc.end = dayUnixE;
							arr[a] =struc;
						}
					}
				
					return arr;
			}

				freeTime(list, threshold){
					//console.log(list);
					var i, j;
					var newList = [];
					var user_list = [];
					for (i = 0; i< list.length ; i++){//iterate through different users
						for (j = 0; j < list[i].length; j++){//iterate through user's events
							newList.push(list[i][j]);
							if (user_list.includes(list[i][j].user_id)==false){
								user_list.push(list[i][j].user_id);
							}
						}

					}

					newList.sort((elemA, elemB) => elemA.start - elemB.start);
					var free = [];

					for (i =0; i< newList.length-1;i++){

						if (i==0){
							var newTime = {};
								newTime.start = 0;
								newTime.end = newList[i].start;
								free.push(newTime);
						}
						if (i== newList.length-2){
							var newTime = {};
								newTime.start = newList[i+1].end;
								newTime.end = 9999999999999999999;
								free.push(newTime);
						}
						if (newList[i].end < newList[i+1].start){
							var difference = newList[i+1].start - newList[i].end;
							//console.log("difference: " + difference);
							if (difference > threshold){               // 0 == no threshold so return any
								var newTime = {};
								newTime.start = newList[i].end;
								newTime.end = newList[i+1].start;
								free.push(newTime);
							}

						}
					}
					var struc = [user_list,free]
					//console.log(newList);
					console.log(struc);
					//console.log(startS);
					//console.log(endS);
					return struc;
				}

				conflict (event, list){//make sure event is not before or after the list's start date and end date
															//to avoid conflicts
					var freetime_user_list = this.freeTime(list, 0)[0];
					var freetime_list = this.freeTime(list, 0)[1];
				//	console.log("this the freetime conflict ");
					//console.log(freetime_list);
					var start = event.start;
					var end = event.end;
					var index1=0, index2=0;
					var i, Scheck=false, Echeck=false;
					for (i = 0; i < freetime_list.length; i++){//start checker
					console.log(i);
					console.log("in list S: "+new Date (freetime_list[i].start));
					console.log("in list E: "+new Date (freetime_list[i].end));
					console.log(" given S : "+new Date (start));
					console.log(" given E : "+new Date (end));


						if (start >= freetime_list[i].start && start <= freetime_list[i].end){
							Scheck = true;
							index1 = i;
							console.log("here "+index1);
						}
					}
					for (i = 0; i < freetime_list.length; i++){//end checker
					console.log(i);
						if (end >= freetime_list[i].start && end <= freetime_list[i].end){
							Echeck = true;
							index2 = i;
							console.log("here "+index2);
						}
					}
					if (Scheck == true && Echeck == true && index1 == index2){
						return false; //not conflicting
					}
					return true; //is conflicting
					console.log(freetime_user_list);
					console.log(freetime_list);


				}

			}

			function test(){
				let soccer = new Event('soccer','soccer practice', 1552685400000,1552692600000);
				console.log(soccer);
				var x = soccer.rep('1','0','1','0','0','0','0','1', 1552685400000,1552692600000, 12345, 56789);
				var y = soccer.rep('1','0','1','1','0','1','0','1', 1552680000000,1552683600000, 32415, 51231);
				var z = soccer.rep('1','1','1','1','1','1','1','1', 1552680000000,1552683600000, 98992, 56273);
				//var z = soccer.rep('0','0','0','1','1','1','1','1', '03/15/2019-16:30 | 03/15/2019-23:00');
				//console.log(x);
				//console.log(y);
				var list = [x,y,z];
				//console.log(list);

				//Fri Mar 15 1996 21:30:00 GMT-0500 (Eastern Standard Time) | Fri Mar 15 1996 22:30:00 GMT-0500 (Eastern Standard Time)
				let cal = new Calendar('my calendar');
				cal.genGrid('2019', '02');
				cal.events_per_day(list,1551416400000, 1554091200000);
				console.log(cal);
				var event = {};
				//1552862056000
				//1552867159500
				event.start = 1551416400000;
				event.end = 1552684400000;
				var bool = cal.conflict (event, list);
				console.log(bool);
				var threshold = (0); //1hr = 12323600
				var freetime = cal.freeTime(list ,threshold);
				console.log("freetime this:");
				console.log(freetime);
				console.log(cal.freetime_per_day(list,1551416400000,1554091200000 ))
			}
