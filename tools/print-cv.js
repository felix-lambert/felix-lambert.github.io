// Prints the built /cv/ and /fr/cv/ pages to PDF with headless Chromium.
// Usage: node tools/print-cv.js <built-site-dir> <output-dir>
// Requires Playwright (npm i -g playwright) with a Chromium build available.
const path = require("path");
const fs = require("fs");
const http = require("http");

function requirePlaywright() {
  try {
    return require("playwright");
  } catch (e) {
    const globalRoot = require("child_process")
      .execSync("npm root -g")
      .toString()
      .trim();
    return require(path.join(globalRoot, "playwright"));
  }
}

const { chromium } = requirePlaywright();
const root = path.resolve(process.argv[2] || "_site");
const out = path.resolve(process.argv[3] || "download");
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css",
  ".js": "text/javascript",
  ".jpg": "image/jpeg",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".woff2": "font/woff2",
};

const server = http.createServer((req, res) => {
  let file = path.join(root, decodeURIComponent(req.url.split("?")[0]));
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
    file = path.join(file, "index.html");
  }
  if (!fs.existsSync(file)) {
    res.statusCode = 404;
    return res.end("not found");
  }
  res.setHeader("Content-Type", types[path.extname(file)] || "application/octet-stream");
  fs.createReadStream(file).pipe(res);
});

(async () => {
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const port = server.address().port;
  const browser = await chromium.launch();
  const jobs = [
    ["/cv/", "Felix-Lambert-CV-EN.pdf"],
    ["/fr/cv/", "Felix-Lambert-CV-FR.pdf"],
  ];
  fs.mkdirSync(out, { recursive: true });
  for (const [url, name] of jobs) {
    const page = await browser.newPage();
    await page.emulateMedia({ media: "print", colorScheme: "light" });
    await page.goto(`http://127.0.0.1:${port}${url}`, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: path.join(out, name),
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
    });
    await page.close();
    console.log("wrote", path.join(out, name));
  }
  await browser.close();
  server.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
