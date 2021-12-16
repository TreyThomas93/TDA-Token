document.addEventListener("DOMContentLoaded", function () {
  callAccounts();

  // GET BUTTONS
  let add_user_button = document.querySelector("#add-user-btn");
  let add_update_account_button = document.querySelector(
    "#add-update-account-btn"
  );
  let exit_add_user_popup = document.querySelector("#exit-add-user-popup");
  let exit_add_update_account_popup = document.querySelector(
    "#exit-add-update-account-popup"
  );
  let add_user_save_button = document.querySelector("#add-user-save-btn");
  let add_update_account_save_button = document.querySelector(
    "#add-update-account-save-btn"
  );

  // LISTEN FOR CLICKS AND CALL FUNCTIONS
  add_user_button.addEventListener("click", openPopup);
  add_update_account_button.addEventListener("click", openPopup);
  exit_add_user_popup.addEventListener("click", closePopup);
  exit_add_update_account_popup.addEventListener("click", closePopup);

  // SAVE ADD USER DATA
  add_user_save_button.addEventListener("click", sendFormData);

  // SAVE ADD/UPDATE ACCOUNT DATA
  add_update_account_save_button.addEventListener("click", sendFormData);
});

function openPopup(e) {
  if (e.target.id === "add-user-btn") {
    document.querySelector("#add-user-popup").style.display = "block";
  } else {
    document.querySelector("#add-update-account-popup").style.display = "block";
  }
}

function closePopup(e) {
  if (
    e.target.id === "exit-add-user-popup" ||
    e.target.id === "add-user-save-btn"
  ) {
    document.querySelector("#add-user-popup").style.display = "none";
  } else {
    document.querySelector("#add-update-account-popup").style.display = "none";
  }
}

function sendFormData(e) {
  e.preventDefault();

  var elements = e.target.parentElement;

  var form_data = {};

  var password = null;

  for (var ipt of elements) {
    if (ipt.value === "") {
      alert("Error: All Fields Must Have A Value.");

      return;
    }

    if (ipt.name === "Password") password = ipt.value;

    if (ipt.name === "Confirm_Password") {
      if (ipt.value !== password) {
        alert("Passwords Do Not Match.");

        return;
      }

      continue;
    }

    if (ipt.value === "Submit") continue;

    form_data[ipt.name] = ipt.value;
  }

  eel.fetchFormData(form_data);

  closePopup(e);
}

eel.expose(response);
function response(response) {
  if (response["error"]) {
    alert(response["error"]);
    return;
  } else alert(response["success"]);

  callAccounts();
}

function callAccounts() {
  eel.callAccounts();
}

eel.expose(fetchAccounts);
function fetchAccounts(accounts) {
  // CREATE CARD ELEMENTS FOR ACCOUNTS
  let accounts_container = document.querySelector("#accounts-container");

  elements = "";
  accounts.forEach((account) => {
    for (const key of Object.keys(account)) {
      let status = account[key]["Active"] === true ? "Active" : "Inactive";

      let refresh_exp = new Date(
        account[key]["refresh_exp_date"]
      ).toDateString();

      let current_date = new Date().toDateString();

      let expired = false;

      // IF CURRENT DATE IS PAST REFRESH EXP
      if (refresh_exp < current_date) {
        expired = true;
      } else expired = false;

      elements += `
      <div class="card">
        <h5>Account ID: ${key}</h5>

        <div class="inner-div">
          <label>Refresh Token Expiration: ${
            account[key]["refresh_exp_date"]
          }</label>
          <label>Account Status: ${status}</label>
        </div>

        <div class="${expired ? "expired" : "not-expired"}">
          <h1>EXPIRED</h1>
        </div>
      </div>
    `;
    }
  });
  accounts_container.innerHTML = elements;
}
