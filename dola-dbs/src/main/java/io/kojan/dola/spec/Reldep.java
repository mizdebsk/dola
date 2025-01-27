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

public class Reldep {
    private final String name;
    private final String sense;
    private final String evr;
    private final boolean rich;

    private Reldep(String name, String sense, String evr, boolean rich) {
        this.name = name;
        this.sense = sense;
        this.evr = evr;
        this.rich = rich;
    }

    public static Reldep simple(String name) {
        return new Reldep(name, null, null, false);
    }

    public static Reldep versioned(String name, String sense, String evr) {
        return new Reldep(name, sense, evr, false);
    }

    public static Reldep rich(String expr) {
        return new Reldep(expr, null, null, true);
    }

    public String getName() {
        return name;
    }

    public String getSense() {
        return sense;
    }

    public String getEVR() {
        return evr;
    }

    public boolean isRich() {
        return rich;
    }

    @Override
    public String toString() {
        if (rich) {
            return "ReldepRich[" + name + "]";
        }
        if (sense == null) {
            return "Reldep[" + name + "]";
        }
        return "Reldep[" + name + " " + sense + " " + evr + "]";
    }

    public String getRpmStr() {
        return sense == null ? name : name + " " + sense + " " + evr;
    }
}
