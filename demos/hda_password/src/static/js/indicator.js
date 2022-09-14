requirejs(['static/js/zxcvbn.js'], function (zxcvbn) {
  $(function () {
    $(".password").on('input', function () {
      const small_letter = document.querySelector(".small-letter");
      const capital_letter = document.querySelector(".capital-letter");
      const special_char = document.querySelector(".special-char");
      const pw_length = document.querySelector(".lenght-check");
      const number_char = document.querySelector(".number-char");
      const guessable = document.querySelector(".guessable");
      const indicator = document.querySelector(".indicator");
      const re_password_info = document.querySelector(".re-enter-password");
      const username_info = document.querySelector(".username-info");
      // const input = document.querySelector(".password");
      const input = document.getElementById('password');
      const weak = document.querySelector(".weak");
      const medium = document.querySelector(".medium");
      const strong = document.querySelector(".strong");
      const button = document.querySelector(".register-button");
      const username = document.getElementById('name');
      const reEnterPassword = document.getElementById('re-password');
      regExBool = false;
      passwordComparison = false;
      nameCheck = false;
      result = zxcvbn(input.value);
      let regExpWeak = /[a-z]/;
      let regExpMedium = /\d+/;
      let regExpStrong = /[^a-zA-Z\d\sßäöüÄÖÜ]/; //[^a-zA-Z\d\s]/; ///\W/g /[^a-zA-Z\d\sßäöüÄÖÜ]/
      let regExpCapital = /[A-Z]/;
      if (input.value != "") {
        indicator.style.visibility = "visible";
        indicator.style.display = "block";
        indicator.style.display = "flex";
        if (input.value.length >= 10 && input.value.match(regExpWeak) && input.value.match(regExpMedium) && input.value.match(regExpStrong) && input.value.match(regExpCapital) && result.score == 4){ 
          no = 3;
        } else if (input.value.length >= 6 && ((input.value.match(regExpWeak) && input.value.match(regExpMedium)) || (input.value.match(regExpMedium) && input.value.match(regExpStrong)) || (input.value.match(regExpWeak) && input.value.match(regExpStrong)))){
          no = 2;
        } else if (input.value.length >= 3 && (input.value.match(regExpWeak) || input.value.match(regExpMedium) || input.value.match(regExpStrong))){
          no = 1; 
        } else {
          no = 0;
        }
        if (no === 1) {
          weak.classList.add("active");
          medium.classList.remove("active");
          strong.classList.remove("active");
          regExBool = false;
        } else if (no === 2) {
          weak.classList.add("active");
          medium.classList.add("active");
          strong.classList.remove("active");
          regExBool = false;
        } else if (no === 3) {
          weak.classList.add("active");
          medium.classList.add("active");
          strong.classList.add("active");
          regExBool = true;
        } else if (no === 0) {
          weak.classList.remove("active");
          medium.classList.remove("active");
          strong.classList.remove("active");
          regExBool = false;
        }
        if (input.value === reEnterPassword.value) {
          passwordComparison = true;
        }
      } else {
        indicator.style.visibility = "hidden";
        indicator.style.display = "block";
        indicator.style.display = "flex";
        button.disabled = true;
      }
      // if username should follow more rules
      // if (username.value.length === 10 && username.value.substring(0, 6).includes("nimbus")) {
      //   nameCheck = true;
      // }
      if (username.value.length >= 5){
        nameCheck = true;
      }
      if (regExBool && passwordComparison && nameCheck) {
        button.disabled = false;
      } else {
        button.disabled = true;
      }
      if (nameCheck) {
        username_info.classList.remove("icon-remove");
        username_info.classList.add("icon-check");
      }
      else {
        username_info.classList.remove("icon-check");
        username_info.classList.add("icon-remove");
      }
      if (passwordComparison) {
        re_password_info.classList.remove("icon-remove");
        re_password_info.classList.add("icon-check");
      }
      else {
        re_password_info.classList.remove("icon-check");
        re_password_info.classList.add("icon-remove");
      }
      if (input.value.match(regExpCapital)) {
        capital_letter.classList.remove("icon-remove");
        capital_letter.classList.add("icon-check");
      }
      else {
        capital_letter.classList.remove("icon-check");
        capital_letter.classList.add("icon-remove");
      }
      if (input.value.match(regExpWeak)) {
        small_letter.classList.remove("icon-remove");
        small_letter.classList.add("icon-check");
      }
      else {
        small_letter.classList.remove("icon-check");
        small_letter.classList.add("icon-remove");
      }
      if (input.value.match(regExpMedium)) {
        number_char.classList.remove("icon-remove");
        number_char.classList.add("icon-check");
      }
      else {
        number_char.classList.remove("icon-check");
        number_char.classList.add("icon-remove");
      }
      if (input.value.match(regExpStrong)) {
        special_char.classList.remove("icon-remove");
        special_char.classList.add("icon-check");
      }
      else {
        special_char.classList.remove("icon-check");
        special_char.classList.add("icon-remove");
      }
      if (input.value.length >= 10) {
        pw_length.classList.remove("icon-remove");
        pw_length.classList.add("icon-check");
      }
      else {
        pw_length.classList.remove("icon-check");
        pw_length.classList.add("icon-remove");
      }
      if (result.score == 4) {
        guessable.classList.remove("icon-remove");
        guessable.classList.add("icon-check");
      }
      else {
        guessable.classList.remove("icon-check");
        guessable.classList.add("icon-remove");
      }

    }

    );
  })
});
