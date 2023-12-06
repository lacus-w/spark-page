# exp20

```scala
import org.apache.spark.sql.streaming.Trigger
import spark.implicits._

sc.setLogLevel("WARN")
val lines = spark.readStream.
    format("socket").
    option("host","localhost").
    option("port",9999).
    load

val words = lines.as[String].flatMap(_.split(" "))
val wordCounts = words.groupBy("value").count
val query = wordCounts.writeStream.
    outputMode("complete").
    format("console").
    trigger(Trigger.ProcessingTime("8 seconds")).
    start
query.awaitTermination
```