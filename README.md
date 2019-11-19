## kibana_object_cmd

List, import and export Kibana objects.

`-list` lists all objects

  You need to specify an object type (like dashboard, visualization or index-pattern) using `-t`

`-export` exports all objects

  You need to specify an object type (like dashboard, visualization or index-pattern) using `-t`
  You can optionally specify an object id using `-id`

  If you want to retrieve all dependant objects use `-all`

  The output will be ndjson to stdout. If you want to have clean json instead, then use `-json`.
