echo src/models:
scc src/models
echo src/views:
scc src/views
echo src/controllers:
scc src/controllers
#echo src/interfaces:
#scc src/interfaces
echo tests:
scc tests
#echo "all python files:"
#scc *.py
echo "Total:"
scc \
--exclude-dir output -M ".*\.csv"
