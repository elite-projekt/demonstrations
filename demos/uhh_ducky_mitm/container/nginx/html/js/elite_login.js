var translation = undefined;

async function getTranslations() {
    const response = await fetch('http://127.0.0.1:5000/orchestration/data/demo/uhh_ducky_mitm/translations');
    const json = await response.json();
    console.log(json);
    return json.translations;
  }
  getTranslations().then(t => {
    translation = t;

  document.getElementById("container").innerHTML =`
			<div class="row">
			<div class="col-md-6">
				<img src="images/undraw_remotely_2j6y.svg" alt="Image"
				class="img-fluid">
			</div>
			<div class="col-md-6 contents">
				<div class="row justify-content-center">
				<div class="col-md-8">
					<div class="mb-4">
          <h4>${translation.nimbus_login_header}<br>Nimbus Account-Services</h3>
          <p class="mb-4 small">${translation.nimbus_login_text}</p>
					</div>
					<form autocomplete="off" action="#" onsubmit="return submit_form(this)">

					<div class="form-group first" id="name_field">
            <label for="name">${translation.nimbus_username}</label>
						<input type="text" class="form-control" id="name" name="uname" value ="internal3495">

					</div>
					<div class="form-group" id="password_field">

            <label for="password">${translation.nimbus_password}</label>
						<div class="input-group">
						<input type="password" class="form-control" id="password" name="psw" value="tzmupMsHlbyYKjRdbE2dvjutzJzfTajhTd4lif26csi8HWKa5XMXz9Rsu4UlB0UrN9JD">
						<i toggle="#password" class="icon-eye toggle-passwort input-group-addon" data-toggle="tooltip"
							data-placement="right" title="Klicken Sie auf das Auge, um das Passwort anzuzeigen."
							id="pw-eye"></i>
						</div>

					</div>
					<div role="alert" aria-live="assertive" aria-atomic="true" class="toast {{classes}} dont-display mt-3"
						data-autohide="false" id=toast>
						<div class="toast-header">
						<strong class="mr-auto">Nimbus</strong>
						<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						</div>
					</div>
					<input type="submit" value="Anmelden" class="btn btn-block btn-primary mt-3">
          </form>
				</div>
				</div>
			</div>
			</div>
    `;
  });



function submit_form(theForm) {
  let attacked = false;
  let user = theForm.uname.value;
  let pw = theForm.psw.value;
  document.getElementById("loading-screen").style.display = "block";
  document.getElementById("container").style.display = "none";
  let loadingText = document.getElementById("loading-text");
  let count = 0;
  let timer = setInterval(function() {
  count++;
    loadingText.innerHTML = `${translation.uhh_web_loading} ${count}%`;
  if (count >= 100) {
    clearInterval(timer);
    loadingText.innerHTML = translations.uhh_web_loading_error;
    }
  }, 500);

  if (attacked) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `http://127.0.0.1:5000/orchestration/start/demo/uhh_ducky_mitm/login`);
    xhr.setRequestHeader("Content-Type", "application/json");
    let json_data = JSON.stringify({"user": user, "pw": pw});
    console.log("Sending");
    console.log(json_data);
    xhr.send(json_data);
  }


	return false;
}
