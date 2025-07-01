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
package io.kojan.dola.build.parser;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import org.junit.jupiter.api.Test;

class LexerTest {

    @Test
    void empty() throws Exception {
        Lexer lexer = new Lexer("");
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void whitespaceOnly() throws Exception {
        Lexer lexer = new Lexer(" \n");
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void keywordToken() throws Exception {
        Lexer lexer = new Lexer("print");
        assertThat(lexer.next().isKeyword("print")).isTrue();
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void literalToken() throws Exception {
        Lexer lexer = new Lexer("\"hello\"");
        assertThat(lexer.next().expectLiteral()).isEqualTo("hello");
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void beginToken() throws Exception {
        Lexer lexer = new Lexer("{");
        lexer.next().expectBlockBegin();
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void endToken() throws Exception {
        Lexer lexer = new Lexer("}");
        assertThat(lexer.next().isBlockEnd()).isTrue();
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void multipleTokens() throws Exception {
        Lexer lexer = new Lexer("print \"value\" { }");
        assertThat(lexer.next().isKeyword("print")).isTrue();
        assertThat(lexer.next().expectLiteral()).isEqualTo("value");
        lexer.next().expectBlockBegin();
        assertThat(lexer.next().isBlockEnd()).isTrue();
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void whitespaceNormalization() throws Exception {
        Lexer lexer = new Lexer("  print\n \"hello\"  ");
        assertThat(lexer.next().isKeyword("print")).isTrue();
        assertThat(lexer.next().expectLiteral()).isEqualTo("hello");
        assertThat(lexer.next().isEndOfInput()).isTrue();
    }

    @Test
    void tabRejection() throws Exception {
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(() -> new Lexer("  print\n\t\"hello\"  "))
                .withMessageContaining("TAB characters are not allowed");
    }

    @Test
    void unterminatedStringLiteral() throws Exception {
        Lexer lexer = new Lexer("\"unterminated");
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(lexer::next)
                .withMessageContaining("unterminated string literal");
    }

    @Test
    void illegalCharacter() throws Exception {
        Lexer lexer = new Lexer("$");
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(lexer::next)
                .withMessageContaining("illegal character");
    }

    @Test
    void expectLiteralFailure() throws Exception {
        Lexer lexer = new Lexer("print");
        lexer.next();
        assertThatExceptionOfType(BuildOptionParseException.class)
                .isThrownBy(lexer::expectLiteral)
                .withMessageContaining("expected literal");
    }
}
