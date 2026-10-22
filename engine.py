"""
engine.py
---------
AnonymizerEngine: 텍스트를 받아 결과(치환된 코드, 매핑표)만 돌려주는 순수 로직 모듈.
GUI나 로깅을 전혀 모름 (화면/저장 방식이 바뀌어도 이 파일은 그대로 재사용 가능).
"""

import re


class AnonymizerEngine:

    RESERVED_WORDS = {
        "and", "array", "as", "asm", "begin", "case", "class", "const", "constructor",
        "destructor", "dispinterface", "div", "do", "downto", "else", "end", "except",
        "exports", "file", "finalization", "finally", "for", "function", "goto", "if",
        "implementation", "in", "inherited", "initialization", "inline", "interface",
        "is", "label", "library", "mod", "nil", "not", "object", "of", "or", "out",
        "packed", "procedure", "program", "property", "raise", "record", "repeat",
        "resourcestring", "set", "shl", "shr", "string", "then", "threadvar", "to",
        "try", "type", "unit", "until", "uses", "var", "while", "with", "xor",
        "private", "protected", "public", "published", "automated", "virtual",
        "dynamic", "override", "overload", "message", "reintroduce", "static",
        "abstract", "sealed", "final", "deprecated", "platform", "experimental",
        "unsafe", "varargs", "cdecl", "pascal", "register", "safecall", "stdcall",
        "read", "write", "default", "nodefault", "stored", "implements", "index",
        "add", "remove", "name", "readonly", "writeonly", "dispid", "helper",
        "strict", "operator", "reference", "unused",
    }

    COMMON_LIBRARY_NAMES = {
        "integer", "int64", "cardinal", "byte", "word", "shortint", "smallint",
        "longint", "longword", "single", "double", "extended", "currency", "comp",
        "boolean", "true", "false", "char", "widechar", "ansichar", "pchar",
        "pwidechar", "pansichar", "string", "ansistring", "widestring",
        "unicodestring", "shortstring", "variant", "olevariant", "tdatetime",
        "pointer", "tobject", "texception", "exception", "tclass", "tguid",
        "result", "self", "message",
        "writeln", "write", "readln", "read", "inc", "dec", "length", "setlength",
        "copy", "delete", "insert", "pos", "trim", "trimleft", "trimright",
        "uppercase", "lowercase", "stringreplace", "format", "inttostr", "strtoint",
        "strtointdef", "floattostr", "strtofloat", "strtofloatdef", "datetostr",
        "strtodate", "datetimetostr", "formatdatetime", "now", "date", "time",
        "inttohex", "hextostr", "booleantostr", "vartype", "varastype",
        "assigned", "freeandnil", "tryfinally", "exit", "break", "continue",
        "showmessage", "messagedlg", "application", "sleep", "getmem", "freemem",
        "new", "dispose", "raiselasterror", "exceptionclass",
        "tstringlist", "tstrings", "tlist", "tobjectlist", "tdictionary",
        "tstream", "tfilestream", "tmemorystream", "tstringstream",
        "tcomponent", "tpersistent", "tinterfacedobject",
        "tform", "tbutton", "tedit", "tmemo", "tlabel", "tpanel", "tcombobox",
        "tcheckbox", "tradiobutton", "tapplication", "tscreen", "sender",
        "tnotifyevent", "tcloseaction", "tcloseevent",
        "tfdconnection", "tfdquery", "tfdmemtable", "tfdlocalsql", "tfdtransaction",
        "tdatasource", "tdataset", "tfield", "tfielddef", "fieldbyname", "asstring",
        "asinteger", "asfloat", "asboolean", "asdatetime", "asvariant", "aswidestring",
        "params", "paramvalues", "sql", "active", "connected", "connection",
        "driverid", "server", "database", "open", "close", "post", "append", "edit",
        "cancel", "next", "prior", "first", "last", "eof", "bof", "recordcount",
        "fieldcount", "fields", "locate", "applyupdates", "commit", "rollback",
        "starttransaction", "fetchoptions", "updateoptions", "resourceoptions",
        "tcxgriddbtableview", "tcxgrid", "tcxgridlevel", "tcxgriddbcolumn",
        "datacontroller", "values", "appendrecord", "posteditingdata",
        "tcxtextedit", "tcxbuttonedit", "tcxlookupcombobox",
        "tjsonobject", "tjsonarray", "tjsonvalue", "tjsonstring", "tjsonnumber",
        "parsejsonvalue", "tojson", "asobject", "asarray",
        "tregex", "tmatch", "tmatchcollection", "ismatch",
        "charinset", "trycharinset",
        "activesheetastable", "cells", "isempty", "columns", "rows", "count",
        "usedrange", "worksheets", "workbooks", "activesheet", "sheets",
    }

    IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
    STRING_LITERAL_RE = re.compile(r"'(?:[^']|'')*'")
    LINE_COMMENT_RE = re.compile(r"//.*")
    BRACE_COMMENT_RE = re.compile(r"\{(?!\$)[^}]*\}", re.DOTALL)
    PAREN_COMMENT_RE = re.compile(r"\(\*(?:(?!\*\)).)*\*\)", re.DOTALL)

    def anonymize(self, code: str, extra_whitelist=None):
        """
        code: 익명화할 원본 코드 조각
        extra_whitelist: 가리지 않을 이름 목록 (list[str])
        반환: (치환된 코드: str, 매핑표: dict[placeholder, original])
        """
        whitelist = {w.strip().lower() for w in (extra_whitelist or []) if w.strip()}
        mapping = {}
        reverse_map = {}
        counters = {"id": 0, "str": 0}

        def repl_string(m):
            original = m.group(0)
            key = original.lower()
            if key not in reverse_map:
                counters["str"] += 1
                placeholder = f"'STR{counters['str']}'"
                reverse_map[key] = placeholder
                mapping[placeholder] = original
            return reverse_map[key]

        code = self.STRING_LITERAL_RE.sub(repl_string, code)
        code = self.BRACE_COMMENT_RE.sub("{ (주석 제거됨) }", code)
        code = self.PAREN_COMMENT_RE.sub("(* (주석 제거됨) *)", code)
        code = self.LINE_COMMENT_RE.sub("// (주석 제거됨)", code)

        def repl_ident(m):
            word = m.group(0)
            low = word.lower()
            if low in self.RESERVED_WORDS or low in self.COMMON_LIBRARY_NAMES or low in whitelist:
                return word
            if re.fullmatch(r"str\d+", low):
                return word
            if low not in reverse_map:
                counters["id"] += 1
                placeholder = f"ID{counters['id']}"
                reverse_map[low] = placeholder
                mapping[placeholder] = word
            return reverse_map[low]

        code = self.IDENT_RE.sub(repl_ident, code)
        return code, mapping