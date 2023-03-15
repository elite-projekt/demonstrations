function stop_demo () {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `http://127.0.0.1:5000/orchestration/stop/demo/uhh_ducky_mitm`);
    xhr.send();
}

var translation = undefined;

async function getTranslations() {
    const response = await fetch('http://127.0.0.1:5000/orchestration/data/demo/uhh_ducky_mitm/translations');
    const json = await response.json();
    console.log(json);
    return json.translations;
  }
  getTranslations().then(t => {
    translation = t;

let html = `<h1>Gestohlene Zugangsdaten</h1>
<table id="data-table">
      <thead>
        <tr>
          <th>${translation.nimbus_username}</th>
          <th>${translation.nimbus_password}</th>
        </tr>
      </thead>
      <tbody>
        <!-- Data rows will be added dynamically by the JavaScript function -->
      </tbody>
</table>
<div id="text"></div>
`;


  let end_button = `
<button type="button" onclick="stop_demo()" style="width: 20%;" class="btn">
  <span class="align-middle btn btn-block btn-primary mt-3">${t.uhh_web_status_button}</span>
</button>
`
  let info_string_evil=`
  <p> ${t.uhh_web_table_before_link} <a href="https://nimbus.de">${t.uhh_web_table_link}</a> ${t.uhh_web_table_after_link} </p>
  <p> ${t.uhh_web_status_before_button} </p>
  <p> ${end_button} </p>
  <p> ${t.uhh_web_status_after_button} </p>
  <p>
    <img src="images/about_connection_secure.png" alt="Secure connection">
    <img src="images/open_cert.png" alt="Secure connection">
 </p>
 <img src="images/cert.png" alt="Secure connection">
  <p> ${t.uhh_web_status_after_images} </p>
    `;



  function updateTable() {
  // create XHR object
  var xhr = new XMLHttpRequest();

  // define function to be executed when response is received
    xhr.onreadystatechange = function() {
    // check if request is complete and response is OK
    if (this.readyState === 4 && this.status === 200) {
      // parse response as JSON
      var data = JSON.parse(this.responseText);

      // get reference to table and tbody elements
      var table = document.getElementById("data-table");
      var tbody = table.getElementsByTagName("tbody")[0];

      // clear existing table rows
      tbody.innerHTML = "";

      // loop through each data entry
      data.credentials.forEach(function(entry) {
        var username = entry[0];
        var password = entry[1];

        // create new row and cells for username and password
        var row = tbody.insertRow(0);
        var usernameCell = row.insertCell(0);
        var passwordCell = row.insertCell(1);

        // add data to cells
        usernameCell.innerHTML = username;
        passwordCell.innerHTML = password;

        // set row ID to username
        row.id = username;
      });
    }
  };

  // set request parameters
  xhr.open("GET", "http://127.0.0.1:5000/orchestration/data/demo/uhh_ducky_mitm", true);

  // send request
  xhr.send();

  // call function again after one second
  setTimeout(updateTable, 1000);
}
updateTable();

  let content = document.getElementById("content");
  content.innerHTML = html;

  let text_elem = document.getElementById("text");
  text_elem.innerHTML = `
    <div class="centered-text">
      ${info_string_evil}
    </div>`;

});

