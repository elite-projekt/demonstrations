requirejs(['static/signup-form/js/zxcvbn.js'], function(zxcvbn){
$(function(){
    $(".password").on('input',function(){
        const small_letter = document.querySelector(".small-letter");
        const capital_letter = document.querySelector(".capital-letter");
        const special_char = document.querySelector(".special-char");
        const pw_length = document.querySelector(".lenght-check");
        const number_char = document.querySelector(".number-char");
        const indicator = document.querySelector(".indicator");
        const input = document.querySelector(".password");
        const weak = document.querySelector(".weak");
        const medium = document.querySelector(".medium");
        const strong = document.querySelector(".strong");
        const button = document.querySelector(".register-button");
        result = zxcvbn(input.value);
        let regExpWeak = /[a-z]/;
        let regExpMedium = /\d+/;
        let regExpStrong = /[^a-zA-Z\d\sßäöüÄÖÜ]/; //[^a-zA-Z\d\s]/; ///\W/g /[^a-zA-Z\d\sßäöüÄÖÜ]/
        let regExpCapital = /[A-Z]/;
          if(input.value != ""){
            indicator.style.visibility = "visible";
            indicator.style.display = "block";
            indicator.style.display = "flex";
            if(input.value.length <= 3 && (input.value.match(regExpWeak) || input.value.match(regExpMedium) || input.value.match(regExpStrong)))no=1;
            if(input.value.length >= 6 && ((input.value.match(regExpWeak) && input.value.match(regExpMedium)) || (input.value.match(regExpMedium) && input.value.match(regExpStrong)) || (input.value.match(regExpWeak) && input.value.match(regExpStrong))))no=2;
            if(input.value.length >= 10 && input.value.match(regExpWeak) && input.value.match(regExpMedium) && input.value.match(regExpStrong) && input.value.match(regExpCapital) &&result.score == 4)no=3;
            if(no==1){
              weak.classList.add("active");
              button.disabled = true;
            }
            if(no==2){
              medium.classList.add("active");
              button.disabled = true;
            }else{
              medium.classList.remove("active");
              button.disabled = true;
            }
            if(no==3){
              weak.classList.add("active");
              medium.classList.add("active");
              strong.classList.add("active");
              button.disabled = false;
            }else{
              strong.classList.remove("active");
            }
            
          }else{
            indicator.style.visibility = "hidden";
            indicator.style.display = "block";
            indicator.style.display = "flex";
            button.disabled = true;
          }
        
          if(input.value.match(regExpCapital)){
            capital_letter.classList.remove("icon-remove");
            capital_letter.classList.add("icon-check");
          }
          else{              
            capital_letter.classList.remove("icon-check");
            capital_letter.classList.add("icon-remove");
          }
          if(input.value.match(regExpWeak)){
            small_letter.classList.remove("icon-remove");
            small_letter.classList.add("icon-check");
          }
          else{              
            small_letter.classList.remove("icon-check");
            small_letter.classList.add("icon-remove");
          }
          if(input.value.match(regExpMedium)){
            number_char.classList.remove("icon-remove");
            number_char.classList.add("icon-check");
          }
          else{              
            number_char.classList.remove("icon-check");
            number_char.classList.add("icon-remove");
          }
          if(input.value.match(regExpStrong)){
            special_char.classList.remove("icon-remove");
            special_char.classList.add("icon-check");
          }
          else{              
            special_char.classList.remove("icon-check");
            special_char.classList.add("icon-remove");
          }
          if(input.value.length >= 10){
            pw_length.classList.remove("icon-remove");
            pw_length.classList.add("icon-check");
          }
          else{
            pw_length.classList.remove("icon-check");
            pw_length.classList.add("icon-remove");
          }
        
      });
    })
});
