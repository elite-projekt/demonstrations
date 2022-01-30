// Generated by CoffeeScript 1.10.0
(function() {
  var feedback_tmpl, guess_times_tmpl, props_tmpl, results_tmpl, round_logs, round_to_x_digits, test_passwords;

  test_passwords = 'zxcvbn\nqwER43@!\nTr0ub4dour&3\ncorrecthorsebatterystaple\ncoRrecth0rseba++ery9.23.2007staple$\n\np@ssword\np@$$word\n123456\n123456789\n11111111\nzxcvbnm,./\nlove88\nangel08\nmonkey13\niloveyou\nwoaini\nwang\ntianya\nzhang198822\nli4478\na6a4Aa8a\nb6b4Bb8b\nz6z4Zz8z\naiIiAaIA\nzxXxZzXZ\npässwörd\nalpha bravo charlie delta\na b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9\na b c 1 2 3\ncorrect-horse-battery-staple\ncorrect.horse.battery.staple\ncorrect,horse,battery,staple\ncorrect~horse~battery~staple\nWhyfaultthebardifhesingstheArgives’harshfate?\nEupithes’sonAntinousbroketheirsilence\nAthena lavished a marvelous splendor\nbuckmulliganstenderchant\nseethenthatyewalkcircumspectly\nLihiandthepeopleofMorianton\nestablishedinthecityofZarahemla\n!"£$%^&*()\n\nD0g..................\nabcdefghijk987654321\nneverforget13/3/1997\n1qaz2wsx3edc\n\ntemppass22\nbriansmith\nbriansmith4mayor\npassword1\nviking\nthx1138\nScoRpi0ns\ndo you know\n\nryanhunter2000\nrianhunter2000\n\nasdfghju7654rewq\nAOEUIDHG&*()LS_\n\n12345678\ndefghi6789\n\nrosebud\nRosebud\nROSEBUD\nrosebuD\nros3bud99\nr0s3bud99\nR0$38uD99\n\nverlineVANDERMARK\n\neheuczkqyq\nrWibMFACxAUGZmxhVncy\nBa9ZyWABu99[BK#6MBgbH88Tofv)vs$w';

  results_tmpl = '{{#results}}\n<table class="result">\n  <tr>\n    <td>password: </td>\n    <td colspan="2"><strong>{{password}}</strong></td>\n  </tr>\n  <tr>\n    <td>guesses_log10: </td>\n    <td colspan="2">{{guesses_log10}}</td>\n  </tr>\n  <tr>\n    <td>score: </td>\n    <td>{{score}} / 4</td>\n  <tr>\n    <td>function runtime (ms): </td>\n    <td colspan="2">{{calc_time}}</td>\n  </tr>\n  <tr>\n    <td colspan="3">guess times:</td>\n  </tr>\n  {{& guess_times_display}}\n  {{& feedback_display }}\n  <tr>\n    <td colspan="3"><strong>match sequence:</strong></td>\n  </tr>\n</table>\n{{& sequence_display}}\n{{/results}}';

  guess_times_tmpl = '<tr>\n  <td>100 / hour:</td>\n  <td>{{online_throttling_100_per_hour}}</td>\n  <td> (throttled online attack)</td>\n</tr>\n<tr>\n  <td>10&nbsp; / second:</td>\n  <td>{{online_no_throttling_10_per_second}}</td>\n  <td> (unthrottled online attack)</td>\n</tr>\n<tr>\n  <td>10k / second:</td>\n  <td>{{offline_slow_hashing_1e4_per_second}}</td>\n  <td> (offline attack, slow hash, many cores)</td>\n<tr>\n  <td>10B / second:</td>\n  <td>{{offline_fast_hashing_1e10_per_second}}</td>\n  <td> (offline attack, fast hash, many cores)</td>\n</tr>';

  feedback_tmpl = '{{#warning}}\n<tr>\n  <td>warning: </td>\n  <td colspan="2">{{warning}}</td>\n</tr>\n{{/warning}}\n{{#has_suggestions}}\n<tr>\n  <td style="vertical-align: top">suggestions:</td>\n  <td colspan="2">\n    {{#suggestions}}\n    - {{.}} <br />\n    {{/suggestions}}\n  </td>\n</tr>\n{{/has_suggestions}}';

  props_tmpl = '<div class="match-sequence">\n{{#sequence}}\n<table>\n  <tr>\n    <td colspan="2">\'{{token}}\'</td>\n  </tr>\n  <tr>\n    <td>pattern:</td>\n    <td>{{pattern}}</td>\n  </tr>\n  <tr>\n    <td>guesses_log10:</td>\n    <td>{{guesses_log10}}</td>\n  </tr>\n  {{#cardinality}}\n  <tr>\n    <td>cardinality:</td>\n    <td>{{cardinality}}</td>\n  </tr>\n  <tr>\n    <td>length:</td>\n    <td>{{length}}</td>\n  </tr>\n  {{/cardinality}}\n  {{#rank}}\n  <tr>\n    <td>dictionary_name:</td>\n    <td>{{dictionary_name}}</td>\n  </tr>\n  <tr>\n    <td>rank:</td>\n    <td>{{rank}}</td>\n  </tr>\n  <tr>\n    <td>reversed:</td>\n    <td>{{reversed}}</td>\n  </tr>\n  {{#l33t}}\n  <tr>\n    <td>l33t subs:</td>\n    <td>{{sub_display}}</td>\n  </tr>\n  <tr>\n    <td>un-l33ted:</td>\n    <td>{{matched_word}}</td>\n  </tr>\n  {{/l33t}}\n  <tr>\n    <td>base-guesses:</td>\n    <td>{{base_guesses}}</td>\n  </tr>\n  <tr>\n    <td>uppercase-variations:</td>\n    <td>{{uppercase_variations}}</td>\n  </tr>\n  <tr>\n    <td>l33t-variations:</td>\n    <td>{{l33t_variations}}</td>\n  </tr>\n  {{/rank}}\n  {{#graph}}\n  <tr>\n    <td>graph:</td>\n    <td>{{graph}}</td>\n  </tr>\n  <tr>\n    <td>turns:</td>\n    <td>{{turns}}</td>\n  </tr>\n  <tr>\n    <td>shifted count:</td>\n    <td>{{shifted_count}}</td>\n  </tr>\n  {{/graph}}\n  {{#base_token}}\n  <tr>\n    <td>base_token:</td>\n    <td>\'{{base_token}}\'</td>\n  </tr>\n  <tr>\n    <td>base_guesses:</td>\n    <td>{{base_guesses}}</td>\n  </tr>\n  <tr>\n    <td>num_repeats:</td>\n    <td>{{repeat_count}}</td>\n  </tr>\n  {{/base_token}}\n  {{#sequence_name}}\n  <tr>\n    <td>sequence-name:</td>\n    <td>{{sequence_name}}</td>\n  </tr>\n  <tr>\n    <td>sequence-size</td>\n    <td>{{sequence_space}}</td>\n  </tr>\n  <tr>\n    <td>ascending:</td>\n    <td>{{ascending}}</td>\n  </tr>\n  {{/sequence_name}}\n  {{#regex_name}}\n  <tr>\n    <td>regex_name:</td>\n    <td>{{regex_name}}</td>\n  </tr>\n  {{/regex_name}}\n  {{#day}}\n  <tr>\n    <td>day:</td>\n    <td>{{day}}</td>\n  </tr>\n  <tr>\n    <td>month:</td>\n    <td>{{month}}</td>\n  </tr>\n  <tr>\n    <td>year:</td>\n    <td>{{year}}</td>\n  </tr>\n  <tr>\n    <td>separator:</td>\n    <td>\'{{separator}}\'</td>\n  </tr>\n  {{/day}}\n</table>\n{{/sequence}}\n</div>';

  round_to_x_digits = function(n, x) {
    return Math.round(n * Math.pow(10, x)) / Math.pow(10, x);
  };

  round_logs = function(r) {
    var i, len, m, ref, results1;
    r.guesses_log10 = round_to_x_digits(r.guesses_log10, 5);
    ref = r.sequence;
    results1 = [];
    for (i = 0, len = ref.length; i < len; i++) {
      m = ref[i];
      results1.push(m.guesses_log10 = round_to_x_digits(m.guesses_log10, 5));
    }
    return results1;
  };

  requirejs(['static/js/zxcvbn.js'], function(zxcvbn) {
    return $(function() {
      var _listener, i, last_q, len, password, r, ref, rendered, results_lst;
      window.zxcvbn = zxcvbn;
      results_lst = [];
      ref = test_passwords.split('\n');
      for (i = 0, len = ref.length; i < len; i++) {
        password = ref[i];
        if (!(password)) {
          continue;
        }
        r = zxcvbn(password);
        round_logs(r);
        r.sequence_display = Mustache.render(props_tmpl, r);
        r.guess_times_display = Mustache.render(guess_times_tmpl, r.crack_times_display);
        r.feedback.has_suggestions = r.feedback.suggestions.length > 0;
        r.feedback_display = Mustache.render(feedback_tmpl, r.feedback);
        results_lst.push(r);
      }
      rendered = Mustache.render(results_tmpl, {
        results: results_lst
      });
      $('#results').html(rendered);
      last_q = '';
      _listener = function() {
        var current, results;
        current = $('#password').val();
        if (!current) {
          $('#search-results').html('');
          return;
        }
        if (current !== last_q) {
          last_q = current;
          r = zxcvbn(current);
          round_logs(r);
          r.sequence_display = Mustache.render(props_tmpl, r);
          r.guess_times_display = Mustache.render(guess_times_tmpl, r.crack_times_display);
          r.feedback.has_suggestions = r.feedback.suggestions.length > 0;
          r.feedback_display = Mustache.render(feedback_tmpl, r.feedback);
          results = {
            results: [r]
          };
          rendered = Mustache.render(results_tmpl, results);
          return $('#search-results').html(rendered);
        }
      };
      return setInterval(_listener, 100);
    });
  });

}).call(this);
