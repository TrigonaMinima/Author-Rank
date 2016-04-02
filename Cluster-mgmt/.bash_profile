
BOLD="\[\033[1m\]"
OFF="\[\033[m\]"
PS1="${BOLD}\u@\h:\w\$${OFF} "
PS2="${BOLD}>${OFF} "


# added by Anaconda3 2.5.0 installer
export PATH="/Users/admin/anaconda/bin:$PATH"

export SCALA_HOME="/usr/local/bin/scala"

export PATH="$PATH:/usr/local/scala/bin"
export PATH="$PATH:/usr/local/spark/bin"

# Hadoop settings
export HADOOP_HOME="/usr/local/hadoop"
export PATH=$PATH:$HADOOP_HOME/bin
export HADOOP_PREFIX=$HADOOP_HOME
export HADOOP_CONF_DIR="/usr/local/hadoop/etc/hadoop"
export JAVA_HOME="$(/usr/libexec/java_home)"
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib"

# pyspark related variables
export PYSPARK_PYTHON=python
export PYTHONHASHSEED=0
# launches pyspark on the cluster
alias pyspark="pyspark --master spark://ap50.local:7077"