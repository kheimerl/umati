#!/usr/bin/env sh

sh $MTURK_CMD_HOME/bin/loadHITs.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 \
-label umati_survey \
-input umati_survey.input \
-question umati_survey.question \
-properties umati_survey.properties 
