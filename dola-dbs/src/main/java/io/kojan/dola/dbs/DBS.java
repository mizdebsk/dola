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
package io.kojan.dola.dbs;

import static io.kojan.dola.rpm.RPM.rpmExpand;

import io.kojan.dola.build.DeclarativeBuild;
import io.kojan.dola.build.parser.BuildOptionParser;
import io.kojan.dola.imperator.Imperator;
import java.util.stream.Collectors;

public class DBS {
    private static Imperator imperator;

    private static final boolean debugEnabled = "1".equals(rpmExpand("%{dola_debug}"));

    private static void debug(Object... msg) {
        if (debugEnabled) {
            System.err.print("DOLA: ");
            for (Object s : msg) {
                System.err.print(s.toString());
            }
            System.err.println();
        }
    }

    public static String conf() throws Exception {
        String rpmName = rpmExpand("%{name}");
        StringBuilder dslBuilder = new StringBuilder();
        int n = Integer.parseInt(rpmExpand("%#"));
        for (int i = 2; i <= n; i++) {
            dslBuilder.append(rpmExpand("%" + i)).append('\n');
        }
        BuildOptionParser parser = new BuildOptionParser(rpmName, dslBuilder.toString());
        DeclarativeBuild ctx = parser.parse();

        boolean withBootstrap = !rpmExpand("%{with bootstrap}").equals("0");

        imperator = new Imperator(ctx, withBootstrap);

        return "";
    }

    public static String buildrequires() throws Exception {
        String out = imperator.buildrequires().stream().collect(Collectors.joining("\n"));
        debug("Output buildrequires script:\n", out);
        return out;
    }

    public static String build() throws Exception {
        String out = imperator.build().stream().collect(Collectors.joining("\n"));
        debug("Output build script:\n", out);
        return out;
    }

    public static String install() throws Exception {
        String out = imperator.install().stream().collect(Collectors.joining("\n"));
        debug("Output install script:\n", out);
        return out;
    }
}
