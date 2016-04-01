
BOLD="\[\033[1m\]"
OFF="\[\033[m\]"
PS1="${BOLD}\u@\h:\w\$${OFF} "
PS2="${BOLD}>${OFF} "


# added by Anaconda3 2.5.0 installer
export PATH="/Users/admin/anaconda/bin:$PATH"

export SCALA_HOME="/usr/local/bin/scala"

export PATH="$PATH:/usr/local/scala/bin"
export PATH="$PATH:/usr/local/spark/bin"

export PYSPARK_PYTHON=python


# Hadoop settings
export HADOOP_HOME="/usr/local/hadoop"
export PATH=$PATH:$HADOOP_HOME/bin
export HADOOP_PREFIX=$HADOOP_HOME
export HADOOP_CONF_DIR="/usr/local/hadoop/etc/hadoop"

export JAVA_HOME="$(/usr/libexec/java_home)"