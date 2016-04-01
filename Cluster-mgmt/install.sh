echo "====Java version===="
java -version
echo "==========\n\n"

echo "====Brew installation===="
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo "==========\n\n"

echo "====wget, git installation===="
brew install wget git
echo "==========\n\n"

echo "====Scala installation===="
brew install scala
echo "==========\n\n"

echo "====Scala version===="
scala -version
echo "==========\n\n"

echo "export SCALA_HOME=/usr/local/bin/scala" >> ~/.bashrc
echo "export PATH=$PATH:$SCALA_HOME/bin" >> ~/.bashrc
source ~/.bashrc

echo "====Spark installation===="
tar xvf spark-1.6.1-bin-hadoop2.6.tar
sudo mv spark-1.6.1-bin-hadoop2.6 /usr/local/spark
echo "==========\n\n"

echo "export PATH=$PATH:/usr/local/spark/bin" >> ~/.bashrc
source ~/.bashrc

mv spark-1.6.1-bin-hadoop2.6.tar Used/

echo "====Checking Spark installation===="
spark-shell

