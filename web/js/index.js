document.addEventListener("DOMContentLoaded", function () {
  // GET BUTTONS
  let add_user_button = document.querySelector("#add-user-btn");
  let add_update_account_button = document.querySelector(
    "#add-update-account-btn"
  );
  let exit_add_user_popup = document.querySelector("#exit-add-user-popup");
  let exit_add_update_account_popup = document.querySelector(
    "#exit-add-update-account-popup"
  );

  // LISTEN FOR CLICKS AND CALL FUNCTIONS
  add_user_button.addEventListener("click", openPopup);
  add_update_account_button.addEventListener("click", openPopup);
  exit_add_user_popup.addEventListener("click", closePopup);
  exit_add_update_account_popup.addEventListener("click", closePopup);
});

function openPopup(e) {
  if (e.target.id === "add-user-btn") {
    document.querySelector("#add-user-popup").style.display = "block";
  } else {
    document.querySelector("#add-update-account-popup").style.display = "block";
  }
}

function closePopup(e) {
  if (e.target.id === "exit-add-user-popup") {
    document.querySelector("#add-user-popup").style.display = "none";
  } else {
    document.querySelector("#add-update-account-popup").style.display = "none";
  }
}
