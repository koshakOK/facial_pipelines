#!/usr/bin/env sh

if [ "$#" -eq 0 ]
then
    echo "Example: $0 'docker exec -it openface FeatureExtraction' videos output"
    exit 1
fi

FEAT_EXT_CMD="$1"
INDIR="$2"
OUTDIR="$3"

for file in $INDIR/*.mp4
do
    stem=$(basename $file .mp4)
    outdir_for_video="$OUTDIR/$stem"
    $FEAT_EXT_CMD -f "$file" -out_dir "$outdir_for_video"
done
