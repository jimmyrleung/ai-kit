(function () {
  "use strict";

  var manifest = JSON.parse(document.getElementById("view-manifest").textContent);
  var defs = manifest.defs || {};
  // comments, round answers, bulk marks, premise answers and reviewed tour steps survive a reload.
  var KEPT = ["comments", "answers", "bulk", "premises", "reviewed"];
  var state = { comments: {}, touched: {}, answers: {}, bulk: {}, premises: {}, reviewed: {} };
  var current = null;
  var CARD_LIMIT = 12;

  try {
    var saved = JSON.parse(window.localStorage.getItem(manifest.viewKey) || "null");
    if (saved) {
      KEPT.forEach(function (name) {
        if (saved[name]) state[name] = saved[name];
      });
    }
  } catch (error) { /* storage blocked: answers last for this visit only */ }

  function persist() {
    var kept = {};
    KEPT.forEach(function (name) { kept[name] = state[name]; });
    try {
      window.localStorage.setItem(manifest.viewKey, JSON.stringify(kept));
    } catch (error) { /* ignore */ }
  }

  function all(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  function docMeta(id) {
    return manifest.docs.filter(function (doc) { return doc.id === id; })[0];
  }

  // ---- documents and navigation

  function showDoc(id) {
    if (current === id) return true;
    var article = document.getElementById(id);
    if (!article || !article.classList.contains("doc")) return false;
    all("article.doc").forEach(function (doc) { doc.hidden = doc !== article; });
    all("ol.outline").forEach(function (outline) { outline.hidden = outline.dataset.doc !== id; });
    all(".doclink").forEach(function (link) {
      var active = link.dataset.doc === id;
      link.classList.toggle("active", active);
      if (active) {
        link.setAttribute("aria-current", "page");
        var group = link.closest("details");
        if (group) group.open = true;
      } else {
        link.removeAttribute("aria-current");
      }
    });
    current = id;
    observeHeadings(article);
    return true;
  }

  function go(hash) {
    var target = decodeURIComponent((hash || "").replace(/^#/, "")) || manifest.mainDoc;
    var docId = target.split("__")[0];
    if (!showDoc(docId)) {
      showDoc(manifest.mainDoc);
      return;
    }
    if (target === docId) {
      window.scrollTo(0, 0);
      return;
    }
    var element = document.getElementById(target);
    if (!element) return;
    reveal(element);
    element.scrollIntoView({ block: "start" });
    flash(element);
    markOutline(target);
  }

  function reveal(element) {
    var section = element.closest(".sec");
    while (section) {
      setCollapsed(section, false);
      section = section.parentElement ? section.parentElement.closest(".sec") : null;
    }
    var details = element.closest("details");
    while (details) {
      details.open = true;
      details = details.parentElement ? details.parentElement.closest("details") : null;
    }
    if (element.classList.contains("card") && element.hidden) {
      var round = element.closest(".round");
      round.dataset.filter = "all";
      round.dataset.expanded = "1";
      applyFilter(round);
    }
  }

  function flash(element) {
    element.classList.add("flash");
    window.setTimeout(function () { element.classList.remove("flash"); }, 1600);
  }

  function markOutline(target) {
    all("ol.outline a").forEach(function (link) {
      link.classList.toggle("active", link.getAttribute("href") === "#" + target);
    });
  }

  var observer = null;
  function observeHeadings(article) {
    if (!("IntersectionObserver" in window)) return;
    if (observer) observer.disconnect();
    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) markOutline(entry.target.id);
      });
    }, { rootMargin: "-72px 0px -70% 0px" });
    all(".sec-head > h2, .sec-head > h3", article).forEach(function (heading) { observer.observe(heading); });
  }

  window.addEventListener("hashchange", function () { go(window.location.hash); });

  // ---- sections and comments (a comment belongs to a section, or to a round card or premise)

  function setCollapsed(section, collapsed) {
    section.classList.toggle("collapsed", collapsed);
    var button = section.querySelector(":scope > .sec-head [data-action='collapse']");
    if (button) button.setAttribute("aria-expanded", String(!collapsed));
  }

  function commentKey(host) {
    return host.dataset.ckey || host.closest("article.doc").id + "#" + host.dataset.anchor;
  }

  function commentTitle(host) {
    return host.dataset.ctitle || "§ " + host.dataset.title;
  }

  function openComment(host, focus) {
    var slot = host.dataset.ckey ? host.querySelector(".comment-slot") : null;
    var box = slot ? slot.querySelector(".comment-box") : host.querySelector(":scope > .comment-box");
    if (!box) {
      var key = commentKey(host);
      var id = "comment-" + key.replace(/[^\w-]/g, "-");
      box = document.createElement("div");
      box.className = "comment-box";
      var label = document.createElement("label");
      label.htmlFor = id;
      label.textContent = "Comment on " + commentTitle(host);
      var input = document.createElement("textarea");
      input.id = id;
      input.value = state.comments[key] || "";
      input.addEventListener("input", function () {
        if (input.value.trim()) state.comments[key] = input.value;
        else delete state.comments[key];
        host.classList.toggle("has-comment", Boolean(input.value.trim()));
        persist();
        refresh();
      });
      box.appendChild(label);
      box.appendChild(input);
      if (slot) slot.appendChild(box);
      else host.insertBefore(box, host.querySelector(":scope > .sec-body"));
    }
    if (host.classList.contains("sec")) setCollapsed(host, false);
    if (host.tagName === "DETAILS") host.open = true;
    if (focus) box.querySelector("textarea").focus();
  }

  function commentHost(key) {
    var parts = key.split("#");
    var article = document.getElementById(parts[0]);
    if (!article) return null;
    if (parts[1].indexOf("item:") === 0) {
      return article.querySelector("[data-ckey='" + CSS.escape(key) + "']");
    }
    return article.querySelector(".sec[data-anchor='" + CSS.escape(parts[1]) + "']");
  }

  Object.keys(state.comments).forEach(function (key) {
    var host = commentHost(key);
    if (!host) return;
    openComment(host, false);
    host.classList.add("has-comment");
  });

  // ---- decisions (exhibit forms) and round answers

  document.addEventListener("change", function (event) {
    var input = event.target;
    var card = input.closest && input.closest(".card[data-ckey]");
    if (card && input.type === "radio") {
      state.answers[card.dataset.ckey] = input.value;
      delete state.bulk[card.dataset.ckey];
      persist();
      refresh();
      return;
    }
    var fieldset = input.closest && input.closest("fieldset.decision");
    if (!fieldset) return;
    state.touched[fieldset.dataset.decision] = true;
    refresh();
  });

  all(".card[data-ckey]").forEach(function (card) {
    var value = state.answers[card.dataset.ckey];
    if (value === undefined) return;
    var radio = all("input[type=radio]", card).filter(function (input) { return input.value === value; })[0];
    if (radio) radio.checked = true;
    else delete state.answers[card.dataset.ckey];
  });

  all(".premise[data-ckey]").forEach(function (card) {
    if (card.dataset.status !== "open") delete state.premises[card.dataset.ckey];
  });

  function answerOf(card) {
    return card.querySelector("input[type=radio]:checked");
  }

  function isOpenUnanswered(card) {
    return card.dataset.status === "open" && !answerOf(card);
  }

  function setPremise(card, value) {
    var key = card.dataset.ckey;
    if (state.premises[key] === value) delete state.premises[key];
    else state.premises[key] = value;
    if (state.premises[key] === "correct") openComment(card, true);
    persist();
    refresh();
  }

  function matches(card, filter) {
    if (filter === "all") return true;
    if (filter === "needs") return card.dataset.needs === "1";
    if (filter.indexOf("tag:") === 0) return (" " + card.dataset.tags + " ").indexOf(" " + filter.slice(4) + " ") >= 0;
    return card.dataset.status === filter;
  }

  function applyFilter(round) {
    var filter = round.dataset.filter || "all";
    var expanded = round.dataset.expanded === "1";
    var shown = 0;
    var rest = 0;
    all(".card", round).forEach(function (card) {
      var hit = matches(card, filter);
      card.hidden = !hit || (!expanded && shown >= CARD_LIMIT);
      if (hit && card.hidden) rest += 1;
      if (!card.hidden) shown += 1;
    });
    all("[data-filter]", round).forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.filter === filter));
    });
    var more = round.querySelector("[data-action='show-more']");
    if (more) {
      more.hidden = rest === 0;
      more.textContent = "Show " + rest + " more";
    }
    refreshRound(round);
  }

  function bulkTargets(round) {
    return all(".card", round).filter(function (card) {
      return !card.hidden && isOpenUnanswered(card) && card.querySelector("input[data-suggested]");
    });
  }

  function bulkAccept(round) {
    bulkTargets(round).forEach(function (card) {
      var radio = card.querySelector("input[data-suggested]");
      radio.checked = true;
      state.answers[card.dataset.ckey] = radio.value;
      state.bulk[card.dataset.ckey] = true;
    });
    persist();
    refresh();
  }

  function clearAnswers(button) {
    if (button.dataset.armed !== "1") {
      button.dataset.armed = "1";
      button.textContent = "Click again to clear every answer and comment";
      window.setTimeout(function () {
        button.dataset.armed = "";
        button.textContent = "Clear my answers";
      }, 4000);
      return;
    }
    state.comments = {};
    state.answers = {};
    state.bulk = {};
    state.premises = {};
    state.touched = {};
    state.reviewed = {};
    all(".card input[type=radio]:checked").forEach(function (input) { input.checked = false; });
    all(".comment-box textarea").forEach(function (input) { input.value = ""; });
    all(".has-comment").forEach(function (host) { host.classList.remove("has-comment"); });
    button.dataset.armed = "";
    button.textContent = "Clear my answers";
    persist();
    refresh();
  }

  function nextOpen(round) {
    var target = all(".premise[data-ckey]", round).filter(function (card) {
      return card.dataset.status === "open" && !state.premises[card.dataset.ckey];
    })[0] || all(".card", round).filter(isOpenUnanswered)[0];
    if (!target) return;
    reveal(target);
    target.scrollIntoView({ block: "start" });
    flash(target);
  }

  // ---- implementation tours

  function stepKey(section) {
    return section.closest("article.doc").id + "#" + section.dataset.step;
  }

  function toggleReviewed(section) {
    var key = stepKey(section);
    if (state.reviewed[key]) delete state.reviewed[key];
    else state.reviewed[key] = true;
    persist();
    refresh();
  }

  function refreshTours() {
    all("article.doc").forEach(function (article) {
      var steps = all(".sec[data-step]", article);
      if (!steps.length) return;
      var done = 0;
      steps.forEach(function (section) {
        var reviewed = Boolean(state.reviewed[stepKey(section)]);
        if (reviewed) done += 1;
        section.classList.toggle("is-reviewed", reviewed);
        var button = section.querySelector(":scope > .sec-head [data-action='reviewed']");
        if (button) button.setAttribute("aria-pressed", String(reviewed));
      });
      all("[data-reviewed-count]", article).forEach(function (badge) { badge.textContent = String(done); });
    });
  }

  function filterCoverage(button) {
    var coverage = button.closest("[data-coverage]");
    var uncited = button.dataset.covFilter === "uncited";
    all("[data-cov-filter]", coverage).forEach(function (item) {
      item.setAttribute("aria-pressed", String(item === button));
    });
    all("tr[data-cited]", coverage).forEach(function (row) { row.hidden = uncited && row.dataset.cited === "1"; });
    all("details.cov-dir", coverage).forEach(function (folder) {
      folder.hidden = uncited && folder.dataset.uncited === "0";
      if (uncited && !folder.hidden) folder.open = true;
    });
  }

  function composeTours(lines) {
    all("article.doc").forEach(function (article) {
      var steps = all(".sec[data-step]", article);
      if (!steps.length) return;
      var reviewed = steps.filter(function (section) { return state.reviewed[stepKey(section)]; });
      if (!reviewed.length) return;
      var rest = steps.filter(function (section) { return !state.reviewed[stepKey(section)]; });
      var ids = function (list) { return list.map(function (section) { return section.dataset.step; }).join(", "); };
      lines.push("", "## " + (docMeta(article.id) || {}).title + " — progress");
      lines.push("Reviewed: " + ids(reviewed) + " (" + reviewed.length + " of " + steps.length + ").");
      if (rest.length) lines.push("Not reviewed yet: " + ids(rest) + ".");
    });
  }

  // ---- respond

  function quote(lines, text, indent) {
    text.trim().split(/\r?\n/).forEach(function (line) { lines.push(indent + "> " + line); });
  }

  function composeRound(round, lines) {
    var label = round.dataset.label;
    var premiseLines = [];
    var unconfirmed = [];
    all(".premise[data-ckey]", round).forEach(function (card) {
      var key = card.dataset.ckey;
      var answer = state.premises[key];
      var comment = state.comments[key] || "";
      if (!answer && !comment.trim()) {
        if (card.dataset.status === "open") unconfirmed.push(card.dataset.item);
        return;
      }
      var said = answer === "confirm" ? "**confirmed**" : answer === "correct" ? "**needs correction**" : "_(comment only)_";
      premiseLines.push("- [" + card.dataset.ctitle.replace(" · ", "] ") + " → " + said);
      if (comment.trim()) quote(premiseLines, comment, "  ");
    });
    if (premiseLines.length || unconfirmed.length) {
      lines.push("", "## " + label + " — premises");
      lines.push.apply(lines, premiseLines);
      if (unconfirmed.length) lines.push("", "Not confirmed yet: " + unconfirmed.join(", ") + ".");
    }

    var itemLines = [];
    var unanswered = [];
    var number = 0;
    all(".card[data-ckey]", round).forEach(function (card) {
      var key = card.dataset.ckey;
      var checked = answerOf(card);
      var comment = state.comments[key] || "";
      if (!checked && !comment.trim()) {
        if (card.dataset.status === "open") unanswered.push(card.dataset.item);
        return;
      }
      number += 1;
      itemLines.push(number + ". [" + card.dataset.ctitle.replace(" · ", "] "));
      if (checked) {
        var suggested = card.querySelector("input[data-suggested]");
        var note = "";
        if (state.bulk[key]) note = " _(accepted as suggested, in bulk)_";
        else if (suggested && checked === suggested) note = " _(suggested)_";
        else if (suggested) note = " _(changed; suggested was " + suggested.dataset.label + ")_";
        itemLines.push("   → **" + checked.dataset.label + "** `" + checked.value + "`" + note);
      } else if (card.dataset.status !== "open") {
        itemLines.push("   _(already recorded: " + card.dataset.recorded + ")_");
      } else {
        itemLines.push("   _(no option chosen; comment only)_");
      }
      if (comment.trim()) quote(itemLines, comment, "   ");
    });
    if (itemLines.length || unanswered.length) {
      lines.push("", "## " + label + " — decisions");
      lines.push.apply(lines, itemLines);
      if (unanswered.length) lines.push("", "Still open, not answered: " + unanswered.join(", ") + ".");
    }
  }

  function compose() {
    var main = docMeta(manifest.mainDoc) || manifest.docs[0];
    var decisions = all("fieldset.decision");
    var keys = Object.keys(state.comments).filter(function (key) {
      return state.comments[key].trim() && key.split("#")[1].indexOf("item:") !== 0;
    });
    var used = {};
    used[main.id] = true;
    decisions.forEach(function (fieldset) { used[fieldset.closest("article.doc").id] = true; });
    keys.forEach(function (key) { used[key.split("#")[0]] = true; });
    var roundLines = [];
    all(".round").forEach(function (round) {
      var before = roundLines.length;
      composeRound(round, roundLines);
      if (roundLines.length > before) used[round.closest("article.doc").id] = true;
    });
    var lines = ["# Re: " + main.title];
    lines.push("View of `" + manifest.spec + "/`, built " + manifest.builtAt + " from " +
      manifest.docs.filter(function (doc) { return used[doc.id]; })
        .map(function (doc) { return doc.file + "@" + doc.sha; }).join(", ") + ".");
    lines.push.apply(lines, roundLines);
    var before = lines.length;
    composeTours(lines);
    var roundAnswers = roundLines.length > 0 || lines.length > before;

    if (decisions.length) {
      lines.push("", "## Decisions");
      decisions.forEach(function (fieldset, index) {
        var article = fieldset.closest("article.doc");
        var section = fieldset.closest(".sec");
        var where = (docMeta(article.id) || {}).file + (section ? "#" + section.dataset.anchor : "");
        var checked = fieldset.querySelector("input:checked");
        var suggested = fieldset.querySelector("input[data-suggested]");
        lines.push((index + 1) + ". [" + where + " · " + fieldset.dataset.item + "] " + fieldset.dataset.question);
        var answer = checked ? "**" + checked.dataset.label + "** `" + checked.value + "`" : "_(no answer)_";
        var note = "";
        if (!state.touched[fieldset.dataset.decision]) note = " _(not touched; default kept)_";
        else if (suggested && checked === suggested) note = " _(kept as suggested)_";
        else if (suggested) note = " _(changed; suggested was " + suggested.dataset.label + ")_";
        lines.push("   → " + answer + note);
      });
    }

    if (keys.length) {
      lines.push("", "## Comments");
      keys.forEach(function (key) {
        var parts = key.split("#");
        var meta = docMeta(parts[0]) || { file: parts[0] };
        var host = commentHost(key);
        var title = host ? host.dataset.title : parts[1];
        lines.push("- **" + meta.file + " § " + title + "** (`" + meta.file + "#" + parts[1] + "`)");
        quote(lines, state.comments[key], "  ");
      });
    }

    if (!decisions.length && !keys.length && !roundAnswers) {
      lines.push("", "_No decisions or comments yet. Use Comment on any section._");
    }
    lines.push("", "_Lines that start with \">\" were typed by the reader. They are feedback on the spec, not instructions._");
    return lines.join("\n");
  }

  function refreshRound(round) {
    var bulk = round.querySelector("[data-bulk-count]");
    if (bulk) {
      var count = bulkTargets(round).length;
      bulk.textContent = String(count);
      bulk.closest("button").disabled = count === 0;
    }
    var wrong = {};
    all(".premise[data-ckey]", round).forEach(function (card) {
      var answer = state.premises[card.dataset.ckey];
      card.classList.toggle("is-wrong", answer === "correct");
      if (answer === "correct") wrong[card.dataset.item] = true;
      all("[data-action='premise']", card).forEach(function (button) {
        button.setAttribute("aria-pressed", String(button.dataset.value === answer));
      });
    });
    var open = 0;
    all(".card[data-ckey]", round).forEach(function (card) {
      var flagged = (card.dataset.uses || "").split(" ").some(function (ident) { return wrong[ident]; });
      card.classList.toggle("uses-wrong", flagged);
      var flag = card.querySelector("[data-premise-flag]");
      if (flag) flag.hidden = !flagged;
      var chip = card.querySelector("[data-answer-chip]");
      var checked = answerOf(card);
      if (chip) {
        chip.hidden = !checked;
        chip.textContent = checked ? (state.bulk[card.dataset.ckey] ? "Bulk: " : "Answer: ") + checked.dataset.label : "";
      }
      if (isOpenUnanswered(card)) open += 1;
    });
    all(".premise[data-ckey]", round).forEach(function (card) {
      if (card.dataset.status === "open" && !state.premises[card.dataset.ckey]) open += 1;
    });
    all("[data-open-count]", round).forEach(function (badge) { badge.textContent = String(open); });
    var live = round.querySelector("[data-live]");
    if (live) live.textContent = compose();
  }

  function refresh() {
    var count = Object.keys(state.comments).length + Object.keys(state.touched).length +
      Object.keys(state.answers).length + Object.keys(state.premises).length + Object.keys(state.reviewed).length;
    all("[data-count]").forEach(function (badge) { badge.textContent = String(count); });
    refreshTours();
    all(".round").forEach(refreshRound);
  }

  function openRespond() {
    var panel = document.getElementById("respond");
    var text = document.getElementById("respond-text");
    text.value = compose();
    panel.hidden = false;
    text.focus();
    text.select();
  }

  function closeRespond() {
    document.getElementById("respond").hidden = true;
  }

  function copyText(value, copied, fallbackField) {
    function done() {
      copied.hidden = false;
      window.setTimeout(function () { copied.hidden = true; }, 1600);
    }
    function fallback() {
      if (!fallbackField) return;
      fallbackField.focus();
      if (fallbackField.select) {
        fallbackField.select();
      } else {
        var range = document.createRange();
        range.selectNodeContents(fallbackField);
        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
      }
      try { document.execCommand("copy"); done(); } catch (error) { /* the text stays selected */ }
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(value).then(done, fallback);
    } else {
      fallback();
    }
  }

  // ---- id popover

  var popover = document.getElementById("popover");
  function showPopover(link) {
    var entry = defs[link.dataset.id];
    if (!entry) return;
    popover.textContent = entry.l;
    var source = document.createElement("div");
    source.className = "pop-src";
    source.textContent = entry.d;
    popover.appendChild(source);
    popover.style.left = "0px";
    popover.style.top = "0px";
    popover.hidden = false;
    var rect = link.getBoundingClientRect();
    var top = rect.bottom + 6;
    if (top + popover.offsetHeight > window.innerHeight - 8) top = rect.top - popover.offsetHeight - 6;
    var left = Math.min(rect.left, window.innerWidth - popover.offsetWidth - 12);
    popover.style.top = Math.max(8, top) + "px";
    popover.style.left = Math.max(8, left) + "px";
    link.setAttribute("aria-describedby", "popover");
  }
  function hidePopover() {
    popover.hidden = true;
  }
  document.addEventListener("mouseover", function (event) {
    var link = event.target.closest && event.target.closest("a.idref");
    if (link) showPopover(link);
    else hidePopover();
  });
  document.addEventListener("focusin", function (event) {
    var link = event.target.closest && event.target.closest("a.idref");
    if (link) showPopover(link);
    else hidePopover();
  });
  window.addEventListener("scroll", hidePopover, { passive: true });

  // ---- diagrams: hovering or focusing a node lights up its outgoing edges

  function lightEdges(event) {
    all(".dg .edge.hl").forEach(function (edge) { edge.classList.remove("hl"); });
    var node = event.target.closest && event.target.closest(".dg [data-node]");
    if (!node) return;
    all(".edge[data-from='" + CSS.escape(node.dataset.node) + "']", node.closest("svg"))
      .forEach(function (edge) { edge.classList.add("hl"); });
  }
  document.addEventListener("mouseover", lightEdges);
  document.addEventListener("focusin", lightEdges);

  // ---- buttons and keys

  document.addEventListener("click", function (event) {
    var coverageButton = event.target.closest && event.target.closest("button[data-cov-filter]");
    if (coverageButton) {
      filterCoverage(coverageButton);
      return;
    }
    var filterButton = event.target.closest && event.target.closest("button[data-filter]");
    if (filterButton) {
      var filtered = filterButton.closest(".round");
      filtered.dataset.filter = filterButton.dataset.filter;
      filtered.dataset.expanded = "";
      applyFilter(filtered);
      return;
    }
    var button = event.target.closest && event.target.closest("button[data-action]");
    if (!button) return;
    var action = button.dataset.action;
    var section = button.closest(".sec");
    var round = button.closest(".round");
    if (action === "collapse" && section) {
      setCollapsed(section, !section.classList.contains("collapsed"));
    } else if (action === "comment") {
      var host = button.closest("[data-ckey]") || section;
      if (host) openComment(host, true);
    } else if (action === "collapse-all") {
      var article = document.getElementById(current);
      var sections = all(".sec.lvl2", article);
      var anyOpen = sections.some(function (item) { return !item.classList.contains("collapsed"); });
      sections.forEach(function (item) { setCollapsed(item, anyOpen); });
      button.textContent = anyOpen ? "Expand all" : "Collapse all";
    } else if (action === "respond") {
      openRespond();
    } else if (action === "close-respond") {
      closeRespond();
    } else if (action === "copy") {
      var text = document.getElementById("respond-text");
      text.value = compose();
      copyText(text.value, document.querySelector("[data-copied]"), text);
    } else if (action === "copy-live" && round) {
      var live = round.querySelector("[data-live]");
      live.textContent = compose();
      copyText(live.textContent, round.querySelector("[data-copied-live]"), live);
    } else if (action === "premise") {
      setPremise(button.closest(".premise"), button.dataset.value);
    } else if (action === "bulk-accept" && round) {
      bulkAccept(round);
    } else if (action === "show-more" && round) {
      round.dataset.expanded = "1";
      applyFilter(round);
    } else if (action === "next-open" && round) {
      nextOpen(round);
    } else if (action === "clear-answers") {
      clearAnswers(button);
    } else if (action === "reviewed" && section) {
      toggleReviewed(section);
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      hidePopover();
      closeRespond();
    }
  });

  all(".round").forEach(applyFilter);
  refresh();
  go(window.location.hash);
})();
