/* TaskSource Grammar
 * ==================
 * PEG grammar for a task source in restricted markdown.
 * Example:
 * ----------------------------
 * # four-steps-forward
 * - category: repeat
 *
 * ## Setting
 *
 * ```
 * |g |g |g |g |g |
 * |b |b |b |b |b |
 * |b |b |b |b |b |
 * |b |b |b |b |b |
 * |b |b |bS|b |b |
 * ```
 * - energy: 2
 * - length: 2
 *
 * ## Solution
 *
 * ```
 * repeat 4:
 *     fly()
 * ```
 * ----------------------------
 */

Start
  = taskId:Headline __ options:Option* __ setting:Setting __ solution:Solution
  { return Object.assign(
      {
        taskId: taskId,
        setting: setting,
        solution: solution
      },
      ...options
    );
  }


Headline
  = "# " _ taskId:Value _ EOL
  { return taskId }


Option
  = __ "-" _ key:Value ":" _ value:Value _ EOL
  { return {[key]: value} }


Setting
  = "## Setting" __ fields:Code __ options:Option*
  { return Object.assign(
      {
        fields: fields
      },
      ...options
    );
  }


Solution
  = "## Solution" __ solution:Code
  { return solution }


Code
  = _ "```" [^\n\r]* EOL
    code:$([^`]*)
    "```" _ EOL
  { return code }


Value
  = Integer
  / Text


Integer
  = digits:[0-9]+ & WS
  // require a whitespace to follow to distinguish texts starting with some digits
  { return parseInt(digits.join(""), 10); }


Text
  = $([a-zA-Z0-9_-]+)

_ "inline whitespace"
  = [ \t]*


__ "whitespace"
  = WS*


WS "single whitespace"
  = [ \t\n\r]


EOL "end of line or file"
  = "\r\n"
  / "\n"
  / "\r"
  / !.
