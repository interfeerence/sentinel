#!/bin/bash
set -evx

mkdir ~/.exilium

# safety check
if [ ! -f ~/.exilium/.exilium.conf ]; then
  cp share/exilium.conf.example ~/.exilium/exilium.conf
fi
