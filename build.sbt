val Http4sVersion = "0.23.26"
val CirceVersion = "0.14.6"

lazy val root = (project in file("."))
  .settings(
    organization := "CCP",
    name := "Eve Docs",
    version := "1.0.0-SNAPSHOT",
    scalaVersion := "2.13.13",
    libraryDependencies ++= Seq(
      "ch.qos.logback" % "logback-classic" % "1.5.3" % Runtime,
      "com.lihaoyi" %% "requests" % "0.8.0",
      "io.circe" %% "circe-generic" % CirceVersion,
      "io.circe" %% "circe-parser" % CirceVersion,
      "org.http4s" %% "http4s-ember-server" % Http4sVersion,
      "org.http4s" %% "http4s-ember-client" % Http4sVersion,
      "org.http4s" %% "http4s-circe" % Http4sVersion,
      "org.http4s" %% "http4s-dsl" % Http4sVersion
    )
  )
