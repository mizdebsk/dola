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

class FormattingLexer extends Lexer {
    private int indentLevel;
    private boolean whiteSpaceBefore;
    private boolean newLineBefore;
    private final StringBuilder buffer = new StringBuilder();
    private String currentToken;

    public FormattingLexer(String str) {
        super(str);
    }

    private void token(String nextToken) {
        if (currentToken != null) {
            boolean newLineAfter;
            if (currentToken.equals("{")) {
                indentLevel++;
                newLineAfter = true;
            } else if (currentToken.equals("}")) {
                indentLevel--;
                newLineBefore = true;
                newLineAfter = true;
            } else {
                newLineAfter = false;
            }
            if (whiteSpaceBefore) {
                if (newLineBefore) {
                    buffer.append('\n').append("  ".repeat(indentLevel));
                } else {
                    buffer.append(' ');
                }
            }
            buffer.append(currentToken);
            newLineBefore = newLineAfter;
            whiteSpaceBefore = true;
        }
        currentToken = nextToken;
    }

    @Override
    public Lexer next() {
        super.next();
        token(str.substring(lexBeg, lexEnd));
        return this;
    }

    @Override
    public boolean isBlockEnd() {
        newLineBefore = true;
        return super.isBlockEnd();
    }

    @Override
    public boolean isEndOfInput() {
        newLineBefore = true;
        return super.isEndOfInput();
    }

    public String asString() {
        return buffer.toString();
    }
}
