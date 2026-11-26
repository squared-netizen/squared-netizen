"""The facts behind every page. Edit here, then: python3 tools/build.py

Each project: the infobox, a lead, a one-paragraph summary, a concept sketch,
an architecture summary, features, use cases and references. [[key]] in any
text cites the reference with that key. Written from each repository's
documentation and, where it was thin or disagreed with itself, its code.
"""

OWNER = "squared-netizen"
GH = f"https://github.com/{OWNER}"


def diagram(width, height, boxes, arrows, soft=()):
    """A small box-and-arrow sketch. boxes: (id, x, y, w, h, label, sub).
    arrows: (from_id, to_id, label)."""
    at = {b[0]: b for b in boxes}
    out = [f'<svg viewBox="0 0 {width} {height}" role="img" xmlns="http://www.w3.org/2000/svg">',
           '<defs><marker id="a" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" '
           'orient="auto"><path class="ar" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for f, t, label in arrows:
        _, x1, y1, w1, h1, *_ = at[f]
        _, x2, y2, w2, h2, *_ = at[t]
        ax, ay = x1 + w1 / 2, y1 + h1 / 2
        bx, by = x2 + w2 / 2, y2 + h2 / 2
        # leave the box on the side facing the other
        if abs(bx - ax) * h1 > abs(by - ay) * w1:
            sx = ax + (w1 / 2 if bx > ax else -w1 / 2); sy = ay
            ex = bx - (w2 / 2 if bx > ax else -w2 / 2); ey = by
        else:
            sx = ax; sy = ay + (h1 / 2 if by > ay else -h1 / 2)
            ex = bx; ey = by - (h2 / 2 if by > ay else -h2 / 2)
        out.append(f'<path class="ln" d="M{sx:.0f},{sy:.0f} L{ex:.0f},{ey:.0f}" marker-end="url(#a)"/>')
        if label:
            out.append(f'<text class="sm" x="{(sx + ex) / 2 + 4:.0f}" y="{(sy + ey) / 2 - 4:.0f}">{label}</text>')
    for b in boxes:
        i, x, y, w, h, label, sub = b
        cls = "bx2" if i in soft else "bx"
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>')
        ty = y + h / 2 + (0 if sub else 4)
        out.append(f'<text x="{x + w / 2}" y="{ty:.0f}" text-anchor="middle" font-size="13" font-weight="600">{label}</text>')
        if sub:
            out.append(f'<text class="sm" x="{x + w / 2}" y="{ty + 15:.0f}" text-anchor="middle">{sub}</text>')
    out.append("</svg>")
    return "".join(out)


ECOSYSTEM_SKETCH = diagram(
    300, 210,
    [("sq", 10, 10, 120, 44, "squared", "framework"),
     ("cart", 170, 10, 120, 44, "sqcart", ".sq format"),
     ("pg", 90, 85, 120, 44, "squared-pg", "generator"),
     ("term", 10, 160, 120, 44, "sqterm", "terminal app"),
     ("ex", 170, 160, 120, 44, "examples", "demo apps")],
    [("sq", "pg", ""), ("cart", "pg", ""), ("pg", "ex", ""), ("sq", "term", "")])

PROJECTS = [
    {
        "id": "squared", "name": "squared", "repo": "squared", "kind": "C++ framework",
        "status": "Active, rewrite in progress", "status_class": "s-active",
        "lead_plain": "A C++23 framework for Linux and Android, built as named modules, for games, "
                      "simulation software and tooling.",
        "lead": "<b>squared</b> is a cross-platform software development kit for Linux and Android, "
                "written in C++23 as named modules, with a Lua 5.4 scripting layer, for games, "
                "simulation software and tooling.[[readme-fw]] It is undergoing a ground-up rewrite, "
                "and its APIs are not yet stable.[[readme]]",
        "infobox": [
            ("Type", "Software development kit (framework)"),
            ("Language", "C++23 (named modules, <code>import std</code>); Lua 5.4"),
            ("Platforms", "Linux, Android (built on the phone in Termux)"),
            ("Toolchain", "clang and libc++; make"),
            ("Status", "Ground-up rewrite; unstable[[readme]]"),
            ("Licence", "MIT[[license]]"),
            ("Repository", f'<a href="{GH}/squared">{OWNER}/squared</a>'),
        ],
        "sketch": diagram(270, 150,
                          [("ui", 10, 10, 115, 44, "Stage", "UI thread"),
                           ("tg", 145, 10, 115, 44, "Telegraph", "messages"),
                           ("m", 145, 96, 115, 44, "Model", "own thread"),
                           ("p", 10, 96, 115, 44, "Platform", "Android, Linux")],
                          [("ui", "tg", ""), ("tg", "m", ""), ("p", "ui", "")], soft=("tg",)),
        "sketch_caption": "An app's two halves meet in the Telegraph",
        "summary": "squared is published as a package repository: its framework lives under "
                   "<code>packages/package.squared-core</code> and its application templates under "
                   "<code>templates/</code>, and its one consumer is the squared-pg project generator, which "
                   "copies them into a workspace the developer owns.[[readme]] Code is written against "
                   "<code>import squared;</code> or a single module such as <code>import sq.gui;</code>.[[readme-fw]] "
                   "An application is split into a model, running on its own thread, and a Stage of screens "
                   "and panes on the UI thread; the two exchange messages and snapshots through a "
                   "Telegraph.[[stage]] On Android the platform layer is a NativeActivity with no Java of its own, "
                   "and the APK is built with make, without Gradle.[[template]]",
        "concept": diagram(620, 210,
                           [("app", 10, 20, 150, 50, "Your app", "import squared;"),
                            ("stage", 230, 20, 150, 50, "Stage, gui", "screens, panes"),
                            ("msg", 230, 120, 150, 50, "messaging", "Telegraph"),
                            ("model", 450, 120, 150, 50, "Model", "its own thread"),
                            ("mods", 450, 20, 150, 50, "modules", "files, font, gles, term..."),
                            ("plat", 10, 120, 150, 50, "Platform layer", "NativeActivity, Linux")],
                           [("app", "stage", ""), ("stage", "msg", ""), ("msg", "model", ""),
                            ("stage", "mods", ""), ("plat", "app", "")], soft=("msg",)),
        "concept_caption": "An application on squared: the platform starts it, the Stage draws it, the model runs apart from it.",
        "architecture": [
            ("Modules", "One named module per directory: <code>app</code>, <code>assets</code>, <code>console</code>, "
                        "<code>data</code>, <code>dev</code>, <code>files</code>, <code>font</code>, <code>gles</code>, "
                        "<code>graphics</code>, <code>gui</code>, <code>math</code>, <code>messaging</code>, "
                        "<code>stage</code>, <code>term</code> and <code>time</code>, each built from a partition per "
                        "everyday type, with implementation units and tests beside it.[[readme-fw]] The standard "
                        "library comes in as <code>import std</code>, from libc++'s module sources pinned in "
                        "<code>third_party/libcxx</code>.[[readme-fw]]"),
            ("Application model", "The App holds the Telegraph, with the model at its far end and the Stage at its "
                                  "near end; there is one App for the process.[[stage]] The model runs on its own "
                                  "thread and publishes snapshots; the Stage, on the UI thread, owns screens, panes "
                                  "and widgets, and the platform delivers input and the window to it.[[stage]]"),
            ("Platform", "The Android template is a NativeActivity in C++ with no classes.dex unless asked for: running "
                         "in the background adds a tiny generated dex (<code>tools/dexgen</code>) for a foreground "
                         "service.[[template]] Desktop Linux runs the same application code.[[readme-fw]]"),
            ("Build", "make and clang with libc++. Module interfaces and objects go through a build cache keyed by what "
                      "they read, shared between workspaces.[[history]]"),
            ("Layouts", "Screens can be described in JSON files, <code>sq_app/layouts/</code>, which sqgen compiles into "
                        "constant tables.[[layouts]] The planned visual editor, sqgui, will read and write the same "
                        "files and take in sqgen."),
            ("Packages (planned)", "squared-core stays the framework every application uses, and its "
                                   "<code>math</code> stays small. Add-on packages, each in its own repository, will "
                                   "extend it in one field: squared-math, -language, -physics, -chem, -bio, -game, "
                                   "-ai, -net and -tui, the first of them to be built. They are built when something needs one, and what nearly all of "
                                   "them share moves into core. See <a href=\"../index.html#sdk\">the squared SDK</a>."),
        ],
        "features": [
            "C++23 named modules throughout, with <code>import std</code>.[[readme-fw]]",
            "Android apps with no Java, no Gradle and no Android Studio, built and installed from a phone.[[template]]",
            "A model on its own thread, a UI on another, and a message line between them (the Telegraph).[[stage]]",
            "A GUI of screens, panes and widgets, with pinch zoom for every app, kept across launches.[[history]]",
            "Text through FreeType: font sets with system fallbacks and a glyph atlas.[[history]]",
            "A terminal core (<code>sq::term</code>): an ECMA-48 parser, a cell grid with scrollback, and a pty.[[history]]",
            "Running in the background on Android: a foreground service with a notification and an optional wake lock.[[history]]",
            "A development Console reachable from Termux, and log lines sent over UDP in development builds.[[template]]",
        ],
        "use_cases": [
            "Writing an Android app entirely on a phone, from generation to install.",
            "A terminal emulator: <a href=\"sqterm.html\">sqterm</a> is written on squared.",
            "Games and simulations that keep their model apart from their UI.",
            "Tools for Linux that share code with an Android app.",
        ],
        "refs": [
            ("readme", "squared: README", f"{GH}/squared/blob/main/README.md"),
            ("license", "squared: LICENSE", f"{GH}/squared/blob/main/LICENSE"),
            ("readme-fw", "squared framework: README", f"{GH}/squared/blob/main/packages/package.squared-core/tree/squared/README.md"),
            ("layouts", "squared: programmer's guide to layouts", f"{GH}/squared/blob/main/packages/package.squared-core/tree/squared/docs/programmer/layouts.md"),
            ("stage", "squared: programmer's guide to the Stage", f"{GH}/squared/blob/main/packages/package.squared-core/tree/squared/docs/programmer/stage.md"),
            ("template", "squared: the Android application template", f"{GH}/squared/tree/main/templates/template.android.cpp"),
            ("history", "squared: commit history", f"{GH}/squared/commits/main"),
        ],
    },
    {
        "id": "squared-pg", "name": "squared-pg", "repo": "squared-pg", "kind": "Project generator",
        "status": "Active", "status_class": "s-active",
        "lead_plain": "An offline-first project generator for squared: a C++20 engine sequenced by Lua 5.4 "
                      "workflows, writing a workspace the developer owns.",
        "lead": "<b>squared-pg</b> is an offline-first project generator for applications built on the squared "
                "framework. A native C++20 engine provides the generation capability and a Lua 5.4 control layer "
                "sequences it into workflows; the output is a self-contained workspace the developer owns "
                "outright.[[readme]]",
        "infobox": [
            ("Type", "Project generator (command-line tool and library)"),
            ("Language", "C++20 engine; Lua 5.4 workflows"),
            ("Command", "<code>sqpg</code>"),
            ("Platforms", "Termux on Android (first-class), Linux, other desktops[[building]]"),
            ("Network", "None at any point; the vendored third-party sources are the whole dependency list[[readme]]"),
            ("Licence", "MIT[[license]]"),
            ("Repository", f'<a href="{GH}/squared-pg">{OWNER}/squared-pg</a>'),
        ],
        "sketch": diagram(270, 150,
                          [("in", 10, 10, 115, 44, "Input", "CLI, tools"),
                           ("lua", 145, 10, 115, 44, "Lua workflow", "decides"),
                           ("eng", 145, 96, 115, 44, "Engine", "C++20"),
                           ("ws", 10, 96, 115, 44, "Workspace", "yours")],
                          [("in", "lua", ""), ("lua", "eng", ""), ("eng", "ws", "")]),
        "sketch_caption": "Input, workflow, engine, workspace",
        "summary": "The engine is a programmable pipeline: it knows what a template, a kit, a package and an asset are, "
                   "and how to resolve, validate and materialise them, but it does not decide which ones are wanted. "
                   "Lua does: it parses arguments, loads configuration, chooses the template and kits, and calls engine "
                   "operations in whatever order a workflow needs, so workflows can change after release without a "
                   "rebuild.[[readme]] The command-line tool <code>sqpg</code> is one consumer of that stack. A bootstrap "
                   "script clones squared and sqcart beside it, and <code>sqpg initialize</code> lays out an environment "
                   "of a version-controlled project tree, a sandbox and the tools.[[readme]]",
        "concept": diagram(620, 200,
                           [("user", 10, 75, 120, 50, "You", "sqpg new ..."),
                            ("lua", 170, 75, 130, 50, "Lua workflow", "lua/"),
                            ("eng", 340, 75, 130, 50, "Engine", "engine/"),
                            ("res", 340, 0, 130, 50, "Resources", "templates, kits"),
                            ("ws", 500, 75, 110, 50, "Workspace", "make, run"),
                            ("cart", 340, 150, 130, 46, "sqcart", ".sq cartridges")],
                           [("user", "lua", ""), ("lua", "eng", ""), ("res", "eng", ""),
                            ("cart", "eng", ""), ("eng", "ws", "")], soft=("res", "cart")),
        "concept_caption": "A request becomes a workspace: Lua chooses, the engine resolves and writes.",
        "architecture": [
            ("Engine", "A C++20 engine with a lifecycle state machine and a set of core services, exposed as an "
                       "enumerable set of operations; its public headers are under <code>engine/include</code>, and a "
                       "binding layer under <code>engine/lua</code> keeps the C++ and Lua boundary narrow.[[readme]][[agents]]"),
            ("Workflows", "Lua 5.4 modules in <code>lua/</code> sequence the engine's operations: list, new, plan and "
                          "initialize are workflows, not fixed code paths.[[readme]]"),
            ("Resources", "Templates, kits, packages and assets are inert data under <code>resources/</code>; the "
                          "squared package repository and sqcart are brought in beside it.[[readme]]"),
            ("In the SDK", "sqpg is the tool that <i>creates</i>: it sets up a workspace tree and generates a "
                           "project from a template, kits and packages, and it is installed in <code>bin</code> "
                           "like any other tool. Managing the workspace afterwards is square's job: every question "
                           "about a manifest goes to square, which asks sqcart. Building is sqmake's. See "
                           "<a href=\"../index.html#sdk\">the squared SDK</a>."),
            ("Building (planned)", "Generated projects build with make today. The plan is for the build step to "
                                   "go through <b>sqmake</b>, a separate library and command line that runs the "
                                   "build itself from a short Lua build file, with no generated make, CMake or "
                                   "Ninja files; it knows how to build, not what a workspace is."),
            ("Specification", "A functional specification, kept as an Obsidian vault with a decision log and open "
                              "questions, guides the design; during the initial implementation the repository is "
                              "the ground truth and the specification is amended to match.[[agents]]"),
        ],
        "features": [
            "Generates terminal and Android applications from templates, with kits that add capabilities such as OpenGL or a Lua workspace.[[readme]]",
            "<code>sqpg plan</code> shows what a generation would do without doing it.[[readme]]",
            "Builds and runs with a C++20 compiler and make alone; CMake is optional.[[building]]",
            "No network at build or run time.[[readme]]",
            "Workflows editable after release, without rebuilding the engine.[[readme]]",
            "Tools that keep squared's templates and a generated project in step (template drift checks, porting back to the template).[[history]]",
        ],
        "use_cases": [
            "<code>sqpg new hello --template template.terminal.cpp --kit kit.terminal</code>, then <code>make</code>: a terminal program.[[readme]]",
            "An Android app on a phone with no Gradle: <code>--template template.android.cpp --platform android</code>, then <code>make apk</code>.[[readme]]",
            "Adding a Lua script workspace beside the C++ one with <code>--kit kit.lua</code>.[[readme]]",
        ],
        "refs": [
            ("readme", "squared-pg: README", f"{GH}/squared-pg/blob/main/README.md"),
            ("building", "squared-pg: BUILDING", f"{GH}/squared-pg/blob/main/BUILDING.md"),
            ("agents", "squared-pg: AGENTS (project context and rules)", f"{GH}/squared-pg/blob/main/AGENTS.md"),
            ("license", "squared-pg: LICENSE", f"{GH}/squared-pg/blob/main/LICENSE"),
            ("history", "squared-pg: commit history", f"{GH}/squared-pg/commits/main"),
        ],
    },
    {
        "id": "sqcart", "name": "sqcart", "repo": "sqcart", "kind": "Container format library",
        "status": "Specified; reference implementation", "status_class": "s-wip",
        "lead_plain": "The reference implementation of the Squared Cartridge format (.sq): a container for "
                      "templates, kits, packages, assets, plugins and applications.",
        "lead": "<b>sqcart</b> is the reference implementation of the Squared Cartridge Specification 2.0, the "
                "<code>.sq</code> container format used for squared's templates, kits, packages, asset bundles, "
                "plugins and distributable applications. It is standalone C++20, with no dependency on squared-pg "
                "or on the squared framework.[[readme]]",
        "infobox": [
            ("Type", "Library and command-line tool for a container format"),
            ("Language", "C++20"),
            ("Format", "<code>.sq</code>, Squared Cartridge 2.0[[spec]]"),
            ("Libraries", "<code>sqcart::read</code>, <code>sqcart::write</code>; a CLI[[readme]]"),
            ("Backends", "miniz and yyjson, vendored or supplied by the host[[readme]]"),
            ("Licence", "MIT[[license]]"),
            ("Repository", f'<a href="{GH}/sqcart">{OWNER}/sqcart</a>'),
        ],
        "sketch": diagram(270, 150,
                          [("c", 70, 10, 130, 44, "name.sq", "the cartridge"),
                           ("m", 10, 96, 115, 44, "SQ-INF/", "manifest.json"),
                           ("t", 145, 96, 115, 44, "payload", "tree, data")],
                          [("c", "m", ""), ("c", "t", "")]),
        "sketch_caption": "A cartridge: a manifest and its payload",
        "summary": "A cartridge carries a manifest, <code>SQ-INF/manifest.json</code>, with a fixed envelope common "
                   "to every kind (format, version, kind, id, version, licence) and the payload that kind "
                   "describes.[[spec]] The kind is an opaque token rather than a closed set, and the role of a file "
                   "is never inferred from its name: there is a single <code>.sq</code> extension.[[spec]] The "
                   "library is split so a runtime or an Android launcher links the reader alone, carrying no "
                   "compressor, canonical-ordering logic or manifest writer.[[readme]] The longer aim is "
                   "high-capacity, high-performance containers that hold both very large datasets and executable "
                   "extensions.[[readme]]",
        "concept": diagram(620, 190,
                           [("author", 10, 70, 120, 50, "Author", "kit, template"),
                            ("w", 170, 70, 130, 50, "sqcart::write", "pack, sign order"),
                            ("sq", 340, 70, 110, 50, ".sq", "cartridge"),
                            ("r", 490, 20, 120, 50, "sqcart::read", "squared-pg"),
                            ("r2", 490, 120, 120, 50, "sqcart::read", "a runtime, launcher")],
                           [("author", "w", ""), ("w", "sq", ""), ("sq", "r", ""), ("sq", "r2", "")],
                           soft=("sq",)),
        "concept_caption": "Written once by a packaging tool, read by the generator or by a runtime that carries only the reader.",
        "architecture": [
            ("Targets", "<code>sqcart::read</code> (always built), <code>sqcart::write</code> (packaging tools), a "
                        "<code>sqcart</code> command-line tool for people and CI, and a deferred Lua binding.[[readme]]"),
            ("Manifest", "The envelope is common to every kind and versioned; a reader refuses a format version it "
                         "does not know, in either direction.[[spec]]"),
            ("Embedding", "A host can supply its own miniz and yyjson (<code>SQCART_USE_EXTERNAL_MINIZ</code>, "
                          "<code>SQCART_USE_EXTERNAL_YYJSON</code>) and link the reader into its own target.[[readme]]"),
            ("In the SDK", "sqcart is the lowest-level user of the cartridge specification and knows nothing of "
                           "workspaces. The planned manager, square, is the tool that does: other tools ask square "
                           "about a manifest, and square asks sqcart and answers in JSON, so a change in sqcart "
                           "touches square alone. See <a href=\"../index.html#sdk\">the squared SDK</a>."),
        ],
        "features": [
            "One container format for templates, kits, packages, asset bundles, plugins and applications.[[readme]]",
            "A read-only library small enough for a runtime.[[readme]]",
            "Builds with CMake or, on Termux, with <code>make check</code>.[[readme]]",
            "Offline by construction: no network resolution of any kind in the format.[[spec]]",
        ],
        "use_cases": [
            "squared-pg reading templates and kits as cartridges.",
            "square answering the other tools' questions about a workspace's manifests.",
            "Shipping an asset bundle or plugin that a squared app opens read-only.",
            "sqterm's packages reuse the cartridge manifest envelope (kind <code>package</code>) for <code>pkg</code>.[[sqterm-pkg]]",
        ],
        "refs": [
            ("readme", "sqcart: README", f"{GH}/sqcart/blob/main/README.md"),
            ("license", "sqcart: LICENSE", f"{GH}/sqcart/blob/main/LICENSE"),
            ("spec", "Squared Cartridge Specification 2.0", f"{GH}/sqcart/blob/main/docs/developer/specs/sq-cartridge-2.0.md"),
            ("sqterm-pkg", "sqterm: packages README (the manifest, and pkg)", f"{GH}/sqterm/blob/main/packages/README.md"),
        ],
    },
    {
        "id": "sqmake", "name": "sqmake", "repo": "sqmake", "kind": "Build system",
        "status": "Specified (draft 0.1); not built yet", "status_class": "s-idle",
        "lead_plain": "The squared SDK's build system: make's model with Ninja's engine, Cargo's conventions, "
                      "CMake's usage requirements and Lua 5.4, running the build itself.",
        "lead": "<b>sqmake</b> is the build system of the squared SDK. It keeps make's model (targets, prerequisites, "
                "rebuild when what a target is made from changes) and drops make's syntax; it runs the build itself "
                "and never writes make, CMake or Ninja files for another tool to run.[[spec]] It builds a workspace "
                "without knowing what one is: it asks square what to build.[[readme]]",
        "infobox": [
            ("Type", "Build system: a library and a thin command line"),
            ("Language", "C++23 modules; build files in Lua 5.4[[spec]]"),
            ("Toolchain", "clang 23, libc++ 23 and bionic, defined once in squared[[spec]]"),
            ("Libraries", "<code>libsqmake</code>; the <code>sqmake</code> CLI[[spec]]"),
            ("Status", "Draft specification 0.1 (2026-11-19); nothing built yet[[readme]]"),
            ("Licence", "MIT[[license]]"),
            ("Repository", f'<a href="{GH}/sqmake">{OWNER}/sqmake</a>'),
        ],
        "sketch": diagram(270, 150,
                          [("l", 10, 10, 115, 44, "build.lua", "a project"),
                           ("g", 145, 10, 115, 44, "the graph", "files, commands"),
                           ("o", 78, 96, 115, 44, "outputs", "only what is stale")],
                          [("l", "g", ""), ("g", "o", "")]),
        "sketch_caption": "A build file becomes a graph; only what is out of date runs",
        "summary": "A target is rebuilt when an input is newer, when its command's hash changed, when a header its "
                   "compile read changed, when a module it imports was rebuilt, or when the toolchain changed: the "
                   "toolchain's fingerprint, a hash of the compiler's version, the C++ library's version, the target "
                   "and every flag that changes a compiled module, is part of every command's hash.[[spec]] Commands "
                   "are argument lists run without a shell, and <code>sqmake build --explain</code> prints the whole "
                   "resolved graph and every command.[[spec]] One toolchain builds every C++ module in the SDK, so a "
                   "compiled module never meets one made by another compiler.[[toolchain]]",
        "concept": diagram(620, 190,
                           [("sq", 10, 70, 120, 50, "square", "what to build"),
                            ("mk", 170, 70, 130, 50, "libsqmake", "load, resolve, plan"),
                            ("tc", 170, 150, 130, 36, "toolchain", "clang 23, libc++ 23"),
                            ("run", 340, 70, 120, 50, "run", "a thread pool"),
                            ("out", 500, 70, 110, 50, "build/", "objects, BMIs")],
                           [("sq", "mk", ""), ("tc", "mk", ""), ("mk", "run", ""), ("run", "out", "")],
                           soft=("out",)),
        "concept_caption": "square says what to build; sqmake plans it with the SDK's one toolchain and runs what is stale.",
        "architecture": [
            ("Stages", "Load (Lua registers toolchains, rules and targets), Resolve (conventions and usage "
                       "requirements), Plan (a graph, module dependencies included; a cycle is refused), Check (what "
                       "is out of date), Run (a thread pool).[[spec]]"),
            ("Modules", "<code>clang-scan-deps</code> orders the compiles; compiled modules are outputs in the graph, "
                        "kept in a folder named by the toolchain's fingerprint, with one <code>std</code> module per "
                        "fingerprint; a library written as modules is built from its sources by its "
                        "consumer.[[spec]]"),
            ("Toolchain", "Defined once, in squared (<code>build/toolchain.sh</code>): the flags that change a "
                          "compiled module are the toolchain's, never a target's, and a target asking for another is "
                          "refused with a plain message.[[spec]][[toolchain]]"),
            ("Lua", "Standalone, sqmake owns its Lua state; embedded (in sqpg), it uses the host's, in its own "
                    "<code>sqmake</code> table, and build files run sandboxed.[[spec]]"),
            ("In the SDK", "sqpg creates a workspace, square manages it, and sqmake builds it. See "
                           "<a href=\"../index.html#sdk\">the squared SDK</a>."),
        ],
        "features": [
            "make's model without make's syntax: named inputs and outputs, explicit rules, ordinary Lua functions.[[spec]]",
            "Rebuilds on command and toolchain changes as well as file times, and on headers the compiler reports.[[spec]]",
            "C++23 modules ordered by <code>clang-scan-deps</code>, from sqterm's <code>llvm</code> package.[[spec]]",
            "Offline, no daemon, one small binary; it runs on the phone in sqterm.[[spec]]",
        ],
        "use_cases": [
            "Building a workspace sqpg created, from the inputs square names.",
            "An IDE or tool embedding <code>libsqmake</code> to build and to show the graph.",
            "Building squared and the kits with the same toolchain as applications (an open question).[[spec]]",
        ],
        "refs": [
            ("readme", "sqmake: README", f"{GH}/sqmake/blob/main/README.md"),
            ("license", "sqmake: LICENSE", f"{GH}/sqmake/blob/main/LICENSE"),
            ("spec", "sqmake: draft specification 0.1", f"{GH}/sqmake/blob/main/docs/spec.md"),
            ("toolchain", "squared: build/toolchain.sh (the SDK's one toolchain)",
             f"{GH}/squared/blob/main/packages/package.squared-core/tree/squared/build/toolchain.sh"),
        ],
    },
    {
        "id": "sqterm", "name": "sqterm", "repo": "sqterm", "kind": "Android terminal app",
        "status": "Active (Sprint 12)", "status_class": "s-active",
        "lead_plain": "A terminal for Android written on squared, with its own prefix of packages: zsh, bash, "
                      "the GNU tools, make and clang 23.",
        "lead": "<b>sqterm</b> is a terminal emulator for Android written as a squared application: a shell in a "
                "pseudo-terminal, drawn by squared, with no Java of its own. It is inspired by Termux and is "
                "side-loaded rather than published on Google Play.[[readme]]",
        "infobox": [
            ("Type", "Terminal emulator"),
            ("Platform", "Android (arm64), target SDK 28"),
            ("Language", "C++23 on squared"),
            ("Shell", "zsh 5.9.2 from its own prefix; bash 5.3"),
            ("Toolchain", "clang 23.1.5, lld, libc++ 23; clang-format, clang-scan-deps, clangd, clang-tidy, clang-doc; built for the phone[[packages]]"),
            ("Licence", "MIT[[license]]; its fonts and FreeType carry their own[[notice]]"),
            ("Repository", f'<a href="{GH}/sqterm">{OWNER}/sqterm</a>'),
        ],
        "sketch": diagram(270, 150,
                          [("v", 10, 10, 115, 44, "TerminalView", "UI thread"),
                           ("s", 145, 10, 115, 44, "Shell", "model thread"),
                           ("p", 145, 96, 115, 44, "pty", "zsh, programs"),
                           ("pre", 10, 96, 115, 44, "Prefix", "files/usr")],
                          [("v", "s", ""), ("s", "p", ""), ("pre", "p", "")]),
        "sketch_caption": "The view, the shell, and the prefix the shell runs from",
        "summary": "The shell runs in a pseudo-terminal on the model's thread, its output parsed by squared's terminal "
                   "core and published as a snapshot; the TerminalView draws the newest screen from one glyph texture "
                   "on the UI thread.[[readme]] Its programs come from its own prefix, <code>files/usr</code>, filled "
                   "from packages: a few carried in the APK and unpacked at first start, and larger ones installed "
                   "with <code>pkg</code> from a file.[[packages]] GitHub Actions builds every package for Android API 28 "
                   "and publishes it to a release; the phone fetches them as a deliberate step, and every build stays "
                   "offline.[[packages]]",
        "concept": diagram(620, 210,
                           [("ci", 10, 10, 140, 50, "GitHub Actions", "recipes, API 28"),
                            ("rel", 10, 120, 140, 50, "Release", "packages"),
                            ("fetch", 200, 120, 140, 50, "fetch_packages", "Termux, on purpose"),
                            ("apk", 200, 10, 140, 50, "APK", "zsh, bash, tools"),
                            ("pkg", 390, 120, 110, 50, "pkg", "install, remove"),
                            ("prefix", 390, 10, 110, 50, "Prefix", "files/usr"),
                            ("shell", 530, 60, 80, 50, "Shell", "zsh")],
                           [("ci", "rel", ""), ("rel", "fetch", ""), ("fetch", "apk", "bundled"),
                            ("fetch", "pkg", "large"), ("apk", "prefix", ""), ("pkg", "prefix", ""),
                            ("prefix", "shell", "")], soft=("rel",)),
        "concept_caption": "Packages are built on CI, fetched on purpose, and installed into sqterm's own prefix.",
        "architecture": [
            ("Application", "A Shell model owns the pty and a <code>sq::term</code> terminal; a TerminalView widget "
                            "draws it and sends keys back; Glyphs holds the fonts, mapped from the APK, and the glyph "
                            "atlas for the whole process.[[readme]]"),
            ("Prefix and packages", "Recipes in <code>packages/</code> build each package; every archive carries a "
                                    "cartridge-style manifest listing its files, which <code>pkg</code> uses to list, "
                                    "upgrade, remove and back up packages. Each package has its own key, so a change "
                                    "rebuilds only it and what depends on it.[[packages]]"),
            ("Toolchain", "clang and lld 23 as one binary, a sysroot built from AOSP's bionic rather than the NDK, and "
                          "static libc++ 23 runtimes with the <code>import std</code> sources. clangd, clang-tidy and "
                          "clang-doc come as a package of their own, so the compiler package stays small.[[packages]]"),
            ("Platform", "Running in the background through squared's foreground service, with a notification and an "
                         "optional wake lock.[[readme]]"),
        ],
        "features": [
            "A shell in a pty with scrollback, rotation and the keys of a hardware keyboard.[[readme]]",
            "Copy and paste the way Termux does it: word selection, handles, and bracketed paste.[[readme]]",
            "Keeps running in the background, with a notification; survives a swipe from the recent apps.[[readme]]",
            "Pinch to scale the font, kept across launches.[[readme]]",
            "Its own prefix with zsh, bash, coreutils, sed, grep, gawk and make.[[packages]]",
            "<code>pkg</code>: list, install from a file (optionally deleting it), remove, back up.[[packages]]",
            "C, C++ and C++23 <code>import std</code> compiled and run on the phone, from the prefix.[[packages]]",
            "The tools around the compiler: clang-format, clang-scan-deps (module dependencies), clangd, clang-tidy and clang-doc.[[packages]]",
        ],
        "use_cases": [
            "A shell on the phone that keeps working with the screen off.",
            "Building and running C and C++ programs on the device, offline.",
            "Long-running jobs (a build, a download) that outlive the app's window.",
        ],
        "refs": [
            ("readme", "sqterm: README", f"{GH}/sqterm/blob/main/README.md"),
            ("packages", "sqterm: packages README", f"{GH}/sqterm/blob/main/packages/README.md"),
            ("license", "sqterm: LICENSE", f"{GH}/sqterm/blob/main/LICENSE"),
            ("notice", "sqterm: NOTICE", f"{GH}/sqterm/blob/main/NOTICE.md"),
            ("actions", "sqterm: packages workflow", f"{GH}/sqterm/blob/main/.github/workflows/packages.yml"),
        ],
    },
    {
        "id": "squared-examples", "name": "squared-examples", "repo": "squared-examples", "kind": "Example apps",
        "status": "Waiting on the generator's rewrite", "status_class": "s-idle",
        "lead_plain": "Complete applications built with squared and squared-pg, kept apart from both so experiments "
                      "cannot change their release code.",
        "lead": "<b>squared-examples</b> holds independent, complete applications built with the squared framework "
                "and the squared-pg generator, kept outside both repositories so that experiments cannot change "
                "their release code.[[readme]]",
        "infobox": [
            ("Type", "Example applications"),
            ("Apps", "demo, hello (Android)[[demo]]"),
            ("Generated by", "squared-pg 0.1.0-alpha.1, <code>template.android.cpp</code>[[demo]]"),
            ("Licence", "MIT[[license]]"),
            ("Repository", f'<a href="{GH}/squared-examples">{OWNER}/squared-examples</a>'),
        ],
        "sketch": diagram(270, 150,
                          [("pg", 75, 10, 120, 44, "squared-pg", "generates"),
                           ("d", 10, 96, 115, 44, "demo", "APK"),
                           ("h", 145, 96, 115, 44, "hello", "APK")],
                          [("pg", "d", ""), ("pg", "h", "")]),
        "sketch_caption": "Generated apps, kept on their own",
        "summary": "The README describes the collection as empty while squared-pg is rewritten; the repository itself "
                   "holds two generated Android applications, <code>demo</code> and <code>hello</code>, each a full "
                   "workspace with its own copy of the framework at a recorded revision "
                   "(<code>SQUARED_REV</code>).[[readme]][[demo]] Each builds an APK with make on a phone, with no "
                   "Gradle, no Android Studio and no Java in the build.[[demo]]",
        "concept": diagram(620, 160,
                           [("sq", 10, 55, 130, 50, "squared", "at a revision"),
                            ("pg", 190, 55, 130, 50, "squared-pg", "generate"),
                            ("ws", 370, 55, 120, 50, "Workspace", "demo, hello"),
                            ("apk", 530, 55, 80, 50, "APK", "install")],
                           [("sq", "pg", ""), ("pg", "ws", ""), ("ws", "apk", "make apk")]),
        "concept_caption": "Each example is a generated workspace that builds on its own.",
        "architecture": [
            ("Workspaces", "Each application is a complete workspace: <code>sq_app/</code> (the application), "
                           "<code>sq_android/</code> (the platform layer), <code>squared/</code> (the vendored framework), "
                           "<code>mk/</code> and <code>tools/</code>.[[demo]]"),
            ("Repository model", "Applications stay outside the framework and generator repositories, so neither can "
                                 "change them by accident.[[readme]]"),
        ],
        "features": [
            "Two Android applications, demo and hello, generated from the Android template.[[demo]]",
            "Build, package, install and run from Termux: <code>make</code>, <code>make apk</code>, <code>make install</code>, <code>make run</code>.[[demo]]",
            "A development Console reachable from Termux, with no adb.[[demo]]",
        ],
        "use_cases": [
            "A known-good app to try squared on a phone.",
            "A reference for what squared-pg generates.",
        ],
        "refs": [
            ("readme", "squared-examples: README", f"{GH}/squared-examples/blob/main/README.md"),
            ("demo", "squared-examples: demo README", f"{GH}/squared-examples/blob/main/demo/README.md"),
            ("license", "squared-examples: LICENSE", f"{GH}/squared-examples/blob/main/LICENSE"),
        ],
    },
]

PLANNED = [
    ("square", "Workspace manager",
     "The one tool that knows what a workspace is. It manages a workspace after sqpg creates it, and answers "
     "every manifest question for the other tools: it asks sqcart and hands them JSON, so a change in how "
     "sqcart works touches square alone. It can also extract a template, kits and packages from a workspace "
     "that has grown to suit its developer, so the next project starts from that layout without writing a "
     "template by hand."),
    ("sqmake", "Build system (library and command line)",
     "Builds an application from a workspace, knowing how to build it rather than what a workspace is. It runs "
     "the build itself, with no generated make, CMake or Ninja files: make's model with Ninja's engine "
     "(command hashes, compiler-written header dependencies), Cargo's conventions, Lua 5.4 as the escape "
     "hatch and CMake's usage requirements. A library, <code>libsqmake</code>, with a thin command line; "
     "offline, no daemon, <code>--explain</code> to show the whole resolved graph."),
    ("sqgui", "Visual UI editor",
     "Edits squared's layouts visually: the JSON layout files an app's screens and panes are built from. It "
     "takes in sqgen, the build step that compiles those files into constant tables, and asks square where "
     "the app and its model are."),
    ("sqedit", "Text tool",
     "A pattern-matching text tool in the spirit of LPeg, to replace sed in the workflow."),
    ("Virtual Cartridge Drive (sqcart 3.0)", "Storage layer",
     "A mutable, disk-backed view over <code>.sq</code> cartridges. Reads resolve against staged changes and "
     "the mounted cartridge; writes are buffered on disk, coalesced, and committed through sqcart's "
     "format-aware operations at chosen times. sqcart stays the authority on what a valid cartridge is."),
    ("Manuals", "Command-line app",
     "A command-line app for storing and managing documentation: man pages, squared's manuals and notes, "
     "listed and searched, and filtered to the tools actually installed. Built to be embedded later in an "
     "IDE or a game engine."),
    ("apkpack", "Build tool",
     "A native replacement for aapt2, zipalign, apksigner and android.jar: an APK built and signed with no "
     "Java and no Android SDK."),
]

# The framework's add-on packages: built only when something needs one, or
# when code added to squared-core grows too large or plainly belongs in one.
# Each its own repository; what nearly all of them share moves into core.
PACKAGES = [
    ("squared-math", "A full calculator, 3D graphics for data visualisation, discrete mathematics and "
                     "calculus, logic, cryptography and blockchain. squared-core keeps only its small "
                     "<code>math</code> module."),
    ("squared-tui", "Character-cell programs: a screen that writes only what changed, typed input, and a "
                    "test bench through sqterm's own emulator; the same program in a terminal or as an app. "
                    "No curses compatibility, no terminfo. Next to be built: "
                    "<a href=\"docs/squared/docs/design/squared-tui.html\">its design</a>."),
    ("squared-language", "Unicode, a bitmap-font packer and converter, text shaping and TrueType."),
    ("squared-physics", "squared's own physics engine: 2D first, inspired by Box2D, then the full thing."),
    ("squared-chem", "Chemistry as software: a working representation of chemical systems."),
    ("squared-bio", "The same for biology."),
    ("squared-game", "The engine of Cataclysm: Dark Days Ahead remade on squared. It takes C:DDA's licence, "
                     "CC BY-SA 3.0; every other package is MIT."),
    ("squared-ai", "Large language models (creating, training, a harness), genetic algorithms, a "
                   "knowledge-based expert-system framework, and classic game AI."),
    ("squared-net", "Talking to the internet, and distributed soft real-time systems."),
]

SDK_SKETCH = diagram(400, 290,
    [("spec", 125, 5, 150, 44, "Cartridge spec", "what a workspace is"),
     ("cart", 125, 80, 150, 44, "sqcart", "reads and writes .sq"),
     ("square", 125, 155, 150, 44, "square", "manages workspaces"),
     ("pg", 5, 240, 120, 44, "sqpg", "creates"),
     ("make", 140, 240, 120, 44, "sqmake", "builds"),
     ("gui", 275, 240, 120, 44, "sqgui", "edits the UI")],
    [("spec", "cart", ""), ("cart", "square", ""), ("square", "pg", ""), ("square", "make", ""),
     ("square", "gui", "")], soft=("spec",))

OTHER = [
    ("sandbox", "not described here yet."),
    ("learncpp-pdfs", "not described here yet."),
]


# The To do list (todo.html): what is to be done, not yet a project or a PR.
# Each item: title, and optionally what it is about (one sentence) and
# done=True once it is.
TODO = [
    {"title": "Research ways to eliminate static casting"},
    {"title": "Polish the apps' pkg install",
     "about": "sqterm and sqIDE: it works, but could use some polish."},
]
