(function () {
  var root = document.querySelector("[data-jstack-finder]");
  if (!root) {
    return;
  }

  var input = root.querySelector("input");
  var buttons = Array.prototype.slice.call(root.querySelectorAll("[data-group]"));
  var cards = Array.prototype.slice.call(document.querySelectorAll(".jstack-skill"));
  var grids = Array.prototype.slice.call(document.querySelectorAll(".jstack-skillgrid"));
  var count = root.querySelector("[data-jstack-count]");
  var group = "all";

  function apply() {
    var query = (input.value || "").trim().toLowerCase();
    var shown = 0;

    cards.forEach(function (card) {
      var name = card.getAttribute("data-name") || "";
      var haystack = (name + " " + card.textContent).toLowerCase();
      var inGroup = group === "all" || card.getAttribute("data-group") === group;
      var match = inGroup && (query.length === 0 || haystack.indexOf(query) !== -1);
      card.hidden = !match;
      if (match) {
        shown += 1;
      }
    });

    grids.forEach(function (grid) {
      var visible = grid.querySelector(".jstack-skill:not([hidden])");
      grid.hidden = !visible;
      var heading = grid.previousElementSibling;
      if (heading && heading.tagName === "H2") {
        heading.hidden = !visible;
      }
    });

    if (count) {
      count.textContent = shown === 1 ? "1 skill" : shown + " skills";
    }
  }

  input.addEventListener("input", apply);
  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      group = button.getAttribute("data-group") || "all";
      buttons.forEach(function (other) {
        other.setAttribute("aria-pressed", other === button ? "true" : "false");
      });
      apply();
    });
  });

  apply();
})();
