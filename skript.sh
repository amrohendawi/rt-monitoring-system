start=`date +%s`
cyclictest -l10000 -m -Sp90 -i200 -h400 -q > new
end=`date +%s`

runtime=$((end-start))