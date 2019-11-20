#!/bin/bash

if [ "$1" == "" ] || [ "$2" == "" ] ; then
  echo "Usage $0 <title> <logo svg>"
  exit
fi
if [ ! -f $2 ] ; then
  echo "File $2 does not exist"
  exit
fi
file -i $2 | grep " image/svg+xml;" >/dev/null
if [ $? -ne 0 ] ; then
  echo "$2 is not a SVG file"
  exit
fi

TITLE=$1
SVG=$(cat $2 | base64 -w 0)

sed -i "s/PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMCIgaGVpZ2h0PSIzOSIgdmlld0JveD0iMCAwIDMwIDM5Ij4gIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+ICAgIDxwb2x5Z29uIGZpbGw9IiNGMDRFOTgiIHBvaW50cz0iMCAwIDAgMzQuNTQ3IDI5LjkyMiAuMDIiLz4gICAgPHBhdGggZmlsbD0iIzM0Mzc0MSIgZD0iTTAsMTQuNCBMMCwzNC41NDY4IEwxNC4yODcyLDE4LjA2MTIgQzEwLjA0MTYsMTUuNzM4IDUuMTgwNCwxNC40IDAsMTQuNCIvPiAgICA8cGF0aCBmaWxsPSIjMDBCRkIzIiBkPSJNMTcuMzc0MiwxOS45OTY4IEwyLjcyMSwzNi45MDQ4IEwxLjQzMzQsMzguMzg5MiBMMjkuMjYzOCwzOC4zODkyIEMyNy43NjE0LDMwLjgzODggMjMuNDA0MiwyNC4zMjY0IDE3LjM3NDIsMTkuOTk2OCIvPiAgPC9nPjwvc3ZnPg==/$SVG/" /usr/share/kibana/src/legacy/ui/ui_render/views/ui_app.pug
sed -i "s/PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMCIgaGVpZ2h0PSIzOSIgdmlld0JveD0iMCAwIDMwIDM5Ij4gIDxnIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+ICAgIDxwb2x5Z29uIGZpbGw9IiNGMDRFOTgiIHBvaW50cz0iMCAwIDAgMzQuNTQ3IDI5LjkyMiAuMDIiLz4gICAgPHBhdGggZmlsbD0iIzM0Mzc0MSIgZD0iTTAsMTQuNCBMMCwzNC41NDY4IEwxNC4yODcyLDE4LjA2MTIgQzEwLjA0MTYsMTUuNzM4IDUuMTgwNCwxNC40IDAsMTQuNCIvPiAgICA8cGF0aCBmaWxsPSIjMDBCRkIzIiBkPSJNMTcuMzc0MiwxOS45OTY4IEwyLjcyMSwzNi45MDQ4IEwxLjQzMzQsMzguMzg5MiBMMjkuMjYzOCwzOC4zODkyIEMyNy43NjE0LDMwLjgzODggMjMuNDA0MiwyNC4zMjY0IDE3LjM3NDIsMTkuOTk2OCIvPiAgPC9nPjwvc3ZnPg==/$SVG/" /usr/share/kibana/src/legacy/ui/ui_render/views/chrome.pug

sed -i "s/Loading Kibana/Loading $TITLE/" /usr/share/kibana/src/legacy/ui/ui_render/views/ui_app.pug
sed -i "s/title Kibana/title $TITLE/" /usr/share/kibana/src/legacy/ui/ui_render/views/chrome.pug
