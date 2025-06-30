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
package io.kojan.dola.generator.transformer;

import static org.assertj.core.api.Assertions.assertThat;

import io.kojan.dola.generator.BuildContext;
import java.util.jar.Manifest;
import org.easymock.EasyMock;
import org.junit.jupiter.api.Test;

class ManifestInjectorTest {
    @Test
    void manifestInjector() {
        BuildContext bc = EasyMock.createStrictMock(BuildContext.class);
        EasyMock.expect(bc.eval("%{NAME}")).andReturn("nn");
        EasyMock.expect(bc.eval("%{?EPOCH}")).andReturn("ee");
        EasyMock.expect(bc.eval("%{VERSION}")).andReturn("vv");
        EasyMock.expect(bc.eval("%{RELEASE}")).andReturn("rr");
        EasyMock.replay(bc);
        Manifest mf = new Manifest();
        mf.getMainAttributes().putValue("Foo", "xx");
        ManifestInjector manifestInjector = new ManifestInjector(bc);
        manifestInjector.transform(mf);
        assertThat(mf.getMainAttributes().getValue("Foo")).isEqualTo("xx");
        assertThat(mf.getMainAttributes().getValue("Rpm-Name")).isEqualTo("nn");
        assertThat(mf.getMainAttributes().getValue("Rpm-Epoch")).isEqualTo("ee");
        assertThat(mf.getMainAttributes().getValue("Rpm-Version")).isEqualTo("vv");
        assertThat(mf.getMainAttributes().getValue("Rpm-Release")).isEqualTo("rr");
        EasyMock.verify(bc);
    }
}
