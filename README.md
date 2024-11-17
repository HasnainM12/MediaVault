# Multi-threaded Chat System
A Java chat application I built to understand networking concepts and multi-threading. It uses Socket Programming to enable real-time communication between multiple clients through a central server.
## Features
- Real-time messaging between multiple clients
- Username system with join/leave notifications
- Server handles multiple connections simultaneously
- Clean console-based interface
## Built With
- Java
- Socket Programming
- Maven
- Multi-threading
## Setup
Build the project with Maven:
```bash
mvn clean install
```
Run the server:
```bash
mvn exec:java -D"exec.mainClass=basicchat.App" -D"exec.args=server"
```
In a new terminal, run a client:
```bash
mvn exec:java -D"exec.mainClass=basicchat.App" -D"exec.args=client"
```
Remember to:
- Keep server terminal running
- Start new terminal for each client
- Enter username when prompted
- Type 'exit' to quit client
## Future Plans
- Admin commands (kick/ban)
- Private messaging
- Chat rooms
- Message history
- Simple file sharing
- GUI interface
