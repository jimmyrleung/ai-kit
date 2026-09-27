# Engineering change contract

Apply during analysis, design, decomposition, implementation, and review, including fixes.
Read applicable repository instructions and inspect nearby production code, tests,
documentation, and CI before choosing an approach. Cite suitable existing utilities,
helpers, fixtures, and test locations; follow the repository's established conventions.

Add or extend meaningful tests for changed behavior. Extend a suitable existing test file;
create a new one only when repository conventions require it or no existing file is a
suitable home. Record that reason in the implementation/task plan. Preserve coverage on
either path: fewer files is not a quality target.

Keep the patch focused on the requested outcome. Avoid duplicated helpers, speculative
abstractions, unrelated cleanup, and unnecessary complexity. Aim for a coherent, mergeable
change that fits its repository and satisfies relevant checks. Reviewers challenge these
problems with repository evidence; they do not request cosmetic rewrites outside scope.
