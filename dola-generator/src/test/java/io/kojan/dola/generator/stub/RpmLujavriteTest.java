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
package io.kojan.dola.generator.stub;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.kojan.dola.generator.BuildContext;
import java.io.InputStream;
import java.lang.ProcessBuilder.Redirect;
import java.nio.file.Path;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class RpmLujavriteStub {
    public static String stubMain(String arg) {
        System.err.println("Hello from Java!");
        System.out.println("foo");
        BuildContext context = new RpmBuildContext();
        System.out.println(context.eval("%[7+5]"));
        System.out.println(context.eval("%(expr 7 + 5)"));
        return "7 plus " + arg + " equals " + context.eval("%[7+" + arg + "]");
    }
}

public class RpmLujavriteTest {

    @BeforeAll
    public static void setUpClass() {
        System.load("/usr/lib64/lua/5.4/lujavrite.so");
    }

    @Test
    public void testCallThrougtRpmLujavrite() throws Exception {
        Path javaExecutable = Path.of(ProcessHandle.current().info().command().get());
        assertTrue(javaExecutable.endsWith(Path.of("bin/java")));
        Path javaHome = javaExecutable.getParent().getParent();
        Path libjvmPath = javaHome.resolve("lib/server/libjvm.so");
        String classPath = System.getProperty("java.class.path");
        StringBuilder macro = new StringBuilder();
        macro.append("%{lua:\n");
        macro.append("local lujavrite = require \"lujavrite\"\n");
        macro.append("local libjvm = \"").append(libjvmPath).append("\"\n");
        macro.append("local classpath = \"").append(classPath).append("\"\n");
        macro.append(
                "lujavrite.init(libjvm, \"-Djava.class.path=\" .. classpath, \"--enable-native-access=ALL-UNNAMED\")\n");
        macro.append(
                "print(lujavrite.call(\"io/kojan/dola/generator/stub/RpmLujavriteStub\", \"stubMain\", \"(Ljava/lang/String;)Ljava/lang/String;\", \"35\"))\n");
        macro.append("}");
        ProcessBuilder pb = new ProcessBuilder("rpm", "-E", macro.toString());
        pb.redirectError(Redirect.INHERIT);
        Process p = pb.start();
        assertEquals(0, p.waitFor());
        String out;
        try (InputStream is = p.getInputStream()) {
            out = new String(is.readAllBytes());
        }
        assertEquals("foo\n12\n12\n7 plus 35 equals 42\n", out);
    }
}
