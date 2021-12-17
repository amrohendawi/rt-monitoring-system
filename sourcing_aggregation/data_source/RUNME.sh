# setup all binary files and run data_source with 95 priority and 5 minutes duration per test
make clean all && sudo ./data_source -p95 -d5s
