// Minimal static dev server. Forwards --port/--host (and PORT/HOST env) so
// Kimi Work can assign a preview port.
const http = require("http");
const fs = require("fs");
const path = require("path");

const argv = process.argv.slice(2);
function arg(name, fallback) {
  const i = argv.indexOf("--" + name);
  if (i !== -1 && argv[i + 1]) return argv[i + 1];
  const eq = argv.find((a) => a.startsWith("--" + name + "="));
  if (eq) return eq.split("=")[1];
  return fallback;
}

const port = parseInt(arg("port", process.env.PORT || "7100"), 10);
const host = arg("host", process.env.HOST || "127.0.0.1");
const root = __dirname;

const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css",
  ".js": "text/javascript",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".ttf": "font/ttf",
  ".json": "application/json",
  ".ico": "image/x-icon",
};

http
  .createServer((req, res) => {
    let urlPath = decodeURIComponent(req.url.split("?")[0]);
    if (urlPath === "/") urlPath = "/index.html";
    const file = path.normalize(path.join(root, urlPath));
    if (!file.startsWith(root)) {
      res.writeHead(403);
      return res.end("Forbidden");
    }
    fs.readFile(file, (err, data) => {
      if (err) {
        res.writeHead(404);
        return res.end("Not found");
      }
      res.writeHead(200, { "Content-Type": types[path.extname(file).toLowerCase()] || "application/octet-stream" });
      res.end(data);
    });
  })
  .listen(port, host, () => console.log(`Serving ${root} at http://${host}:${port}/`));
