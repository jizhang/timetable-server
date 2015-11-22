Time Table
===

## Develop

* Install [Project Lombok](https://projectlombok.org/).
* Download source:

```bash
$ git clone git@github.com:jizhang/timetable
```

* Import into Eclipse as Maven project.
* Or run from command line:

```bash
$ mvn spring-boot:run
```

## Deploy

```bash
$ mvn package
$ java -jar target/timetable.jar --server.port=8080 --spring.datasource.url=jdbc:h2:./timetable
```
