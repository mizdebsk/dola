--
-- Copyright (c) 2023-2025 Red Hat, Inc.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--

local lujavrite = require "lujavrite"

local libjvm = rpm.expand("%{__dola_libjvm}")
local classpath = rpm.expand("%{__dola_classpath}")
local classworlds_conf = rpm.expand("%{_javaconfdir}/dola/classworlds")

-- Initialize JVM
if not lujavrite.initialized() then
    local bsx_debug = rpm.expand("%{dola_bsx_debug}")
    if bsx_debug == "1" then
        io.stderr:write("╔══════════════════════════════════════════════════╗\n")
        io.stderr:write("║ ┌─╮   ╷                                          ║\n")
        io.stderr:write("║ │ │╭─╮│ ╭─╮    Initializing startup sequence...  ║\n")
        io.stderr:write("║ └─╯╰─╯╰╴╰─┴╯                                     ║\n")
        io.stderr:write("╚══════════════════════════════════════════════════╝\n")
    end
    lujavrite.init(
       libjvm,
       "-Djava.class.path=" .. classpath,
       "-Ddola.bsx.debug=" .. bsx_debug,
       "--enable-native-access=ALL-UNNAMED"
    )
    lujavrite.call(
       "io/kojan/dola/bsx/BSX",
       "configureClassWorld",
       "(Ljava/lang/String;)Ljava/lang/String;",
       classworlds_conf
    )
end

local function call0(realm, class, method)
   return lujavrite.call(
      "io/kojan/dola/bsx/BSX",
      "call0S",
      "(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;",
      realm,
      class,
      method
   )
end

local function call1(realm, class, method, arg)
   return lujavrite.call(
      "io/kojan/dola/bsx/BSX",
      "call1S",
      "(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;",
      realm,
      class,
      method,
      arg
   )
end

-- Exported module functions
return {
   call0 = call0,
   call1 = call1
}
