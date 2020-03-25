#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'


# Output Formatting Facilities ----
FMT_CODE="\e[0;31;47m"  # red on grey
FMT_BKG_PURP="\e[0;30;45m"  # normal black on purple
FMT_OFF="\e[0m"
title()   { echo -e "\n${FMT_BKG_PURP}\n
                          $*                            \n${FMT_OFF}"; }
code()    { echo -e "\n${FMT_CODE}\$ $*${FMT_OFF}"; }


# PARAMS ----
FN_TEST=$(basename $0)
FN_TARGET=${FN_TEST#test-}
FN_TARGET=${FN_TARGET%.sh}


# preconditions ----
if [ ! -f ${FN_TARGET} ]; then fatal "No file ${FN_TARGET}"; fi


# MAIN ----
title "Testing ${FN_TARGET}"

code "make -f ${FN_TARGET} show"
make -f ${FN_TARGET} show

code "make -f ${FN_TARGET} build"
make -f ${FN_TARGET} build

code "make -f ${FN_TARGET} show"
make -f ${FN_TARGET} show

code "make -f ${FN_TARGET} clean"
make -f ${FN_TARGET} clean

code "make -f ${FN_TARGET} show"
make -f ${FN_TARGET} show
