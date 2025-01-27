/*-
 * Copyright (c) 2025 Red Hat, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.kojan.dola.spec.parser;

import io.kojan.dola.spec.BuildOpt;
import io.kojan.dola.spec.BuildSys;
import io.kojan.dola.spec.CondDep;
import io.kojan.dola.spec.Condition;
import io.kojan.dola.spec.MacroDef;
import io.kojan.dola.spec.Pkg;
import io.kojan.dola.spec.Reldep;
import io.kojan.dola.spec.Script;
import io.kojan.dola.spec.ScriptType;
import io.kojan.dola.spec.Spec;
import io.kojan.dola.spec.Tag;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

// Declarative Specfile Parser
public class DSP {

    // Input buffer to parse, holds the entire spec file
    private final String buf;
    // Current parser position
    private int pos;
    // Position of End-Of-File
    private final int eof;

    public DSP(String s) {
        buf = s;
        pos = 0;
        eof = s.length();
    }

    private void initParser() throws SpecParseException {
        // Reject TABs upfront so that we don't need to care about them in the parser code
        if (buf.indexOf('\t') >= 0) {
            pos = buf.indexOf('\t');
            parseError("TAB characters are not allowed, replace them with spaces");
        }
        parseComment();
    }

    private List<String> comment;
    private int commentBegPos;
    private int commentEndPos;

    private List<String> popComment() throws SpecParseException {
        if (comment == null) {
            parseError("comment stack underflow");
        }
        List<String> list = comment;
        comment = null;
        return list;
    }

    private void popCommentIgnore() throws SpecParseException {
        List<String> comment = popComment();
        if (!comment.isEmpty()) {
            pos = commentBegPos;
            parseError("Comment is not allowed at this location");
        }
    }

    private void parseComment() throws SpecParseException {
        if (comment == null) {
            commentBegPos = -1;
            List<String> list = new ArrayList<>();
            while (pos < eof) {
                if (buf.charAt(pos) == '\n') {
                    pos++;
                } else if (buf.charAt(pos) == '#') {
                    if (commentBegPos < 0) {
                        commentBegPos = pos;
                    }
                    pos++;
                    if (pos < eof && buf.charAt(pos) == ' ') {
                        pos++;
                    }
                    int beg = pos;
                    while (pos < eof && buf.charAt(pos) != '\n') {
                        pos++;
                    }
                    list.add(buf.substring(beg, pos));
                } else {
                    break;
                }
            }
            comment = list;
            commentEndPos = pos;
            if (commentBegPos < 0) {
                commentBegPos = pos;
            }
        } else if (pos != commentEndPos) {
            parseError("comment stack overflow");
        }
    }

    private Error parseError(String msg) throws SpecParseException {
        // Count lines
        int lineStart = 0;
        int lineNumber = 1;
        for (int i = 0; i < pos; i++) {
            if (buf.charAt(i) == '\n') {
                lineStart = i + 1;
                lineNumber++;
            }
        }
        int lineEnd = eof;
        for (int i = pos; i < eof; i++) {
            if (buf.charAt(i) == '\n') {
                lineEnd = i;
                break;
            }
        }
        String line = buf.substring(lineStart, lineEnd);
        String banner = "~".repeat(Math.max(10, lineEnd - lineStart));
        StringBuilder sb = new StringBuilder();
        sb.append(msg);
        sb.append("\nat line ")
                .append(lineNumber)
                .append(":\n")
                .append(banner)
                .append("\n")
                .append(line)
                .append("\n")
                .append(banner)
                .append("\n");
        if (pos - lineStart >= 10) {
            sb.append("  here ");
            sb.append("-".repeat(pos - lineStart - 7));
            sb.append("^");
        } else {
            sb.append(" ".repeat(pos - lineStart));
            sb.append("^--- here");
        }
        System.err.println(sb);
        throw new SpecParseException(sb.toString());
    }

    private boolean has(String s) {
        if (buf.substring(pos).startsWith(s)) {
            pos += s.length();
            return true;
        }
        return false;
    }

    private boolean hasTag(String tag) {
        if (has(tag + ":")) {
            skipSpaceTab();
            return true;
        }
        return false;
    }

    private void require(String s) throws SpecParseException {
        if (!has(s)) {
            throw parseError("Expected \"" + s + "\"");
        }
    }

    private void requireNL() throws SpecParseException {
        if (!has("\n")) {
            throw parseError("Expected new line");
        }
    }

    private void skipSpaceTab() {
        while (pos < eof && buf.charAt(pos) == ' ') {
            pos++;
        }
    }

    private String parseUntil(Character... chars) throws SpecParseException {
        Set<Character> cs = Set.of(chars);
        int beg = pos;
        while (pos < eof && !cs.contains(buf.charAt(pos))) {
            pos++;
        }
        if (pos == beg) {
            parseError("Expected at least one character from expected set");
        }
        return buf.substring(beg, pos);
    }

    private String parseWord() throws SpecParseException {
        int beg = pos;
        while (pos < eof && buf.charAt(pos) != ' ' && buf.charAt(pos) != '\n') {
            pos++;
        }
        if (pos == beg) {
            parseError("Expected at least one non-whitespace character");
        }
        return buf.substring(beg, pos);
    }

    private int parseInt() throws SpecParseException {
        if (pos == eof) {
            throw parseError("Unexpected EOF");
        }
        if (!Character.isDigit(buf.charAt(pos))) {
            throw parseError("Expected a digit");
        }
        int beg = pos;
        while (pos < eof && Character.isDigit(buf.charAt(pos))) {
            pos++;
        }
        return Integer.parseInt(buf.substring(beg, pos));
    }

    private String parseUntilEol() throws SpecParseException {
        String s = parseUntilEolNC();
        parseComment();
        return s;
    }

    private String parseUntilEolNC() throws SpecParseException {
        int beg = pos;
        while (pos < eof && buf.charAt(pos) != '\n') {
            pos++;
        }
        if (pos == beg) {
            parseError("Expected at least one character before EOL");
        }
        String s = buf.substring(beg, pos);
        if (pos < eof) {
            pos++;
        }
        return s;
    }

    // The entire RPM spec file.
    public Spec parseSpec() throws SpecParseException {
        initParser();
        List<MacroDef> macroDefs = parseMacroDefs();
        Pkg mainPkg = parseMainPkg();
        List<Pkg> subpackages = parseSubpackages(mainPkg);
        Map<ScriptType, Script> scripts = parseScripts();
        mainPkg = parseMainFiles(mainPkg);
        parseSubFiles(mainPkg, subpackages);
        List<String> changelog = parseChangelog();
        parseEof();
        return Spec.produce(macroDefs, mainPkg, subpackages, scripts, changelog);
    }

    // Zero or more macro definitions, possibly surrounded by if/else
    // conditionals.
    private List<MacroDef> parseMacroDefs() throws SpecParseException {
        List<MacroDef> list = new ArrayList<>();
        while (true) {
            MacroDef macroDef = tryParseMacroDef();
            if (macroDef != null) {
                list.add(macroDef);
            } else if (has("%if ")) {
                List<String> c0 = popComment();
                String cond = parseUntilEol();
                list.add(MacroDef.of("%%if %s".formatted(cond), c0));
                list.addAll(parseMacroDefs());
                if (has("%else\n")) {
                    List<String> c = popComment();
                    list.add(MacroDef.of("%else", c));
                    parseComment();
                    list.addAll(parseMacroDefs());
                }
                require("%endif");
                requireNL();
                List<String> c = popComment();
                list.add(MacroDef.of("%endif", c));
                parseComment();
            } else {
                return list;
            }
        }
    }

    // A single macro definition (global, define, bcond*)
    private MacroDef tryParseMacroDef() throws SpecParseException {
        if (has("%define ")) {
            List<String> c = popComment();
            String key = parseWord();
            skipSpaceTab();
            String val = parseUntilEol();
            return MacroDef.of("%%define %s %s".formatted(key, val), c);
        }
        if (has("%global ")) {
            List<String> c = popComment();
            String key = parseWord();
            skipSpaceTab();
            String val = parseUntilEol();
            return MacroDef.of("%%global %s %s".formatted(key, val), c);
        }
        if (has("%bcond ")) {
            List<String> c = popComment();
            String key = parseWord();
            skipSpaceTab();
            String val = parseUntilEol();
            return MacroDef.of("%%bcond %s %s".formatted(key, val), c);
        }
        if (has("%bcond_with ")) {
            List<String> c = popComment();
            String key = parseUntilEol();
            return MacroDef.of("%%bcond_with %s".formatted(key), c);
        }
        if (has("%bcond_without ")) {
            List<String> c = popComment();
            String key = parseUntilEol();
            return MacroDef.of("%%bcond_with %s".formatted(key), c);
        }
        return null;
    }

    // Main package declaration, including global tags, dependencies and
    // main package description.
    private Pkg parseMainPkg() throws SpecParseException {
        List<Tag> tags = parseGlobalTags();
        List<CondDep> deps = parseDeps();
        BuildSys buildSystem = tryParseBuildSystem();
        List<String> description = parseDescriptionMain();
        String pkgName = tags.getFirst().getValue();
        return Pkg.of(pkgName)
                .withTags(tags)
                .withDeps(deps)
                .withBuildSys(buildSystem)
                .withDescription(description);
    }

    // One or more global tags.
    private List<Tag> parseGlobalTags() throws SpecParseException {
        List<Tag> list = new ArrayList<>();
        list.add(parseGlobalPackageName());
        while (true) {
            Tag globalTag = tryParseGlobalTag();
            if (globalTag != null) {
                list.add(globalTag);
            } else {
                return list;
            }
        }
    }

    // An RPM tag with String value that can appear in global context.
    private Tag parseGlobalPackageName() throws SpecParseException {
        if (!hasTag("Name")) {
            throw parseError("Expected Name tag");
        }
        List<String> c = popComment();
        String val = parseUntilEol();
        return Tag.of(1, "Name", val, c);
    }

    // An RPM tag with String value that can appear in global context.
    private Tag tryParseGlobalTag() throws SpecParseException {
        if (hasTag("URL")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(7, "URL", val, c);
        }
        if (hasTag("VCS")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(8, "VCS", val, c);
        }
        if (hasTag("ExclusiveArch")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(10, "ExclusiveArch", val, c);
        }
        if (hasTag("Source")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(999, "Source", val, c);
        }
        if (has("Source")) {
            List<String> c = popComment();
            int n = parseInt();
            require(":");
            skipSpaceTab();
            String val = parseUntilEol();
            return Tag.of(1000 + n, "Source" + n, val, c);
        }
        if (hasTag("Patch")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(9999, "Patch", val, c);
        }
        return tryParsePkgTag();
    }

    // An RPM tag with String value that can be applied to both main
    // package and subpackages.
    private Tag tryParsePkgTag() throws SpecParseException {
        if (hasTag("Epoch")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(2, "Epoch", val, c);
        }
        if (hasTag("Version")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(3, "Version", val, c);
        }
        if (hasTag("Release")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(4, "Release", val, c);
        }
        if (hasTag("Summary")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(5, "Summary", val, c);
        }
        if (hasTag("License")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(6, "License", val, c);
        }
        if (hasTag("BuildArch")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return Tag.of(9, "BuildArch", val, c);
        }
        return null;
    }

    // Zero or more dependencies, possibly surrounded by if/else
    // conditionals.
    private List<CondDep> parseDeps() throws SpecParseException {
        List<CondDep> list = new ArrayList<>();
        while (true) {
            if (has("%if ")) {
                List<String> c = popComment();
                String condExpr = parseUntilEol();
                Condition cond = Condition.of(condExpr);
                List<CondDep> deps = parseDeps();
                for (CondDep dep : deps) {
                    list.add(dep.setCondition(cond).addComment(c));
                }
                if (has("%else\n")) {
                    List<String> c2 = popComment();
                    parseComment();
                    Condition cond2 = cond.negate();
                    List<CondDep> deps2 = parseDeps();
                    for (CondDep dep : deps2) {
                        list.add(dep.setCondition(cond2).addComment(c2));
                    }
                }
                require("%endif");
                requireNL();
                popCommentIgnore();
                parseComment();
            } else {
                CondDep dep = tryParseDep();
                if (dep != null) {
                    list.add(dep);
                } else {
                    return list;
                }
            }
        }
    }

    // A single dependency, eg. Requires.
    private CondDep tryParseDep() throws SpecParseException {
        if (hasTag("BuildRequires")) {
            List<String> c = popComment();
            Reldep reldep = parseReldep();
            return CondDep.ofBuildRequires(reldep, c);
        }
        if (hasTag("Requires")) {
            List<String> c = popComment();
            Reldep reldep = parseReldep();
            return CondDep.ofRequires(reldep, c);
        }
        if (hasTag("Provides")) {
            List<String> c = popComment();
            Reldep reldep = parseReldep();
            return CondDep.ofProvides(reldep, c);
        }
        if (hasTag("Obsoletes")) {
            List<String> c = popComment();
            Reldep reldep = parseReldep();
            return CondDep.ofObsoletes(reldep, c);
        }
        if (hasTag("Suggests")) {
            List<String> c = popComment();
            Reldep reldep = parseReldep();
            return CondDep.ofSuggests(reldep, c);
        }
        return null;
    }

    // A dependency string, aka "reldep". Can be a simple dependency
    // without version like "foo", a simple dependency with version like
    // "foo > 1.0" or a boolean (rich) dependency like "(foo if bar)".
    private Reldep parseReldep() throws SpecParseException {
        if (has("(")) {
            String val = "(" + parseUntilEol();
            return Reldep.rich(val);
        }
        String id = parseUntil('<', '>', '=', ' ', '\n');
        skipSpaceTab();
        if (has("\n")) {
            parseComment();
            return Reldep.simple(id);
        }
        if (has("<")) {
            skipSpaceTab();
            String ver = parseUntilEol();
            return Reldep.versioned(id, "<", ver);
        }
        if (has("<=")) {
            skipSpaceTab();
            String ver = parseUntilEol();
            return Reldep.versioned(id, "<=", ver);
        }
        if (has("=")) {
            skipSpaceTab();
            String ver = parseUntilEol();
            return Reldep.versioned(id, "=", ver);
        }
        if (has(">=")) {
            skipSpaceTab();
            String ver = parseUntilEol();
            return Reldep.versioned(id, ">=", ver);
        }
        if (has(">")) {
            skipSpaceTab();
            String ver = parseUntilEol();
            return Reldep.versioned(id, ">", ver);
        }
        throw parseError("Expect relation operator < <= = >= = or EOL");
    }

    // Optional build system declaration followed by build options.
    private BuildSys tryParseBuildSystem() throws SpecParseException {
        if (hasTag("BuildSystem")) {
            List<String> c = popComment();
            skipSpaceTab();
            require("maven");
            requireNL();
            parseComment();
            List<BuildOpt> buildOpts = parseBuildOptions();
            return BuildSys.of(buildOpts, c);
        }
        return null;
    }

    // Zero or more build options.
    private List<BuildOpt> parseBuildOptions() throws SpecParseException {
        List<BuildOpt> list = new ArrayList<>();
        while (true) {
            BuildOpt opt = tryParseBuildOption();
            if (opt != null) {
                list.add(opt);
            } else {
                return list;
            }
        }
    }

    // A single build option.
    private BuildOpt tryParseBuildOption() throws SpecParseException {
        if (hasTag("BuildOption")) {
            List<String> c = popComment();
            String val = parseUntilEol();
            return BuildOpt.of(val, c);
        }
        return null;
    }

    private List<String> parseDescriptionMain() throws SpecParseException {
        require("%description");
        requireNL();
        popCommentIgnore();
        return parseSection();
    }

    private List<String> parseSection() throws SpecParseException {
        if (comment != null) {
            throw new IllegalStateException();
        }

        Pattern p =
                Pattern.compile(
                        "\n*(#.*\n)*($|%(if|else|endif|global|define|bcond|bcond_with|bcond_without|build|changelog|clean|conf|description|files|install|package|post|posttrans|postun|pre|prep|pretrans|preun|trigger[a-z]+|verifyscript|transfiletrigger[a-z]+|filetrigger[a-z]+)( .*)?\n)");
        Matcher m = p.matcher(buf.substring(pos));
        if (!m.find()) {
            parseError("Unable to determine section boundary");
        }
        int beg = pos;
        pos += m.start();
        String ss = buf.substring(beg, pos);
        parseComment();
        if (ss.isEmpty()) {
            return List.of();
        } else {
            return List.of(ss);
        }
    }

    // Zero or more subpackages.
    private List<Pkg> parseSubpackages(Pkg mainPkg) throws SpecParseException {
        List<Pkg> list = new ArrayList<>();
        while (true) {
            Pkg pkg = tryParseSubpackage(mainPkg);
            if (pkg != null) {
                list.add(pkg);
            } else {
                return list;
            }
        }
    }

    // An optional subpackage declaration, %package followed by corresponding %description.
    private Pkg tryParseSubpackage(Pkg mainPkg) throws SpecParseException {
        if (has("%package -n")) {
            popCommentIgnore();
            skipSpaceTab();
            String name = parseUntilEol();
            List<Tag> tags = parseSubpackageTags();
            List<CondDep> deps = parseDeps();
            popCommentIgnore();
            require("%description -n");
            skipSpaceTab();
            String name2 = parseUntilEolNC();
            if (!name2.equals(name2)) {
                throw parseError(
                        "Package name of %description does not match that of the preceding %package");
            }
            List<String> desc = parseSection();
            return Pkg.of(name).withTags(tags).withDeps(deps).withDescription(desc);
        }
        if (has("%package ")) {
            popCommentIgnore();
            skipSpaceTab();
            String name = parseUntilEol();
            List<Tag> tags = parseSubpackageTags();
            List<CondDep> deps = parseDeps();
            popCommentIgnore();
            require("%description ");
            skipSpaceTab();
            String name2 = parseUntilEolNC();
            if (!name2.equals(name2)) {
                throw parseError(
                        "Package name of %description does not match that of the preceding %package");
            }
            List<String> desc = parseSection();
            return Pkg.ofPrefixed(mainPkg.getName(), name)
                    .withTags(tags)
                    .withDeps(deps)
                    .withDescription(desc);
        }
        return null;
    }

    // Zero or more package tags.
    private List<Tag> parseSubpackageTags() throws SpecParseException {
        List<Tag> list = new ArrayList<>();
        while (true) {
            Tag globalTag = tryParsePkgTag();
            if (globalTag != null) {
                list.add(globalTag);
            } else {
                return list;
            }
        }
    }

    // Zero or more build scripts.
    private Map<ScriptType, Script> parseScripts() throws SpecParseException {
        Map<ScriptType, Script> map = new LinkedHashMap<>();
        while (true) {
            Script script = tryParseScript();
            if (script != null) {
                if (map.containsKey(script.getType())) {
                    parseError("Duplicate script " + script.getName());
                }
                map.put(script.getType(), script);
            } else {
                return map;
            }
        }
    }

    // An optional build script.
    private Script tryParseScript() throws SpecParseException {
        for (ScriptType type : ScriptType.values()) {
            if (has("%" + type.getName() + "\n")) {
                popCommentIgnore();
                List<String> script = parseSection();
                return Script.of(type, script);
            }
        }
        return null;
    }

    // Zero or one %files declarations for the main package.
    private Pkg parseMainFiles(Pkg mainPkg) throws SpecParseException {
        if (has("%files\n")) {
            popCommentIgnore();
            List<String> files = parseSection();
            mainPkg = mainPkg.withFiles(files);
        } else if (has("%files -f")) {
            popCommentIgnore();
            List<String> mfiles = new ArrayList<>();
            do {
                skipSpaceTab();
                String val = parseWord();
                mfiles.add(val);
                skipSpaceTab();
            } while (has("-f"));
            requireNL();
            List<String> files = parseSection();
            mainPkg = mainPkg.withMFiles(mfiles).withFiles(files);
        }
        return mainPkg;
    }

    // Zero or more %files sections for subpackages.
    private void parseSubFiles(Pkg mainPkg, List<Pkg> subpackages) throws SpecParseException {
        while (has("%files ")) {
            popCommentIgnore();
            skipSpaceTab();
            boolean prefixed = !has("-n");
            skipSpaceTab();
            String name = parseWord();
            String fullName = prefixed ? mainPkg.getName() + "-" + name : name;
            int i;
            for (i = 0; i < subpackages.size(); i++) {
                if (subpackages.get(i).getName().equals(fullName)) {
                    break;
                }
            }
            if (i >= subpackages.size()) {
                throw parseError("Subpackage " + fullName + " was not declared");
            }
            List<String> mfiles = new ArrayList<>();
            skipSpaceTab();
            while (has("-f")) {
                skipSpaceTab();
                String val = parseWord();
                mfiles.add(val);
                skipSpaceTab();
            }
            requireNL();
            List<String> files = parseSection();
            subpackages.set(i, subpackages.get(i).withMFiles(mfiles).withFiles(files));
        }
    }

    // The %changelog section.
    private List<String> parseChangelog() throws SpecParseException {
        require("%changelog");
        requireNL();
        popCommentIgnore();
        List<String> lines = parseSection();
        return lines;
    }

    // End of the spec file.
    private void parseEof() throws SpecParseException {
        if (pos != eof) {
            throw parseError("Expected EOF");
        }
        popCommentIgnore();
    }
}
