#!/bin/sh
# Expected verdicts on the reference submissions: "page" then "verified in review".
cd "$(dirname "$0")"
status=0
t() {  # t PROBLEM FILE EXPECTED
  got=$(python3 -I obb.py check "$1" "$2" | grep -o 'IMPROVES\|does not improve' | tr '\n' ',')
  if [ "$got" = "$3" ]; then echo "ok    $1 $(basename $2): $got"; else echo "FAIL  $1 $(basename $2): $got (expected $3)"; status=1; fi
}
echo '{"values": [1, 1, 1, 1]}' > certs/flat4_1a.json
t 1a-upper certs/flat4_1a.json "does not improve,does not improve,"
t 1c-lower certs/kos_1c.json "does not improve,does not improve,"
t 1c-lower certs/vid_1c_v3.json "IMPROVES,does not improve,"
t 1d-upper certs/huiihao_1d.json "does not improve,does not improve,"
t 68a-lower certs/pin_68a.json "does not improve,does not improve,"
t 68a-lower certs/vid_68a_044605.json "IMPROVES,does not improve,"
exit $status
