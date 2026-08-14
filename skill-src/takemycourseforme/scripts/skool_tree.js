/*
 * skool_tree.js — walk a Skool course tree out of the page's Next.js data.
 *
 * Run it inside the real logged-in Chrome tab via chrome_js.py:
 *
 *   python3 chrome_js.py 'skool.com' '@scripts/skool_tree.js' > tree.json
 *
 * Skool is a Next.js app. The course tree lives in the page's __NEXT_DATA__
 * script tag and in the richer /_next/data/<buildId>/<path>.json payload.
 *
 * IMPORTANT: `async fetch` never resolves through Chrome's "execute javascript"
 * bridge. Use a SYNCHRONOUS XHR (open with async=false) — this is the proven
 * workaround and is already wired up below.
 *
 * The walker is heuristic: it looks for objects that have a `title` plus a
 * URL-ish field (url / slug / videoUrl / videoLink / video_url), and infers a
 * "section" name from any parent object that has `title` plus a child list
 * (modules / lessons / children / items / units). Inspect the output and prune
 * noise — Skool changes its schema, so treat this as a starting point, not a
 * contract.
 */
(function () {
  function syncGet(url) {
    var x = new XMLHttpRequest();
    x.open("GET", url, false); // false = SYNCHRONOUS (see note above)
    x.send(null);
    return x.status === 200 ? x.responseText : null;
  }

  function parseScript(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }

  var data = parseScript("__NEXT_DATA__");
  var buildId = (data && data.buildId) || (window.__BUILD_ID__ || null);

  var nodes = [];
  var seen = {};
  var MAX_NODES = 2000;
  var MAX_DEPTH = 20;

  function push(o, section) {
    if (nodes.length >= MAX_NODES) return;
    var key = o.url || o.slug || o.videoUrl || o.videoLink || o.video_url || ("title:" + (o.title || ""));
    if (key && !seen[key]) {
      seen[key] = true;
      nodes.push({
        title: o.title || o.name || "(untitled)",
        url: o.url || null,
        slug: o.slug || null,
        videoUrl: o.videoUrl || o.videoLink || o.video_url || null,
        section: section || null
      });
    }
  }

  function childListOf(o) {
    return o.modules || o.lessons || o.children || o.items || o.units || o.courseModules || null;
  }

  function walk(o, section, depth) {
    if (!o || typeof o !== "object" || depth > MAX_DEPTH) return;
    if (Array.isArray(o)) {
      for (var i = 0; i < o.length; i++) walk(o[i], section, depth);
      return;
    }
    var children = childListOf(o);
    var thisSection = (typeof o.title === "string" && o.title && children) ? o.title : section;
    if (children) walk(children, thisSection, depth + 1);

    var hasUrlField = !!(o.url || o.slug || o.videoUrl || o.videoLink || o.video_url);
    if (typeof o.title === "string" && o.title && hasUrlField) {
      push(o, thisSection);
    }
    for (var k in o) {
      if (Object.prototype.hasOwnProperty.call(o, k)) walk(o[k], thisSection, depth + 1);
    }
  }

  walk(data, null, 0);

  // Also try the richer /_next/data JSON for the current path (sync XHR).
  var nextDataText = null;
  var nextDataKeys = [];
  if (buildId && location.pathname) {
    nextDataText = syncGet("/_next/data/" + buildId + location.pathname + ".json");
    if (nextDataText) {
      try {
        var j = JSON.parse(nextDataText);
        nextDataKeys = Object.keys(j);
        walk(j, null, 0); // merge any extra nodes found there
      } catch (e) { /* ignore malformed */ }
    }
  }

  return JSON.stringify({
    pageUrl: location.href,
    buildId: buildId,
    hasNextData: !!data,
    nodeCount: nodes.length,
    nextDataFetched: !!nextDataText,
    nextDataKeys: nextDataKeys,
    nodes: nodes
  }, null, 2);
})();
