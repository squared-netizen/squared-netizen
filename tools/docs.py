"""Every tool's documentation, gathered into the site: docs/<repo>/<path>.html,
docs/index.html, and docs/search-index.json for the search box.

    python3 tools/build.py              (calls this)
    SQ_REPOS=~/projects python3 tools/build.py

Offline: it reads the repositories' markdown from local checkouts, one folder
each, named as the repository (by default beside this one: ../sqcart,
../squared, ...; SQ_REPOS names another parent), as committed on origin/main
(SQ_DOCS_REF names another; HEAD where a checkout has no such ref): what is
published, not a branch's work or a working tree's edits. A repository not
checked out keeps the pages its last build wrote. Only each repository's own documents
are read (SOURCES below), never a vendored copy of another's (sqterm's
squared/, a third_party/).

Standard library only, so the markdown is converted here: what the SDK's
documents use (headings, paragraphs, lists, block quotes, fenced code, pipe
tables, rules, and inline code, links, emphasis). A link to another gathered
document becomes a link within the site; any other relative link goes to the
file on GitHub.
"""
import fnmatch
import html
import json
import os
import re
import subprocess
import urllib.parse

E = html.escape

# Each repository's documents: (glob patterns to take, patterns to leave out),
# relative to the repository. Patterns match the whole path (fnmatch: * also
# crosses folders).
SOURCES = {
    "squared": (["README.md", "docs/*.md", "packages/package.squared-core/tree/squared/docs/*.md",
                 "templates/*/tree/*.md", "kits/*/tree/*.md"], []),
    "sqcart": (["README.md", "v3/README.md", "docs/*.md"], []),
    "sqdrive": (["README.md", "docs/*.md"], []),
    "sqmake": (["README.md", "docs/*.md"], []),
    "sqterm": (["README.md", "docs/*.md", "packages/README.md", "sq_app/README.md", "sq_app/docs/*.md",
                "sq_android/README.md"], []),
    "squared-pg": (["README.md", "docs/*.md"], []),
    "squared-examples": (["README.md", "*/README.md", "*/docs/*.md"], ["*/squared/*"]),
    "square": (["README.md", "docs/*.md"], []),
    "sqgui": (["README.md", "docs/*.md"], []),
    "apkpack": (["README.md", "docs/*.md"], []),
    "sqedit": (["README.md", "docs/*.md"], []),
    "manuals": (["README.md", "docs/*.md"], []),
    "squared-kits": (["README.md", "docs/*.md"], []),
}
NEVER = ["*third_party/*", "*third-party/*", ".github/*", "*/build/*"]


# ---------------------------------------------------------------- markdown

def slug(text):
    s = re.sub(r"<[^>]+>", "", text).strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
AUTO = re.compile(r"&lt;(https?://[^&\s]+)&gt;")


def inline(text, link):
    """Inline markdown in one line of text: code first (nothing inside it is
    read, and it stands as a placeholder while the rest is read, so emphasis
    can span it), then links, emphasis."""
    codes = []

    def hold(m):
        codes.append(f"<code>{E(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    s = E(CODE.sub(hold, text), quote=False)
    s = AUTO.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)
    s = LINK.sub(lambda m: (f'<a href="{E(link(html.unescape(m.group(3))))}">{m.group(2) or html.unescape(m.group(3))}</a>'), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<i>\1</i>", s)
    return re.sub("\x00(\\d+)\x00", lambda m: codes[int(m.group(1))], s)


LIST_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def convert(md, link):
    """Markdown to HTML; also the page's title (its first heading) and its
    headings, for the search index."""
    lines = md.replace("\t", "    ").split("\n")
    out, headings, title = [], [], None
    i, n = 0, len(lines)
    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(x.strip() for x in para), link) + "</p>")
            para.clear()

    while i < n:
        line = lines[i]
        stripped = line.strip()
        fence = re.match(r"^\s*(```+|~~~+)\s*([\w+.-]*)", line)
        if fence:
            flush()
            mark, lang = fence.group(1), fence.group(2)
            body = []
            i += 1
            while i < n and not lines[i].strip().startswith(mark[:3]):
                body.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{E(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{E(chr(10).join(body))}</code></pre>")
            continue
        h = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if h:
            flush()
            level, text = len(h.group(1)), h.group(2)
            rendered = inline(text, link)
            anchor = slug(rendered)
            if title is None:
                title = re.sub(r"<[^>]+>", "", rendered)
            headings.append(re.sub(r"<[^>]+>", "", rendered))
            out.append(f'<h{level} id="{anchor}">{rendered}</h{level}>')
            i += 1
            continue
        if re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", line):
            flush()
            out.append("<hr>")
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            flush()
            def cells(row):
                row = row.strip().strip("|")
                return [c.strip() for c in re.split(r"(?<!\\)\|", row)]
            head = cells(line)
            rows = []
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            t = ["<div class=\"tablewrap\"><table><thead><tr>"]
            t += [f"<th>{inline(c, link)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c, link)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if stripped.startswith(">"):
            flush()
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner, _, _ = convert("\n".join(quote), link)
            out.append(f"<blockquote>{inner}</blockquote>")
            continue
        if LIST_ITEM.match(line) and (not para or not line.startswith(" ")):
            flush()
            items, stack = [], []
            # Collect the list: items, their continuation lines, nested lists.
            block = []
            while i < n and (LIST_ITEM.match(lines[i]) or (lines[i].startswith("  ") and lines[i].strip()) or
                             (not lines[i].strip() and i + 1 < n and (LIST_ITEM.match(lines[i + 1]) or lines[i + 1].startswith("  ")))):
                block.append(lines[i])
                i += 1
            out.append(render_list(block, link))
            continue
        if not stripped:
            flush()
            i += 1
            continue
        para.append(line)
        i += 1
    flush()
    return "\n".join(out), title, headings


def render_list(block, link):
    """A list and the lists nested in it, by indentation."""
    html_out = []
    stack = []  # (indent, tag)
    item_open = False
    for line in block:
        m = LIST_ITEM.match(line)
        if m:
            indent = len(m.group(1))
            tag = "ol" if m.group(2)[0].isdigit() else "ul"
            while stack and indent < stack[-1][0]:
                html_out.append(f"</li></{stack.pop()[1]}>")
            if not stack or indent > stack[-1][0]:
                stack.append((indent, tag))
                html_out.append(f"<{tag}>")
            elif item_open:
                html_out.append("</li>")
            text = m.group(3)
            box = re.match(r"^\[( |x|X)\]\s+(.*)$", text)
            if box:
                mark = "&#9745; " if box.group(1) != " " else "&#9744; "
                html_out.append("<li>" + mark + inline(box.group(2), link))
            else:
                html_out.append("<li>" + inline(text, link))
            item_open = True
        elif line.strip():
            html_out.append(" " + inline(line.strip(), link))
    while stack:
        html_out.append(f"</li></{stack.pop()[1]}>")
    return "".join(html_out)


# ---------------------------------------------------------------- gathering

def git(repo_dir, *args):
    return subprocess.run(["git", "-C", repo_dir, *args], check=True, capture_output=True).stdout


def ref_of(repo_dir):
    """The commit to read: SQ_DOCS_REF (origin/main), else HEAD."""
    for ref in (os.environ.get("SQ_DOCS_REF", "origin/main"), "HEAD"):
        try:
            return git(repo_dir, "rev-parse", "--verify", "--quiet", ref + "^{commit}").decode().strip()
        except (OSError, subprocess.CalledProcessError):
            continue
    return None


def tracked_markdown(repo_dir, ref):
    names = git(repo_dir, "ls-tree", "-r", "--name-only", ref).decode("utf-8", "replace").split("\n")
    return [x for x in names if x.endswith(".md")]


def wanted(path, take, leave):
    if any(fnmatch.fnmatch(path, p) for p in NEVER + leave):
        return False
    return any(fnmatch.fnmatch(path, p) for p in take)


def page_path(repo, src):
    """docs/<repo>/<src>.html, src's .md (README.md: index) replaced."""
    base = src[:-3]
    if os.path.basename(base) == "README":
        base = os.path.join(os.path.dirname(base), "index")
    return os.path.join("docs", repo, base + ".html")


def build(root, owner, layout):
    """Write the gathered documents; returns how many pages were written."""
    parent = os.environ.get("SQ_REPOS") or os.path.dirname(root)
    pages = {}  # (repo, src) -> out path, for every document found
    found = {}
    for repo, (take, leave) in SOURCES.items():
        rdir = os.path.join(parent, repo)
        ref = ref_of(rdir) if os.path.isdir(rdir) else None
        if ref is None:
            continue
        docs = sorted(p for p in tracked_markdown(rdir, ref) if wanted(p, take, leave))
        if not docs:
            continue
        found[repo] = (ref, docs)
        for src in docs:
            pages[(repo, src)] = page_path(repo, src)

    index_path = os.path.join(root, "docs", "search-index.json")
    try:
        with open(index_path) as f:
            entries = {e["u"]: e for e in json.load(f)}
    except (OSError, ValueError):
        entries = {}
    written = 0
    for repo, (ref, docs) in found.items():
        # A repository's pages are written afresh: the ones it no longer has go.
        for e in [u for u, e in entries.items() if e["r"] == repo]:
            del entries[e]
        stale = os.path.join(root, "docs", repo)
        for d, _, files in os.walk(stale, topdown=False):
            for f in files:
                if f.endswith(".html"):
                    os.remove(os.path.join(d, f))
        for src in docs:
            out = pages[(repo, src)]
            src_dir = os.path.dirname(src)

            def link(target, out=out, src_dir=src_dir, repo=repo):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    return target
                path, _, frag = target.partition("#")
                full = os.path.normpath(os.path.join(src_dir, path)).replace(os.sep, "/")
                if (repo, full) in pages:
                    rel = os.path.relpath(pages[(repo, full)], os.path.dirname(out))
                    return urllib.parse.quote(rel) + ("#" + frag if frag else "")
                if full.startswith(".."):
                    return target
                return f"https://github.com/{owner}/{repo}/blob/main/{full}" + ("#" + frag if frag else "")

            md = git(os.path.join(parent, repo), "show", f"{ref}:{src}").decode("utf-8", "replace")
            body, title, headings = convert(md, link)
            if not title or "{{" in title:  # a template's placeholder is no title
                title = f"{os.path.dirname(src) or repo}/{os.path.basename(src)}"
            depth = out.count("/")
            crumbs = (f'<p class="crumbs"><a href="{"../" * (depth - 1)}index.html">Docs</a> · '
                      f'<a href="{"../" * (depth - 2)}index.html">{E(repo)}</a> · <code>{E(src)}</code> · '
                      f'<a href="https://github.com/{owner}/{repo}/blob/main/{E(src)}">on GitHub</a></p>')
            page = layout(f"{title} · {repo}", f'<article class="doc">{crumbs}{body}</article>', depth=depth,
                          description=f"{repo}: {title}")
            os.makedirs(os.path.dirname(os.path.join(root, out)), exist_ok=True)
            with open(os.path.join(root, out), "w") as f:
                f.write(page)
            text = re.sub(r"```.*?```", " ", md, flags=re.S)
            text = re.sub(r"[#>*_`|\[\]()-]+", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            entries[out] = {"u": out, "r": repo, "p": src, "t": title, "h": headings[:40], "x": text[:20000]}
            written += 1

    # The docs' own index: every repository's documents, by folder.
    by_repo = {}
    for e in entries.values():
        by_repo.setdefault(e["r"], []).append(e)
    parts = ['<article class="doc"><h1>Documentation</h1>',
             '<p>Every tool\'s documents, gathered from its repository. Search them from the box above.</p>']
    for repo in sorted(by_repo):
        parts.append(f'<h2 id="{E(repo)}">{E(repo)}</h2><ul>')
        for e in sorted(by_repo[repo], key=lambda e: e["p"]):
            href = os.path.relpath(e["u"], "docs")
            parts.append(f'<li><a href="{E(urllib.parse.quote(href))}">{E(e["t"])}</a> <span class="path">{E(e["p"])}</span></li>')
        parts.append("</ul>")
        index = os.path.join(root, "docs", repo, "index.html")
        if not os.path.exists(index):
            # A repository with no README: a page listing its documents.
            items = "".join(f'<li><a href="{E(urllib.parse.quote(os.path.relpath(e["u"], os.path.join("docs", repo))))}">{E(e["t"])}</a></li>'
                            for e in sorted(by_repo[repo], key=lambda e: e["p"]))
            with open(index, "w") as f:
                f.write(layout(repo, f'<article class="doc"><h1>{E(repo)}</h1><ul>{items}</ul></article>', depth=2))
    parts.append("</article>")
    os.makedirs(os.path.join(root, "docs"), exist_ok=True)
    with open(os.path.join(root, "docs", "index.html"), "w") as f:
        f.write(layout("Documentation", "".join(parts), depth=1, description="Every squared tool's documentation"))
    with open(os.path.join(root, "docs", "search.html"), "w") as f:
        f.write(layout("Search", '<article class="doc"><h1>Search</h1><div id="results"><p>Searching…</p></div>'
                                 '</article><script src="../assets/search.js"></script>', depth=1))
    with open(index_path, "w") as f:
        json.dump(sorted(entries.values(), key=lambda e: e["u"]), f, separators=(",", ":"))
    return written, sorted(found)
