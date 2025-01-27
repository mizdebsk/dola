/*-
 * Copyright (c) 2024 Red Hat, Inc.
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
package io.kojan.dola.spec;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Spec {
    private final List<MacroDef> macros;
    private final Pkg mainPkg;
    private final List<Pkg> subpkgs;
    private final Map<ScriptType, Script> scripts;
    private final List<String> changelog;

    private Spec(
            List<MacroDef> macros,
            Pkg mainPkg,
            List<Pkg> subpkgs,
            Map<ScriptType, Script> scripts,
            List<String> changelog) {
        this.macros = macros;
        this.mainPkg = mainPkg;
        this.subpkgs = subpkgs;
        this.scripts = scripts;
        this.changelog = changelog;
    }

    public static Spec produce(
            List<MacroDef> macros,
            Pkg mainPkg,
            List<Pkg> subpkgs,
            Map<ScriptType, Script> scripts,
            List<String> changelog) {
        for (Pkg pkg : subpkgs) {
            if (pkg.getFiles() == null) {
                throw new IllegalStateException("Incomplete files for pkg " + pkg.getName());
            }
        }
        return new Spec(
                List.copyOf(macros),
                mainPkg,
                List.copyOf(subpkgs),
                Map.copyOf(scripts),
                List.copyOf(changelog));
    }

    public List<MacroDef> getMacros() {
        return macros;
    }

    public Pkg getMainPkg() {
        return mainPkg;
    }

    public List<Pkg> getSubpkgs() {
        return subpkgs;
    }

    public Map<ScriptType, Script> getScripts() {
        return scripts;
    }

    public List<String> getChangelog() {
        return changelog;
    }

    public Spec withMainPkg(Pkg newMainPkg) {
        return new Spec(macros, newMainPkg, subpkgs, scripts, changelog);
    }

    public Spec withScript(Script script) {
        Map<ScriptType, Script> newScripts = new LinkedHashMap<>(scripts);
        newScripts.put(script.getType(), script);
        return new Spec(macros, mainPkg, subpkgs, newScripts, changelog);
    }
}
