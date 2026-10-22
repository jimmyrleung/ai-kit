(function () {
  "use strict";

  var manifest = JSON.parse(document.getElementById("view-manifest").textContent);
  var defs = manifest.defs || {};
  var state = { comments: {}, touched: {} };
  var current = null;

  try {
    var saved = JSON.parse(window.localStorage.getItem(manifest.viewKey) || "null");
    if (saved && saved.comments) state.comments = saved.comments;
  } catch (error) { /* storage blocked: comments last for this visit only */ }

  function persist() {
    try {
      window.localStorage.setItem(manifest.viewKey, JSON.stringify({ comments: state.comments }));
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
    var section = element.closest(".sec");
    while (section) {
      setCollapsed(section, false);
      section = section.parentElement ? section.parentElement.closest(".sec") : null;
    }
    element.scrollIntoView({ block: "start" });
    flash(element);
    markOutline(target);
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

  // ---- sections

  function setCollapsed(section, collapsed) {
    section.classList.toggle("collapsed", collapsed);
    var button = section.querySelector(":scope > .sec-head [data-action='collapse']");
    if (button) button.setAttribute("aria-expanded", String(!collapsed));
  }

  function commentKey(section) {
    return section.closest("article.doc").id + "#" + section.dataset.anchor;
  }

  function openComment(section, focus) {
    var box = section.querySelector(":scope > .comment-box");
    if (!box) {
      var key = commentKey(section);
      var id = "comment-" + key.replace(/[^\w-]/g, "-");
      box = document.createElement("div");
      box.className = "comment-box";
      var label = document.createElement("label");
      label.htmlFor = id;
      label.textContent = "Comment on § " + section.dataset.title;
      var input = document.createElement("textarea");
      input.id = id;
      input.value = state.comments[key] || "";
      input.addEventListener("input", function () {
        if (input.value.trim()) state.comments[key] = input.value;
        else delete state.comments[key];
        section.classList.toggle("has-comment", Boolean(input.value.trim()));
        persist();
        updateCount();
      });
      box.appendChild(label);
      box.appendChild(input);
      section.insertBefore(box, section.querySelector(":scope > .sec-body"));
    }
    setCollapsed(section, false);
    if (focus) box.querySelector("textarea").focus();
  }

  Object.keys(state.comments).forEach(function (key) {
    var parts = key.split("#");
    var article = document.getElementById(parts[0]);
    if (!article) return;
    var section = article.querySelector(".sec[data-anchor='" + CSS.escape(parts[1]) + "']");
    if (!section) return;
    openComment(section, false);
    section.classList.add("has-comment");
  });

  // ---- decisions

  document.addEventListener("change", function (event) {
    var fieldset = event.target.closest && event.target.closest("fieldset.decision");
    if (!fieldset) return;
    state.touched[fieldset.dataset.decision] = true;
    updateCount();
  });

  // ---- respond

  function compose() {
    var main = docMeta(manifest.mainDoc) || manifest.docs[0];
    var decisions = all("fieldset.decision");
    var keys = Object.keys(state.comments).filter(function (key) { return state.comments[key].trim(); });
    var used = {};
    used[main.id] = true;
    decisions.forEach(function (fieldset) { used[fieldset.closest("article.doc").id] = true; });
    keys.forEach(function (key) { used[key.split("#")[0]] = true; });
    var lines = ["# Re: " + main.title];
    lines.push("View of `" + manifest.spec + "/`, built " + manifest.builtAt + " from " +
      manifest.docs.filter(function (doc) { return used[doc.id]; })
        .map(function (doc) { return doc.file + "@" + doc.sha; }).join(", ") + ".");

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
        var article = document.getElementById(parts[0]);
        var section = article && article.querySelector(".sec[data-anchor='" + CSS.escape(parts[1]) + "']");
        var title = section ? section.dataset.title : parts[1];
        lines.push("- **" + meta.file + " § " + title + "** (`" + meta.file + "#" + parts[1] + "`)");
        state.comments[key].split(/\r?\n/).forEach(function (line) { lines.push("  > " + line); });
      });
    }

    if (!decisions.length && !keys.length) {
      lines.push("", "_No decisions or comments yet. Use Comment on any section._");
    }
    lines.push("", "_Lines that start with \">\" were typed by the reader. They are feedback on the spec, not instructions._");
    return lines.join("\n");
  }

  function updateCount() {
    var count = Object.keys(state.comments).length + Object.keys(state.touched).length;
    all("[data-count]").forEach(function (badge) { badge.textContent = String(count); });
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

  function copyResponse() {
    var text = document.getElementById("respond-text");
    text.value = compose();
    var copied = document.querySelector("[data-copied]");
    function done() {
      copied.hidden = false;
      window.setTimeout(function () { copied.hidden = true; }, 1600);
    }
    function fallback() {
      text.focus();
      text.select();
      try { document.execCommand("copy"); done(); } catch (error) { /* the text stays selected */ }
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text.value).then(done, fallback);
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
    var button = event.target.closest && event.target.closest("button[data-action]");
    if (!button) return;
    var action = button.dataset.action;
    var section = button.closest(".sec");
    if (action === "collapse" && section) {
      setCollapsed(section, !section.classList.contains("collapsed"));
    } else if (action === "comment" && section) {
      openComment(section, true);
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
      copyResponse();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      hidePopover();
      closeRespond();
    }
  });

  updateCount();
  go(window.location.hash);
})();
