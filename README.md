## To run the script
` python fetch_data.py --query prometheus_http_response_size_bytes_count --datasource prometheus --uid edsob1tq38zcwf --date_from now-5m  `


` python3 fetch_data.py --query "sum(increase(net_conntrack_dialer_conn_failed_total{instance=~\"localhost:9090\"}[5m])) > 0" --datasource prometheus --uid edsob1tq38zcwf --date_from now-5m  `


`python3 fetch_data.py --query_name expr --query "rate(prometheus_tsdb_head_samples_appended_total{job=~\"prometheus\",instance=~\"localhost:9090\"}[1m])" --datasource prometheus --uid edsob1tq38zcwf --date_from now-5m`
