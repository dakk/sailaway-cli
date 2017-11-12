# sailaway-cli


## Usage

### login
You need to login before using other commands; the login command will ask for username and password

```bash
sailaway-cli login [email] [password]
```

### list-boats
List the user boats

```bash
sailway-cli list-boats
```

### get-trip
Save the current trip to a gpx file:

```bash
sailaway-cli get-trip boatid output.gpx
```

### load-trip
Load a gpx trip into sailaway as current trip:

```bash
sailaway-cli load-trip boatid input.gpx
```

Or as a library entry:

```bash
sailaway-cli load-trip boatid --library input.gpx
```

### gps-serve
Serve current realtime boat data as GPSD server (for qtVLM and other softwares)

```bash
sailaway-cli gps-serve boatid [8888]
```

