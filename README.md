# Decepticon

Rudderstack's transformer (https://github.com/rudderlabs/rudder-transformer)
didn't work on my M1 machine (neither locally nor on Docker, where it hangs
without responding to requests) so I wrote this fake transformer, which responds
with something useful enough to get rudderstack-server running locally.

Run with

```
python3 decepticon.py
```

and it will listen in the default port for the transformer (`9090`) with the same
message as it got. It won't do any fancy stuff with the types of the columns, and
just set everything as a string.

This was the minimum required to test against Glue the changes in [this PR](https://github.com/rudderlabs/rudder-server/pull/1571),
so YMMV if you want to test some other destination (due to schema compatibility).
