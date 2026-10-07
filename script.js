/* Grace's Takeaway: "Open now" badge and today's row in the hours table.
   Opening hours are read from the JSON-LD block in the page, so there is
   only one set of hours to edit per page (tools/build.py checks that the
   JSON-LD and the hours table in index.html agree). Times are Irish time. */
(function () {
  "use strict";

  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  var SHORT = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };

  function toMinutes(hhmm) {
    var p = hhmm.split(":");
    return parseInt(p[0], 10) * 60 + parseInt(p[1], 10);
  }

  function formatTime(mins) {
    var h = Math.floor(mins / 60) % 24;
    var m = mins % 60;
    var suffix = h >= 12 ? "pm" : "am";
    var h12 = h % 12 === 0 ? 12 : h % 12;
    return h12 + (m ? ":" + (m < 10 ? "0" : "") + m : "") + suffix;
  }

  // Read hours from JSON-LD: { dayIndex: [openMins, closeMins] }
  function readHours() {
    var hours = {};
    var block = document.querySelector('script[type="application/ld+json"]');
    if (!block) return null;
    try {
      var data = JSON.parse(block.textContent);
      (data.openingHoursSpecification || []).forEach(function (spec) {
        [].concat(spec.dayOfWeek).forEach(function (day) {
          var name = String(day).replace("https://schema.org/", "");
          var idx = DAYS.indexOf(name);
          if (idx > -1) hours[idx] = [toMinutes(spec.opens), toMinutes(spec.closes)];
        });
      });
    } catch (e) {
      return null;
    }
    return hours;
  }

  // Current day and minutes in Europe/Dublin, whatever the visitor's timezone.
  function dublinNow() {
    var parts = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/Dublin",
      weekday: "short",
      hour: "2-digit",
      minute: "2-digit",
      hourCycle: "h23"
    }).formatToParts(new Date());
    var get = function (type) {
      for (var i = 0; i < parts.length; i++) if (parts[i].type === type) return parts[i].value;
      return "";
    };
    return { day: SHORT[get("weekday")], mins: parseInt(get("hour"), 10) * 60 + parseInt(get("minute"), 10) };
  }

  function statusText(hours, now) {
    var today = hours[now.day];
    if (today && now.mins >= today[0] && now.mins < today[1]) {
      return { open: true, text: "Open now · until " + formatTime(today[1]) };
    }
    if (today && now.mins < today[0]) {
      return { open: false, text: "Closed now · opens today at " + formatTime(today[0]) };
    }
    for (var i = 1; i <= 7; i++) {
      var d = (now.day + i) % 7;
      if (hours[d]) {
        var when = i === 1 ? "tomorrow" : DAYS[d];
        return { open: false, text: "Closed now · opens " + when + " at " + formatTime(hours[d][0]) };
      }
    }
    return null;
  }

  function update() {
    var hours = readHours();
    if (!hours || !window.Intl) return;
    var now = dublinNow();
    var status = statusText(hours, now);

    var badges = document.querySelectorAll("[data-status]");
    for (var i = 0; i < badges.length; i++) {
      if (!status) continue;
      badges[i].textContent = status.text;
      badges[i].classList.toggle("is-open", status.open);
      badges[i].classList.toggle("is-closed", !status.open);
      badges[i].hidden = false;
    }

    var rows = document.querySelectorAll(".hours-table tr[data-day]");
    for (var j = 0; j < rows.length; j++) {
      rows[j].classList.toggle("is-today", rows[j].getAttribute("data-day") === DAYS[now.day]);
    }
  }

  update();
  setInterval(update, 60 * 1000);
})();
