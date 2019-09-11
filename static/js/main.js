/***
 *Validation funtions for forms within the application 
 * 
 */

function validateLoginForm() {
  var login_name_value = document.forms["loginForm"]["username"].value;
  if (login_name_value == "") {
    alert("You must fill in a user name");
    return false;
  }
}

function validateLocationForm() {
  var location_name_value = document.forms["locationForm"]["location_name"].value;
  if (location_name_value == "") {
    alert("Location name must be filled out");
    return false;
  }
}

function validateUserForm() {
  var name_value = document.forms["userForm"]["name"].value;
  var user_name_value = document.forms["userForm"]["user_name"].value;
  var dob_value = document.forms["userForm"]["dob"].value;
  if (name_value == "") {
    alert("Name must be filled out");
    return false;
  }
  if (user_name_value == "") {
    alert("Username must be filled out");
    return false;
  }
  if (dob_value == "") {
    alert("DOB must be filled out");
    return false;
  }
}

function validatePlaceNameForm() {
  var location_value = document.forms["placeNameForm"]["location"].value;
  var eng_name_value = document.forms["placeNameForm"]["eng_name"].value;
  var irl_name_value = document.forms["placeNameForm"]["irl_name"].value;
  var irl_meaning_value = document.forms["placeNameForm"]["irl_meaning"].value;

  if (location_value == "") {
    alert("Location must be selected");
    return false;
  }
  if (eng_name_value == "") {
    alert("English name must be filled out");
    return false;
  }
  if (irl_name_value == "") {
    alert("Irish name must be filled out");
    return false;
  }
  if (irl_meaning_value == "") {
    alert("Irish Meaning must be filled out");
    return false;
  }
}
