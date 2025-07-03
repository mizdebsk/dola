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
package io.kojan.dola.imperator;

import io.kojan.dola.build.Alias;
import io.kojan.dola.build.DeclarativeBuild;
import io.kojan.dola.build.PackagingOption;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import org.fedoraproject.xmvn.artifact.Artifact;
import org.fedoraproject.xmvn.config.BuildSettings;
import org.fedoraproject.xmvn.config.Configuration;
import org.fedoraproject.xmvn.config.PackagingRule;

public class Imperator {
    private final DeclarativeBuild ctx;
    // Are we in bootstrap mode: true=yes, false=no, null=unknown
    private final Boolean withBootstrap;

    public Imperator(DeclarativeBuild ctx, Boolean withBootstrap) {
        this.ctx = ctx;
        this.withBootstrap = withBootstrap;
    }

    private String glob2re(String glob) {
        if (glob.isEmpty()) {
            return ".*";
        }
        return glob.replaceAll("\\*", ".*").replaceAll("\\?", ".");
    }

    private String glob2re(Artifact glob) {
        return glob2re(glob.getGroupId()) + ":" + glob2re(glob.getArtifactId());
    }

    private List<String> getGleanerArgs() {
        List<String> args = new ArrayList<>();
        args.add("-Ddola.gleaner.outputFile=/dev/fd/4");
        int i = 0;
        for (Artifact br : ctx.getFilteredBuildReqs()) {
            String id = String.format("%03d", i++);
            String key = "dola.gleaner.filter." + id;
            String val = glob2re(br);
            args.add("-D" + key + "=" + val);
        }
        int j = 0;
        for (var entry : ctx.getBuildReqVersions().entrySet()) {
            Artifact br = entry.getKey();
            String version = entry.getValue();
            String id = String.format("%03d", j++);
            String key = "dola.gleaner.version." + id;
            String val = glob2re(br) + "=" + version;
            args.add("-D" + key + "=" + val);
        }
        return args;
    }

    private List<String> getTransformerArgs() {
        List<String> args = new ArrayList<>();
        int i = 0;
        for (var t : ctx.getTransformOptions()) {
            String id = String.format("%03d", i++);
            String key = "dola.transformer.insn." + id + "." + t.getOpcode();
            String val = t.getArgument() + "@" + t.getSelector();
            args.add("-D" + key + "=" + val);
        }
        return args;
    }

    private List<String> getTestArgs() {
        List<String> args = new ArrayList<>();
        args.add("-Dsurefire.reportFormat=plain");
        if (!ctx.getTestExcludes().isEmpty()) {
            String exclArg =
                    ctx.getTestExcludes().stream()
                            .map(s -> "!" + s.replace('@', '#'))
                            .collect(Collectors.joining(","));
            args.add("-Dsurefire.failIfNoSpecifiedTests=false");
            args.add("-Dtest='" + exclArg + "'");
        }
        return args;
    }

    public List<String> buildrequires() throws Exception {
        List<String> lines = new ArrayList<>();

        Configuration conf = new Configuration();
        if (ctx.isSkipTests()) {
            conf.setBuildSettings(new BuildSettings());
            conf.getBuildSettings().setSkipTests(true);
        }

        if (ctx.isSingletonPackaging()) {
            PackagingRule rule1 = new PackagingRule();
            org.fedoraproject.xmvn.config.Artifact glob1 =
                    new org.fedoraproject.xmvn.config.Artifact();
            glob1.setClassifier("*?");
            rule1.setArtifactGlob(glob1);
            rule1.setTargetPackage("__noinstall");
            rule1.setOptional(true);
            conf.addArtifactManagement(rule1);

            PackagingRule rule2 = new PackagingRule();
            org.fedoraproject.xmvn.config.Artifact glob2 =
                    new org.fedoraproject.xmvn.config.Artifact();
            glob2.setArtifactId("{*}");
            rule2.setArtifactGlob(glob2);
            rule2.setTargetPackage("@1");
            conf.addArtifactManagement(rule2);
        }

        for (PackagingOption po : ctx.getPackagingOptions()) {
            PackagingRule rule = new PackagingRule();
            org.fedoraproject.xmvn.config.Artifact glob =
                    new org.fedoraproject.xmvn.config.Artifact();
            glob.setGroupId(po.getGroupIdGlob());
            glob.setArtifactId(po.getArtifactIdGlob());
            glob.setExtension(po.getExtensionGlob());
            glob.setClassifier(po.getClassifierGlob());
            glob.setVersion(po.getVersionGlob());
            rule.setArtifactGlob(glob);
            rule.setTargetPackage(po.getTargetPackage());
            rule.setVersions(po.getCompatVersions());
            rule.setFiles(po.getFiles());
            for (Alias alias : po.getAliases()) {
                org.fedoraproject.xmvn.config.Artifact aa =
                        new org.fedoraproject.xmvn.config.Artifact();
                aa.setGroupId(alias.getGroupId());
                aa.setArtifactId(alias.getArtifactId());
                aa.setExtension(alias.getExtension());
                aa.setClassifier(alias.getClassifier());
                rule.addAlias(aa);
            }
            conf.addArtifactManagement(rule);
        }

        if (conf.getBuildSettings() != null || !conf.getArtifactManagement().isEmpty()) {
            lines.add("# Write out XMvn configuration before calling XMvn for the first time.");
            Path confPath = Path.of(".xmvn/config.d/dola.xml");
            lines.add("mkdir -p " + confPath.getParent());
            lines.add("cat <<__DOLA_EOF__ >" + confPath);
            lines.add(conf.toXML().replaceAll("<\\?xml[^?]*\\?>", "").strip());
            lines.add("__DOLA_EOF__");
            lines.add("");
        }

        if (withBootstrap == null || !withBootstrap || !ctx.usesJavapackagesBootstrap()) {
            if (withBootstrap == null && ctx.usesJavapackagesBootstrap()) {
                lines.add("%if %{without bootstrap}");
            }

            if (!ctx.getExtraBuildReqs().isEmpty() || ctx.getXmvnToolchain() != null) {
                lines.add("# Explicit static build-dependencies.");
                lines.add("cat <<__DOLA_EOF__");
                if (ctx.getXmvnToolchain() != null) {
                    lines.add("xmvn5-toolchain-" + ctx.getXmvnToolchain());
                }
                for (Artifact br : ctx.getExtraBuildReqs()) {
                    lines.add(formatDep(br));
                }
                lines.add("__DOLA_EOF__");
                lines.add("");
            }

            List<String> args = new ArrayList<>();
            args.add("xmvn5");
            args.add("--show-version");
            args.add("--batch-mode");
            args.add("--offline");
            String extCp = "/usr/share/java/dola-gleaner/dola-gleaner.jar";
            if (!ctx.getTransformOptions().isEmpty()) {
                extCp += ":/usr/share/java/dola-transformer/dola-transformer.jar";
            }
            args.add("-Dmaven.ext.class.path=" + extCp);
            args.addAll(getGleanerArgs());
            args.addAll(getTransformerArgs());
            args.addAll(getTestArgs());
            args.addAll(ctx.getMavenOptions());

            if (ctx.isSkipTests()) {
                args.add("-Dmaven.test.skip=true");
            }

            String mavenGoal = ctx.isSkipTests() ? "package" : "verify";
            args.add(mavenGoal);

            args.add("4>&1 >&2");

            lines.add("# Call XMvn with Dola Gleaner extension.  With this extension enabled,");
            lines.add("# Maven build is not actually executed, but the extension analyzes");
            lines.add("# the project and prints out missing artifacts that need to be installed.");
            lines.add(args.stream().collect(Collectors.joining(" \\\n    ")));

            if (ctx.usesJavapackagesBootstrap() && withBootstrap == null) {
                lines.add("%endif");
            }
        }

        return lines;
    }

    public List<String> build() throws Exception {
        List<String> args = new ArrayList<>();
        args.add("xmvn5");
        args.add("--show-version");
        args.add("--batch-mode");
        args.add("--offline");
        if (!ctx.getTransformOptions().isEmpty()) {
            String extCp = "/usr/share/java/dola-transformer/dola-transformer.jar";
            args.add("-Dmaven.ext.class.path=" + extCp);
            args.addAll(getTransformerArgs());
        }
        args.addAll(getTestArgs());
        args.addAll(ctx.getMavenOptions());

        if (ctx.isSkipTests()) {
            args.add("-Dmaven.test.skip=true");
        }

        String mavenGoal = ctx.isSkipTests() ? "package" : "verify";
        args.add(mavenGoal);
        args.add("org.fedoraproject.xmvn:xmvn-mojo:5.0.0:install");

        List<String> lines = new ArrayList<>();
        lines.add("# Run the actual Maven build, executing all build plugins and so on.");
        lines.add(args.stream().collect(Collectors.joining(" \\\n    ")));

        return lines;
    }

    public List<String> install() throws Exception {
        List<String> args = new ArrayList<>();
        args.add("xmvn5-install");
        args.add("-R " + ".xmvn-reactor");
        args.add("-n " + ctx.getBaseName());
        args.add("-d $RPM_BUILD_ROOT");

        List<String> lines = new ArrayList<>();
        lines.add("# Run XMvn Installer to populate buildroot.");
        lines.add(args.stream().collect(Collectors.joining(" \\\n    ")));

        return lines;
    }

    private String formatDep(Artifact art) {
        boolean cusExt = !art.getExtension().equals(Artifact.DEFAULT_EXTENSION);
        boolean cusCla = !art.getClassifier().equals("");
        boolean cusVer = !art.getVersion().equals(Artifact.DEFAULT_VERSION);
        StringBuilder sb = new StringBuilder();
        sb.append("mvn(");
        sb.append(art.getGroupId());
        sb.append(":");
        sb.append(art.getArtifactId());
        if (cusCla || cusExt) {
            sb.append(":");
        }
        if (cusExt) {
            sb.append(art.getExtension());
        }
        if (cusCla) {
            sb.append(":");
            sb.append(art.getClassifier());
        }
        if (cusCla || cusExt || cusVer) {
            sb.append(":");
        }
        if (cusVer) {
            sb.append(art.getVersion());
        }
        sb.append(")");
        return sb.toString();
    }
}
