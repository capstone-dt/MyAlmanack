// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 					EDIT PROFILE INPUT LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

$(document).ready(function() {
  setInterval(
	  () => {
	  	if(valid_alias != previous_valid){
	    	editProfileUpdate();
	  	}
	  },
	  1000
	);
});
function exchangeValues(div_id, form_id){
	var temp_div = document.getElementById(div_id);
	var temp_form = document.getElementById(form_id);
	temp_form.value=temp_div.value;
}
var valid_alias = false;
var previous_valid = true;
function setxalias(){
	var aliasValidation = document.getElementById("aliasValidationId");
	aliasValidation.innerText = "highlight_off";
}
function setcheckalias(){
	var aliasValidation = document.getElementById("aliasValidationId");
	aliasValidation.innerText = "check_circle_outline";
}
function performEditProfileAjax(callback, after){
	var entered_alais = document.getElementById("inputAlias");
	$.ajax({
		url: '/ajax/validate_alias/',
		data: {
		  'alias': entered_alais.value
		},
		dataType: 'json',
		success: function (data) {
		  if (data.is_taken) {
		  	previous_valid = valid_alias;
		  	valid_alias = false;
			setxalias();
		  }else{
		  	previous_valid = valid_alias;
		  	valid_alias = true;
		  	setcheckalias();
		  	callback();
		  }
		  after();
		}
	});
}
function editProfileUpdate(){
	var entered_alais = document.getElementById("inputAlias");
	if(entered_alais.value != "" && entered_alais.value != profile_struct.alias){
		var temp_func = function(){exchangeValues("inputAlias", "id_PIalias");};
		performEditProfileAjax(temp_func, remainderEdit);
	}
}
function remainderEdit(){
	exchangeValues("inputFirstname", "id_PIfirst");
	exchangeValues("inputLastname", "id_PIlast");
	exchangeValues("inputEmail", "id_PIemail");
	var temp_div = document.getElementById("inputBirthday");
	var temp_form = document.getElementById("id_PIbirthday");
	temp_form.value= new Date(temp_div.value).getTime() + "" ;
	exchangeValues("inputPhone", "id_PIphone");
	exchangeValues("inputOrganization", "id_PIorganization");
	exchangeValues("inputDescription", "id_PIdescription");
}
function uploadProfilePicture(){
	var picture_div = document.getElementById("inputProfilePicture");
	var picture_form = document.getElementById("id_PIpicture");
	if(picture_div.files.length > 0){
		var picture_file = picture_div.files[0];
		const reader = new FileReader();
		reader.onload = function(e) {
		picture_form.value = e.target.result;
		var prof_pic_div = document.getElementById("imageDisplay");
		prof_pic_div.setAttribute('src', e.target.result);
		prof_pic_div.style.width = "200px";
		prof_pic_div.style.height = "200px";
		};
		reader.readAsDataURL(picture_file);
	}else{
		picture_form.value = "$";
	}
}
function submitChanges(){
	editProfileUpdate();
	uploadProfilePicture();
	var entered_alais = document.getElementById("inputAlias");
	if(valid_alias || entered_alais.value == profile_struct.alias){
		exchangeValues("inputAlias", "id_PIalias");
		remainderEdit();
		var submit_button = document.getElementById("submitChangesButton");
		submit_button.click();
	}
}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //
// 					EDIT PROFILE DISPLAY LOGIC
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

function limitBirthday(){
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1;
	var yyyy = today.getFullYear() - 18;
	if(dd<10){
	dd='0'+dd
	} 
	if(mm<10){
		mm='0'+mm
	} 
	today = yyyy+'-'+mm+'-'+dd;
	document.getElementById("inputBirthday").setAttribute("max", today);
}
function formatDateHTML(dateObj){
	return dateObj.getFullYear() + "-" + ('0' + (dateObj.getMonth() + 1)).slice(-2) + "-" + ('0' + dateObj.getDate()).slice(-2);
}
function populateFields(){
	if(profile_struct.alias != undefined){
		var first_div = document.getElementById("inputFirstname");
		first_div.value = profile_struct.first_name;
		var last_div = document.getElementById("inputLastname");
		last_div.value = profile_struct.last_name;
		var alias_div = document.getElementById("inputAlias");
		alias_div.value = profile_struct.alias;
		var email_div = document.getElementById("inputEmail");
		email_div.value = profile_struct.email[0];
		var birthday_div = document.getElementById("inputBirthday");
		var jank_date = new Date(Number(profile_struct.birth_date));
		jank_date = new Date(jank_date.setDate(jank_date.getDate() + 1));
		birthday_div.value = formatDateHTML(jank_date);
		var phone_div = document.getElementById("inputPhone");
		phone_div.value = profile_struct.phone_num[0];
		var org_div = document.getElementById("inputOrganization");
		org_div.value = profile_struct.organization;
		var desc_div = document.getElementById("inputDescription");
		desc_div.value = profile_struct.user_desc;
	}
	var prof_pic_div = document.getElementById("imageDisplay");
	var img_div = base64ToImagePassed(profile_struct.profile_picture, prof_pic_div);
	img_div.style.width = "200px";
	img_div.style.height = "200px";
}