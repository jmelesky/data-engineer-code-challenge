## Git process

I don't have nearly as many opinions about git as I do about data and SQL. I understand the pros and cons of using `merge` or `rebase` (cluttering with merge commits vs keeping the branch history, etc), but don't have a strong stance on which should be preferred.

The most important thing, as far as I'm concerned, is having a predictable policy about it. That could be "always `merge`" or "always `rebase`" or "always `merge` unless the branch is (big/long-lived/busy) enough that we `rebase` instead". I'm happy to work with any of them.

