# Commands

### To start elasticsearch

- Go to the elasticsearch directory and give this command
> ./bin/elasticsearch

### To start flume (From your setup)

> flume-ng agent --conf /home/(srn)/apache-flume-1.10.0-bin/conf --conf-file ./flume/flume-kafka.conf --name agent1 -Dflume.root.logger=INFO,console -Xmx512m

### To run kafka

> sudo systemctl start kafka
