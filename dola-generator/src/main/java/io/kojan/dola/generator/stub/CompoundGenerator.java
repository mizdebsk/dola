/*-
 * Copyright (c) 2023-2024 Red Hat, Inc.
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
package io.kojan.dola.generator.stub;

import io.kojan.dola.generator.BuildContext;
import io.kojan.dola.generator.Generator;
import io.kojan.dola.generator.GeneratorFactory;
import io.kojan.dola.generator.logging.Logger;
import java.nio.file.Path;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

class CompoundGenerator {
    private final BuildContext buildContext;
    private final List<FilteredGenerator> generators;
    private final boolean multifile;
    private DepsCollector collector;

    private Generator loadGenerator(String cn) {
        try {
            ClassLoader cl = Thread.currentThread().getContextClassLoader();
            GeneratorFactory factory =
                    (GeneratorFactory) cl.loadClass(cn).getDeclaredConstructor().newInstance();
            return factory.createGenerator(buildContext);
        } catch (ReflectiveOperationException e) {
            throw new RuntimeException(e);
        }
    }

    public CompoundGenerator(BuildContext buildContext) {
        this.buildContext = buildContext;
        if (!buildContext.eval("%{?__dolagen_debug}").isEmpty()) {
            Logger.enableDebug();
        }
        multifile = buildContext.eval("%{?__dolagen_protocol}").equals("multifile");
        Set<String> provCns =
                Set.of(buildContext.eval("%{?__dolagen_provides_generators}").split("\\s+"));
        Set<String> reqCns =
                Set.of(buildContext.eval("%{?__dolagen_requires_generators}").split("\\s+"));
        Set<String> allCns = new LinkedHashSet<>();
        allCns.addAll(provCns);
        allCns.addAll(reqCns);
        generators =
                allCns.stream()
                        .filter(cn -> !cn.isEmpty())
                        .map(
                                cn ->
                                        new FilteredGenerator(
                                                loadGenerator(cn),
                                                provCns.contains(cn),
                                                reqCns.contains(cn)))
                        .collect(Collectors.toUnmodifiableList());
        if (generators.isEmpty()) {
            buildContext.eval("%{warn:dola-generator: no generators were specified}");
        }
    }

    public String runGenerator(String kind) {
        if (collector == null) {
            Path buildRoot = Path.of(buildContext.eval("%{buildroot}"));
            collector = new DepsCollector(buildRoot);
            Logger.startLogging();
            for (Generator generator : generators) {
                Logger.startNewSection();
                Logger.debug(
                        "Running "
                                + generator
                                + " ("
                                + generator.getClass().getCanonicalName()
                                + ")");
                generator.generate(collector);
            }
            Logger.finishLogging();
        }
        StringBuilder sb = new StringBuilder();
        int n = Integer.parseInt(buildContext.eval("%#"));
        for (int i = 1; i <= n; i++) {
            Path filePath = Path.of(buildContext.eval("%" + i));
            Set<String> deps = collector.getDeps(filePath, kind);
            if (multifile && !deps.isEmpty()) {
                sb.append(';').append(filePath).append('\n');
            }
            for (String dep : deps) {
                sb.append(dep).append('\n');
            }
        }
        return sb.toString();
    }
}
