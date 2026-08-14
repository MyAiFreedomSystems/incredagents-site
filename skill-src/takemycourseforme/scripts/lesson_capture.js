/*
 * lesson_capture.js — extract a lesson's body text + resource links from the
 * live page. Run it in the logged-in Chrome tab via chrome_js.py:
 *
 *   python3 chrome_js.py '<url-substring>' '@scripts/lesson_capture.js'
 *
 * Skool lesson bodies are ProseMirror rich text (a contenteditable div). This
 * walks the block elements and converts them to markdown, then collects every
 * link that points at a downloadable file (ZIP/PDF/video/etc.) — those are the
 * actual course deliverables and the most-missed target.
 */
(function () {
  function inlineMd(node) {
    var s = "";
    if (!node || !node.childNodes) return s;
    node.childNodes.forEach(function (n) {
      if (n.nodeType === 3) { s += n.nodeValue; return; }        // text
      if (n.nodeType !== 1) return;                              // not an element
      var t = n.tagName.toLowerCase();
      var inner = inlineMd(n);
      if (t === "a") {
        var h = n.href;
        s += h ? "[" + inner + "](" + h + ")" : inner;
      } else if (t === "strong" || t === "b") s += "**" + inner + "**";
      else if (t === "em" || t === "i") s += "*" + inner + "*";
      else if (t === "code") s += "`" + inner + "`";
      else if (t === "br") s += "\n";
      else if (t === "img") {
        var src = n.src;
        var alt = n.getAttribute("alt") || "";
        s += src ? "![" + alt + "](" + src + ")" : "";
      } else s += inner;
    });
    return s;
  }

  function blockMd(node) {
    var out = [];
    if (!node || !node.childNodes) return out;
    node.childNodes.forEach(function (n) {
      if (n.nodeType !== 1) return;
      var t = n.tagName.toLowerCase();
      if (t === "ul" || t === "ol") {
        blockMd(n).forEach(function (l) { out.push(l); });
        return;
      }
      var text = inlineMd(n).trim();
      if (!text) return;
      if (t === "h1") out.push("# " + text);
      else if (t === "h2") out.push("## " + text);
      else if (t === "h3") out.push("### " + text);
      else if (/^h[4-6]$/.test(t)) out.push("#### " + text);
      else if (t === "li") out.push("- " + text);
      else if (t === "blockquote") out.push("> " + text);
      else if (t === "pre") out.push("```\n" + (n.textContent || "") + "\n```");
      else if (t === "p") out.push(text);
      else out.push(text);
    });
    return out;
  }

  var el = document.querySelector(".ProseMirror")
    || document.querySelector('[contenteditable="true"]')
    || document.querySelector("article")
    || document.querySelector("main")
    || document.body;

  var markdown = blockMd(el).join("\n\n");

  var resources = [];
  var images = [];
  var seenRes = {};
  // Downloadable deliverables only — images are collected separately so the
  // resources list reflects what you'd actually download (ZIP/PDF/video/etc.).
  var FILE_RE = /\.(zip|pdf|mp4|mp3|mov|webm|m4a|docx?|xlsx?|pptx?|csv|txt|srt|vtt)(\?|$)/i;
  var IMG_RE = /\.(png|jpe?g|gif)(\?|$)/i;
  document.querySelectorAll("a[href]").forEach(function (a) {
    var href = a.href || "";
    var isImg = IMG_RE.test(href);
    if (!isImg && !FILE_RE.test(href)) return;
    if (seenRes[href]) return;
    seenRes[href] = true;
    var name = (a.textContent || "").trim();
    if (!name) name = href.split("/").pop().split("?")[0];
    if (isImg) images.push({ name: name, url: href });
    else resources.push({ name: name, url: href });
  });

  return JSON.stringify({
    title: document.title,
    url: location.href,
    markdown: markdown,
    resources: resources,
    images: images
  }, null, 2);
})();
