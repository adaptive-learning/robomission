/* RoboCode PEG Grammar
 * ====================
 * Assumes preprocessed program with marked line numbers and indentation to
 * avoid context-sensitiveness. For example:
 * ```
 * 1| fly()
 * 2| while color() == 'b':
 * >
 * 3| left()
 * 4| right()
 * <
 * 5| fly()
 * ```
 */

Start
  = body:(Sequence / EmptyProgram)
    { return { head: "start", body: body } }

EmptyProgram
  = EOL { return [] }


/* ----- Statements ----- */

Sequence
  = EmptySequence
  / StatementBlock+

EmptySequence
  = SOL "pass" EOL
    { return [] }

StatementBlock
  = lineNumber:SOL s:Statement EOL
    { return { statement: s, location: lineNumber } }


Statement
  = CompoundStatement
  / SimpleStatement


SimpleStatement
  = action:FunctionCall
    { return { head: action } }


CompoundStatement
  = IfStatement
  / WhileStatement
  / RepeatStatement


RepeatStatement
  = "repeat" __ n:Integer ":" b:Body
    { return { head: "repeat", count: n, body: b } }


WhileStatement
  = "while" __ t:Test ":" b:Body
    { return { head: "while", test: t, body: b } }


IfStatement
  = "if" __ t:Test ":" b:Body e:OrelseStatementBlock?
    { return { head: "if", test: t, body: b, orelse: e} }


OrelseStatementBlock
  = EOL lineNumber:SOL s:OrelseStatement
    { return { statement: s, location: lineNumber } }


OrelseStatement
  = ElifStatement
  / ElseStatement


ElifStatement
  = "elif" __ t:Test ":" b:Body e:OrelseStatementBlock?
    { return { head: "elif", test: t, body: b, orelse: e} }


ElseStatement
  = "else:" b:Body
    { return { head: "else", body: b } }


Body
  = EOL INDENT s:Sequence DEDENT
    { return s }


/* ----- Expressions ----- */

Test
  = CompoundTest
  / SimpleTest

CompoundTest
  = left:SimpleTest __ op:BinLogicOp __ right:SimpleTest
    { return { head: op, left: left, right: right } }

SimpleTest
  = sensor:FunctionCall _ op:RelOp _ value:Value
    { return { head: sensor, comparator:op, value: value } }

FunctionCall
  = functionName:Identifier "()"
    { return functionName; }

BinLogicOp
  = "and" / "or"

RelOp
  = "==" / ">=" / "<=" / "!=" / ">" / "<"

Value
  = Integer / String

Integer
  = digits:[0-9]+
    { return parseInt(digits.join(""), 10); }

String
  = "'" value:$([^']*) "'"
    { return value; }


// ----- Lexical Grammar -----

Identifier
  = $([a-zA-Z_][a-zA-Z0-9_]*)

_ "optional spaces"
  = [ \t]*

__ "mandatory spaces"
  = [ \t]+

INDENT
  = ">" EOL

DEDENT
  = "<"

SOL "start of line"
  = lineNumber:Integer "| "
    { return lineNumber }

EOL "end of line or file"
  = "\r\n"
  / "\n"
  / "\r"
  / !.
