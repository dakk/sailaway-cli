# sailaway-cli


## Usage

### login
You need to login before using other commands; the login command will ask for username and password


```bash
sailaway-cli login
```

### get-trip
Save the current trip to a gpx file:

```bash
sailaway-cli get-trip output.gpx
```

### load-trip
Load a gpx trip into sailaway as current trip:

```bash
sailaway-cli load-trip input.gpx
```

Or as a library entry:

```bash
sailaway-cli load-trip --library input.gpx
```

### gps-serve
Serve current realtime boat data as NMEA server (for qtVLM and other softwares)

```bash
sailaway-cli gps-serve 8888
```

