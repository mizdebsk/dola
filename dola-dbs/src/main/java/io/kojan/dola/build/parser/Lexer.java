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

import java.util.ArrayDeque;
import java.util.Deque;

class Lexer {
    // For parsing
    final String str; // raw input string with sentinel character appended
    final int eoi; // end of input index (points to sentinel)
    int lexBeg; // begin index (inclusive) of current token
    int lexEnd; // end index (exclusive) of current token
    int pos; // begin index of next token

    // For making canonical form on the fly
    private final StringBuilder canonicalForm = new StringBuilder();
    private String currentToken; // last token that has not yet been added to cannonicalForm
    private int indentLevel;
    private boolean whiteSpaceBefore; // white space is expected before current token
    private boolean newLineBefore; // new line is expected before current token

    // For error reporting
    private Deque<String> path = new ArrayDeque<>();
    private Deque<Integer> pathForks = new ArrayDeque<>();

    public Lexer(String str) throws BuildOptionParseException {
        this.str = str + '$';
        eoi = str.length();
        // Reject TABs upfront so that we don't need to care about them in the parser code
        if (str.indexOf('\t') >= 0) {
            pos = str.indexOf('\t');
            throw new BuildOptionParseException(
                    "Lexical error: TAB characters are not allowed, replace them with spaces");
        }
        lookahead();
    }

    private BuildOptionParseException lexicalError(String msg) throws BuildOptionParseException {

        appendTokenToCanonicalForm();
        int errPos = pos;

        // Append normalized whitespace, if any.
        pos = lexEnd;
        lookahead();
        if (!canonicalForm.isEmpty() && pos != lexEnd) {
            canonicalForm.append(" ");
        }

        // Then append text that was partially matched as the next token, up to character at which
        // the lexical error occurred.
        canonicalForm.append(str.substring(pos, errPos));

        // For lexical errors, error location is always the last character.
        int errLoc = canonicalForm.length() - 1;

        throw errorCommon(msg, canonicalForm.toString(), errLoc);
    }

    public BuildOptionParseException error(String msg) throws BuildOptionParseException {

        appendTokenToCanonicalForm();
        // For syntax errors, error location is the first character of the last lexeme.
        int lexLen = lexEnd - lexBeg;
        int errLoc = canonicalForm.length() - lexLen;

        throw errorCommon(msg, canonicalForm.toString(), errLoc);
    }

    // number of context lines to show in code snippets, plus one
    final int nLinesInContext = 5;

    private BuildOptionParseException errorCommon(String msg, String canonStr, int errLoc)
            throws BuildOptionParseException {

        // Figure out where (at which indexes) the last 5 lines of code start.
        int[] lineStart = new int[nLinesInContext];
        int lineNum = 0;
        int curLineBeg = 0;
        for (int i = 0; i < canonStr.length(); ) {
            if (canonStr.charAt(i++) == '\n') {
                curLineBeg = i;
                lineStart[lineNum] = i;
                lineNum = (lineNum + 1) % nLinesInContext;
            }
        }
        int snipBeg = lineStart[lineNum];

        // Figure out width of the snippet (max line length in the snippet)
        int snipMaxLen = canonStr.length() - curLineBeg;
        for (int i = 0; i < nLinesInContext; i++) {
            int lineEnd = lineStart[(i + 1) % nLinesInContext];
            snipMaxLen = Math.max(snipMaxLen, Math.max(lineEnd - lineStart[i] - 1, 0));
        }
        String banner = "~".repeat(Math.min(72, Math.max(10, snipMaxLen)));

        // First, message describing nature of the error.
        StringBuilder sb = new StringBuilder();
        sb.append(msg).append("\n");

        // Then path from AST root to the error location.
        sb.append("at BuildOption:");
        for (String node : path) {
            sb.append(" ").append(node);
        }
        sb.append("\n");

        // Next code snippet.
        sb.append(banner).append("\n");
        if (snipBeg > 0) {
            sb.append("[...]\n");
        }
        sb.append(canonStr.substring(snipBeg)).append("\n");
        sb.append(banner).append("\n");

        // Finally, arrow pointing to the error location in the snippet.
        int arrowOffset = errLoc - curLineBeg;
        if (arrowOffset >= 10) {
            sb.append("  here ").append("-".repeat(arrowOffset - 7)).append("^");
        } else {
            sb.append(" ".repeat(arrowOffset)).append("^--- here");
        }

        throw new BuildOptionParseException(sb.toString());
    }

    // Advance to the next lookahead token
    private void lookahead() {
        int ch;
        while ((ch = str.charAt(pos)) == ' ' || ch == '\n') {
            pos++;
        }
    }

    private void appendTokenToCanonicalForm() {
        if (currentToken != null) {
            boolean newLineAfter;
            if (currentToken.charAt(0) == '{') {
                indentLevel++;
                newLineAfter = true;
            } else if (currentToken.charAt(0) == '}') {
                indentLevel--;
                newLineBefore = true;
                newLineAfter = true;
            } else {
                newLineAfter = false;
            }
            if (whiteSpaceBefore) {
                if (newLineBefore) {
                    canonicalForm.append('\n').append("    ".repeat(Math.max(indentLevel, 0)));
                } else {
                    canonicalForm.append(' ');
                }
            }
            canonicalForm.append(currentToken);
            newLineBefore = newLineAfter;
            whiteSpaceBefore = true;
        }
    }

    // Discard current token, advance to next token.
    public Lexer next() throws BuildOptionParseException {
        lexBeg = pos;
        if (pos == eoi) {
            lexEnd = pos;
            appendTokenToCanonicalForm();
            currentToken = null;
            return this;
        }
        int ch = str.charAt(pos++);
        if (ch == '"') {
            while (str.charAt(pos++) != '"') {
                if (pos > eoi) {
                    lexicalError("Lexical error: unterminated string literal");
                }
            }
        } else if (ch >= 'a' && ch <= 'z') {
            while (((ch = str.charAt(pos)) >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z')) {
                pos++;
            }
        } else if (ch != '{' && ch != '}') {
            lexicalError("Lexical error: illegal character");
        }
        lexEnd = pos;
        appendTokenToCanonicalForm();
        currentToken = str.substring(lexBeg, lexEnd);
        lookahead();
        return this;
    }

    // Is current token a specific keyword?
    public boolean isKeyword(String kw) {
        if (kw.length() == lexEnd - lexBeg && str.regionMatches(lexBeg, kw, 0, lexEnd - lexBeg)) {
            path.addLast(currentToken);
            return true;
        }
        return false;
    }

    // Only literal string is allowed at this location, return its value.
    public String expectLiteral() throws BuildOptionParseException {
        if (str.charAt(lexBeg) != '"') {
            error("Syntax error: expected literal (quoted string)");
        }
        path.addLast(currentToken);
        return str.substring(lexBeg + 1, lexEnd - 1);
    }

    private void markPathFork() {
        pathForks.addLast(path.size());
    }

    // Only block beginning is allowed at this location.
    public void expectBlockBegin() throws BuildOptionParseException {
        if (str.charAt(lexBeg) != '{') {
            error("Syntax error: expected opening brace '{'");
        }
        path.addLast("->");
        markPathFork();
    }

    private boolean pathUnwind(boolean reset) {
        int mark = pathForks.size() > 0 ? pathForks.removeLast() : 0;
        boolean dots = false;
        while (path.size() > mark) {
            path.removeLast();
            dots = true;
        }
        if (dots && (path.isEmpty() || !path.peekLast().equals("[...]"))) {
            path.addLast("[...]");
        }
        if (!reset) {
            markPathFork();
        }
        return reset;
    }

    // Is current token a block end '}'?
    public boolean isBlockEnd() {
        newLineBefore = true;
        return pathUnwind(str.charAt(lexBeg) == '}');
    }

    // Is end of input reached, meaning that all tokens were exhausted?
    public boolean isEndOfInput() {
        newLineBefore = true;
        return pathUnwind(lexBeg == eoi);
    }

    // Is the *next* token (aka lookahead token) a string literal?
    public boolean lookaheadIsLiteral() {
        return str.charAt(pos) == '"';
    }

    // Return parsed code as formatted string, in canonical form.
    public String asString() {
        return canonicalForm.toString();
    }
}
