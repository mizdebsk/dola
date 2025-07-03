[![build status](https://img.shields.io/github/actions/workflow/status/mizdebsk/dola/ci.yml?branch=master)](https://github.com/mizdebsk/dola/actions/workflows/ci.yml?query=branch%3Amaster)
[![License](https://img.shields.io/github/license/mizdebsk/dola.svg?label=License)](https://www.apache.org/licenses/LICENSE-2.0)
[![Maven Central version](https://img.shields.io/maven-central/v/io.kojan/dola-dbs.svg?label=Maven%20Central)](https://search.maven.org/artifact/io.kojan/dola-dbs)
[![Javadoc](https://javadoc.io/badge2/io.kojan/dola-dbs/javadoc.svg)](https://javadoc.io/doc/io.kojan/dola-dbs)

Dola
====

Declarative system for Java RPM packaging

Dola is a modern, declarative system for RPM packaging of Maven-based
Java projects.  It enables package maintainers to entirely avoid
writing `%prep`, `%build`, or `%install` scriptlets in RPM spec files.
Instead, all build configuration is expressed using BuildOption tags
(introduced in RPM 4.20), resulting in cleaner, more maintainable spec
files.

Traditional RPM packaging for Java has relied heavily on scripting
within spec files.  Tools like XMvn and Javapackages-Tools
significantly improved this by automating and standardizing Maven
builds and artifact packaging.  However, even these tools still
require some executable configuration, often embedded in %prep through
macro calls.

Dola takes this a step further by introducing a fully declarative,
data-driven approach to spec file creation.  While it leverages XMvn
internally, Dola adds a higher-level abstraction that allows most Java
build processes to be defined purely through data, eliminating the
need for scriptlets.  This enhances consistency, readability, and
automation across Java packaging workflows, and lays the groundwork
for future tooling to automatically process spec files, since
declarative configurations are easier to analyze and transform.


Features
--------

- **No Explicit Build Scriptlets**  
  Dola automatically generates `%prep`, `%build`, and `%install` sections.
  Custom scriptlets can still be added when needed.

- **Dynamic BuildRequires Generation**  
  Analyzes Maven projects and translates build-time dependencies into
  RPM `BuildRequires`.

- **Interoperability**  
  Packages built with Dola remain fully compatible with traditional
  Java packages that use `javapackages-tools`.

- **Automation-Friendly**  
  The declarative nature of Dola specs enables automated refactoring,
  validation, and bulk transformations across package sets.

- **Conversion to Imperative Form**  
  Declarative specs can be automatically converted to traditional,
  imperative RPM spec files compatible with systems using RPM < 4.20.


Syntax
------

For description of the syntax for declarative spec files, see
the [Reference Manual](MANUAL.md).


Copying
-------

Dola is free software. You can redistribute and/or modify it under the
terms of Apache License Version 2.0.

Dola was written by Mikolaj Izdebski.
