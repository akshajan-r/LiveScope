"""PySpark version of the UCSD streamer and daily aggregates (local mode).

The DuckDB path in livescope/ucsd.py handles the 100k sample comfortably; this
job is for the full 124M-interaction file, where Spark's partitioned,
out-of-core execution is the safer choice on a laptop or a CI runner. The
streamer table it writes matches `ucsd_streamer` from the DuckDB path, which
tests/test_spark.py checks on a small file.

Usage:
    python spark/ucsd_spark.py datastore/ucsd/full_a.csv.gz exports/ucsd_spark
"""

from __future__ import annotations

import sys

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql import types as T

ROUNDS_PER_DAY = 144

SCHEMA = T.StructType(
    [
        T.StructField("user_id", T.LongType()),
        T.StructField("stream_id", T.LongType()),
        T.StructField("streamer", T.StringType()),
        T.StructField("time_start", T.IntegerType()),
        T.StructField("time_stop", T.IntegerType()),
    ]
)


def spark_session(memory: str = "4g") -> SparkSession:
    return (
        SparkSession.builder.master("local[*]")
        .appName("livescope-ucsd")
        .config("spark.driver.memory", memory)
        .config("spark.sql.shuffle.partitions", "64")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )


def streamer_profile(df):
    rounds = F.col("time_stop") - F.col("time_start") + 1
    sessions = df.groupBy("streamer", "user_id").agg(F.count("*").alias("sessions"))
    return_rate = sessions.groupBy("streamer").agg(
        F.avg(F.when(F.col("sessions") > 1, 1.0).otherwise(0.0)).alias("return_rate")
    )
    profile = df.groupBy("streamer").agg(
        F.count("*").alias("interactions"),
        F.countDistinct("user_id").alias("unique_viewers"),
        F.countDistinct("stream_id").alias("streams"),
        (F.sum(rounds) / 6.0).alias("watch_hours"),
        (F.avg(rounds) * 10).alias("avg_session_minutes"),
        F.countDistinct(F.floor(F.col("time_start") / ROUNDS_PER_DAY)).alias("active_days"),
    )
    return profile.join(return_rate, "streamer")


def daily(df):
    return (
        df.withColumn("day", F.floor(F.col("time_start") / ROUNDS_PER_DAY))
        .groupBy("day")
        .agg(
            F.countDistinct("user_id").alias("users"),
            F.countDistinct("streamer").alias("streamers"),
            F.count("*").alias("interactions"),
            (F.sum(F.col("time_stop") - F.col("time_start") + 1) / 6.0).alias("watch_hours"),
        )
        .orderBy("day")
    )


def concentration(profile):
    w = Window.orderBy(F.col("watch_hours").desc())
    total = profile.agg(F.sum("watch_hours")).first()[0]
    n = profile.count()
    ranked = profile.select("watch_hours").withColumn("rnk", F.row_number().over(w))
    rows = []
    for pct in (0.001, 0.01, 0.1):
        top = max(1, int(-(-n * pct // 1)))
        share = ranked.where(F.col("rnk") <= top).agg(F.sum("watch_hours")).first()[0] / total
        rows.append((pct, float(share)))
    return rows


def main(src: str, out: str) -> None:
    spark = spark_session()
    df = spark.read.csv(src, schema=SCHEMA, header=False)
    profile = streamer_profile(df).cache()
    profile.write.mode("overwrite").parquet(f"{out}/ucsd_streamer")
    daily(df).write.mode("overwrite").parquet(f"{out}/ucsd_daily")
    for pct, share in concentration(profile):
        print(f"top {pct:.1%} of streamers get {share:.1%} of watch time")
    spark.stop()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
