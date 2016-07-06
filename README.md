# RPi-Sensor-Web
Application software for a sensor-centric Raspberry Pi with full web application stack to provide user accessibility.

This mini-project is a full stack implemenation of a sensor device using the Raspberry Pi 2. The device uses a stack of web and application services to present a UI that gives a simple readout of connected sensors (in this case, temperature and humidity). This stack consists of a wireless Raspberry Pi running the Minibian OS, a uWSGI application server, Nginx web server, MySQLite, and built using the Flask framework (using Python). In addition, integration with the Plotly API allows for richer visualizations of collected data.

![Architecture Diagram](https://raw.githubusercontent.com/will-zegers/RPi-Sensor-Web/develop/img/architecture.png "Figure 1: System architecture")

The DB is updated every 10 minutes, and the UI allows the user to view data over re-set range (i.e. 3, 6, 12, and 24 hours) or, alternatively, use a datetime picker to choose a custom range and display the results graphicaly. The UI can also use the Plotly APIs to generate Plotly datasets and graphs.
