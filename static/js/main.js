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